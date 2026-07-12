"""旅游助手 Agent"""

import os
from typing import List, Optional

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage

from tools import (
    get_weather,
    search_places,
    get_place_details,
    calculate,
    estimate_budget,
    search_travel_knowledge,
)
from prompts import SYSTEM_PROMPT
from memory import create_memory

import dotenv

dotenv.load_dotenv(override=True)


class TravelAgent:
    """旅游助手 Agent"""

    def __init__(
        self,
        model_name: Optional[str] = None,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        temperature: float = 0.7,
        memory_k: int = 10,
    ):
        """初始化旅游助手"""
        # 初始化 LLM
        self.llm = ChatOpenAI(
            model=model_name or os.getenv("MODEL_NAME", "mimo-v2.5"),
            openai_api_key=api_key or os.getenv("OPENAI_API_KEY"),
            openai_api_base=api_base or os.getenv("OPENAI_BASE_URL"),
            temperature=temperature,
        )

        # 工具列表
        self.tools = [
            get_weather,
            search_places,
            get_place_details,
            calculate,
            estimate_budget,
            search_travel_knowledge,
        ]

        # 创建记忆
        self.memory = create_memory(k=memory_k)

        # 创建 Agent
        self.agent = create_agent(self.llm, self.tools)

    def _build_messages(self, user_input: str) -> list:
        """构建消息列表"""
        # 加载记忆
        history = self.memory.load_memory_variables({})

        # 构建消息
        messages = [SystemMessage(content=SYSTEM_PROMPT)]

        # 添加历史消息
        for msg in history.get("history", []):
            messages.append(msg)

        messages.append(HumanMessage(content=user_input))
        return messages

    def chat(self, user_input: str) -> str:
        """与旅游助手对话（非流式）"""
        messages = self._build_messages(user_input)

        # 调用 Agent
        result = self.agent.invoke({"messages": messages})

        # 提取回复
        response = result["messages"][-1].content

        # 保存到记忆
        self.memory.save_context({"input": user_input}, {"output": response})

        return response

    def chat_stream(self, user_input: str):
        """流式对话"""
        messages = self._build_messages(user_input)

        # 流式调用 Agent
        full_response = ""

        try:
            for chunk in self.agent.stream({"messages": messages}):
                # 处理 model 节点的输出（agent 思考和回复）
                if "model" in chunk:
                    model_msgs = chunk["model"].get("messages", [])
                    for msg in model_msgs:
                        if hasattr(msg, "content") and msg.content:
                            text = msg.content
                            yield text
                            full_response += text

                # 处理 tools 节点的输出
                elif "tools" in chunk:
                    tool_msgs = chunk["tools"].get("messages", [])
                    for msg in tool_msgs:
                        if hasattr(msg, "content") and msg.content:
                            # 工具输出不直接显示，但记录到完整回复
                            full_response += f"\n[工具调用结果]\n{msg.content}\n"
        except Exception as e:
            error_msg = f"\n抱歉，处理出错了：{str(e)}"
            yield error_msg
            full_response += error_msg

        # 保存到记忆
        if full_response:
            self.memory.save_context({"input": user_input}, {"output": full_response})

    def clear_memory(self):
        """清空记忆"""
        self.memory.clear()

    def get_memory(self) -> dict:
        """获取当前记忆"""
        return self.memory.load_memory_variables({})
