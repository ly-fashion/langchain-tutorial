"""启动旅游助手 Web 服务"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path
import threading


def start_backend():
    """启动 FastAPI 后端"""
    print("🚀 启动后端服务...")
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "api.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
    ], cwd=str(Path(__file__).parent))


def start_frontend():
    """启动 React 前端"""
    print("🚀 启动前端服务...")
    subprocess.run(["npm", "run", "dev"], cwd=str(Path(__file__).parent / "web"))


def open_browser():
    """打开浏览器"""
    time.sleep(3)
    print("🌐 打开浏览器...")
    webbrowser.open("http://localhost:3000")


if __name__ == "__main__":
    print("=" * 50)
    print("🌍 旅游助手 Web 服务")
    print("=" * 50)
    print()
    print("后端地址: http://localhost:8000")
    print("前端地址: http://localhost:3000")
    print()
    print("按 Ctrl+C 停止服务")
    print("=" * 50)
    print()

    # 在后台打开浏览器
    threading.Thread(target=open_browser, daemon=True).start()

    # 启动后端（主线程）
    try:
        start_backend()
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
