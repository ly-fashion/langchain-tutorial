"""记忆配置"""

from typing import List, Dict, Any
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage


class SimpleMemory:
    """简单的滑动窗口记忆"""

    def __init__(self, k: int = 10):
        """初始化记忆

        Args:
            k: 保留的对话轮数
        """
        self.k = k
        self.history: List[Dict[str, str]] = []

    def save_context(self, inputs: Dict[str, str], outputs: Dict[str, str]):
        """保存对话上下文

        Args:
            inputs: 输入 {"input": "..."}
            outputs: 输出 {"output": "..."}
        """
        self.history.append({
            "input": inputs.get("input", ""),
            "output": outputs.get("output", ""),
        })
        # 保留最近 k 轮
        if len(self.history) > self.k:
            self.history = self.history[-self.k:]

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, List[BaseMessage]]:
        """加载记忆变量

        Returns:
            {"history": [HumanMessage, AIMessage, ...]}
        """
        messages = []
        for item in self.history:
            if item["input"]:
                messages.append(HumanMessage(content=item["input"]))
            if item["output"]:
                messages.append(AIMessage(content=item["output"]))
        return {"history": messages}

    def clear(self):
        """清空记忆"""
        self.history = []


def create_memory(k: int = 10):
    """创建滑动窗口记忆

    Args:
        k: 保留的对话轮数

    Returns:
        SimpleMemory 实例
    """
    return SimpleMemory(k=k)
