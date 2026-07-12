"""FastAPI 后端 - 旅游助手 API"""

import sys
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
import json
import asyncio

from agent import TravelAgent

# 创建 FastAPI 应用
app = FastAPI(
    title="旅游助手 API",
    description="智能旅游助手后端服务",
    version="1.0.0",
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局 Agent 实例
travel_agent = None


class ChatRequest(BaseModel):
    """聊天请求"""
    message: str
    stream: bool = True


class ChatResponse(BaseModel):
    """聊天响应"""
    response: str
    status: str = "success"


class MessageHistory(BaseModel):
    """消息历史"""
    role: str  # "user" or "assistant"
    content: str


@app.on_event("startup")
async def startup():
    """应用启动时初始化 Agent"""
    global travel_agent
    travel_agent = TravelAgent()
    print("✓ 旅游助手 Agent 初始化成功")


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "旅游助手 API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/api/chat",
            "chat_stream": "/api/chat/stream",
            "history": "/api/history",
            "clear": "/api/clear",
        }
    }


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """聊天接口（非流式）"""
    if not travel_agent:
        return {"error": "Agent 未初始化"}

    try:
        response = travel_agent.chat(request.message)
        return ChatResponse(response=response)
    except Exception as e:
        return {"error": str(e)}


@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    """聊天接口（流式 SSE）"""
    if not travel_agent:
        return {"error": "Agent 未初始化"}

    async def event_generator():
        try:
            for chunk in travel_agent.chat_stream(request.message):
                yield {
                    "event": "message",
                    "data": json.dumps({"content": chunk}, ensure_ascii=False),
                }
                await asyncio.sleep(0.01)  # 小延迟避免阻塞

            yield {
                "event": "done",
                "data": json.dumps({"status": "complete"}),
            }
        except Exception as e:
            yield {
                "event": "error",
                "data": json.dumps({"error": str(e)}, ensure_ascii=False),
            }

    return EventSourceResponse(event_generator())


@app.get("/api/history")
async def get_history():
    """获取对话历史"""
    if not travel_agent:
        return {"error": "Agent 未初始化"}

    memory = travel_agent.get_memory()
    history = []

    for msg in memory.get("history", []):
        role = "user" if msg.type == "human" else "assistant"
        history.append({"role": role, "content": msg.content})

    return {"history": history}


@app.post("/api/clear")
async def clear_history():
    """清空对话历史"""
    if not travel_agent:
        return {"error": "Agent 未初始化"}

    travel_agent.clear_memory()
    return {"status": "success", "message": "对话历史已清空"}


@app.get("/api/health")
async def health():
    """健康检查"""
    return {"status": "healthy", "agent_ready": travel_agent is not None}


# 启动命令
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
