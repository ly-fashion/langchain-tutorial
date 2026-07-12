"""旅游助手 Agent 入口"""

import os
import sys
from pathlib import Path

# 设置 UTF-8 编码（Windows 兼容）
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加当前目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from agent import TravelAgent
from rich import print as rprint
from rich.console import Console
from rich.markdown import Markdown


console = Console()


def print_welcome():
    """打印欢迎信息"""
    welcome = """
# 🌍 旅游助手 Agent

欢迎使用旅游助手！我可以帮你：

- 🗺️ 查询目的地信息（景点、天气、交通）
- 📋 规划个性化行程
- 🏨 推荐住宿和美食
- 💰 估算旅行预算
- 📚 回答旅行相关问题

输入 `quit` 或 `exit` 退出
输入 `clear` 清空对话记忆
输入 `memory` 查看对话历史
"""
    console.print(Markdown(welcome))


def main():
    """主函数"""
    print_welcome()

    # 初始化 Agent
    try:
        agent = TravelAgent()
        rprint("[green]✓ 旅游助手初始化成功！[/green]\n")
    except Exception as e:
        rprint(f"[red]✗ 初始化失败: {e}[/red]")
        return

    # 对话循环
    while True:
        try:
            # 获取用户输入
            user_input = console.input("[bold cyan]你: [/bold cyan]")

            # 检查退出命令
            if user_input.lower() in ["quit", "exit", "q"]:
                rprint("\n[yellow]👋 再见！祝你旅途愉快！[/yellow]")
                break

            # 检查清空记忆命令
            if user_input.lower() == "clear":
                agent.clear_memory()
                rprint("[green]✓ 对话记忆已清空[/green]\n")
                continue

            # 检查查看记忆命令
            if user_input.lower() == "memory":
                memory = agent.get_memory()
                if memory.get("history"):
                    rprint("\n[bold]对话历史:[/bold]")
                    for msg in memory["history"]:
                        role = "你" if msg.type == "human" else "助手"
                        rprint(f"  [{role}]: {msg.content[:100]}...")
                else:
                    rprint("[dim]暂无对话历史[/dim]")
                rprint()
                continue

            # 检查空输入
            if not user_input.strip():
                continue

            # 调用 Agent
            rprint("\n[bold green]小旅: [/bold green]", end="")

            # 流式输出
            for chunk in agent.chat_stream(user_input):
                print(chunk, end="", flush=True)
            print("\n")

        except KeyboardInterrupt:
            rprint("\n\n[yellow]👋 再见！祝你旅途愉快！[/yellow]")
            break
        except Exception as e:
            rprint(f"\n[red]✗ 出错了: {e}[/red]\n")


if __name__ == "__main__":
    main()
