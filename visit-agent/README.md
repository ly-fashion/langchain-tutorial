# 🌍 旅游助手 Agent Web 界面

智能旅游助手，支持目的地查询、行程规划、住宿美食推荐等功能。

## 快速开始

### 方式一：一键启动

```bash
cd visit-agent
python start_web.py
```

### 方式二：分别启动

**启动后端：**
```bash
cd visit-agent
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

**启动前端：**
```bash
cd visit-agent/web
npm run dev
```

### 访问地址

- 前端界面: http://localhost:3000
- 后端 API: http://localhost:8000
- API 文档: http://localhost:8000/docs

## 功能特性

- 🗺️ 景点查询：搜索城市热门景点
- 🌤️ 天气查询：获取实时天气信息
- 📋 行程规划：智能生成旅行行程
- 💰 预算估算：计算旅行费用
- 🍜 美食推荐：推荐当地特色美食
- 📚 旅游知识：签证、行李、交通等信息
- 💬 流式对话：实时显示回复内容
- 🔄 多轮对话：记住上下文

## 项目结构

```
visit-agent/
├── api/                    # FastAPI 后端
│   ├── __init__.py
│   └── main.py            # API 服务
├── web/                    # React 前端
│   ├── src/
│   │   ├── App.jsx        # 主组件
│   │   ├── components/    # UI 组件
│   │   │   ├── Header.jsx
│   │   │   ├── ChatBox.jsx
│   │   │   ├── Message.jsx
│   │   │   └── InputBox.jsx
│   │   └── index.css      # 样式
│   ├── package.json
│   └── vite.config.js
├── tools/                  # Agent 工具
├── prompts/                # 提示词
├── memory/                 # 记忆配置
├── agent.py                # Agent 主体
├── main.py                 # 命令行入口
├── start_web.py            # Web 启动脚本
└── README.md
```

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/chat` | POST | 聊天（非流式） |
| `/api/chat/stream` | POST | 聊天（流式 SSE） |
| `/api/history` | GET | 获取对话历史 |
| `/api/clear` | POST | 清空对话历史 |
| `/api/health` | GET | 健康检查 |

## 示例对话

```
你: 北京有什么好玩的？
小旅: 北京热门景点推荐...

你: 帮我规划3天行程
小旅: Day 1: 故宫 → 天安门 → 王府井...

你: 需要多少钱？
小旅: 预算估算：3000-5000元...
```

## 技术栈

- **后端**: FastAPI + SSE
- **前端**: React + Vite + TailwindCSS
- **AI**: LangChain + MiMo-v2.5
