# LangChain 中间件完全指南

> LangChain 的中间件机制让你可以在 LLM 调用的各个环节插入自定义逻辑

---

## 目录

1. [核心概念](#1-核心概念)
2. [Callbacks 回调系统](#2-callbacks-回调系统)
3. [LCEL 表达式语言](#3-lcel-表达式语言)
4. [Runnable 基础组件](#4-runnable-基础组件)
5. [流式处理 Streaming](#5-流式处理-streaming)
6. [错误处理与重试](#6-错误处理与重试)
7. [缓存机制](#7-缓存机制)
8. [日志与追踪](#8-日志与追踪)
9. [安全与认证](#9-安全与认证)
10. [实战示例](#10-实战示例)

---

## 1. 核心概念

### 什么是中间件？

中间件是在请求处理过程中插入的逻辑层，可以：

- **拦截** - 在调用前后执行自定义逻辑
- **转换** - 修改输入或输出
- **监控** - 记录日志、追踪性能
- **容错** - 实现重试、降级、超时

### LangChain 中间件架构

```
用户输入
    ↓
[前置处理] → [LLM调用] → [后置处理]
    ↓           ↓           ↓
  转换输入    执行模型    转换输出
    ↓           ↓           ↓
     ← ← ← Callbacks ← ← ←
    ↓
最终输出
```

---

## 2. Callbacks 回调系统

### 2.1 回调事件类型

| 事件                 | 触发时机       | 用途             |
| -------------------- | -------------- | ---------------- |
| `on_llm_start`       | LLM 开始调用   | 记录输入、预处理 |
| `on_llm_new_token`   | 生成新 token   | 流式输出         |
| `on_llm_end`         | LLM 调用结束   | 记录输出、后处理 |
| `on_llm_error`       | LLM 调用出错   | 错误处理         |
| `on_chain_start`     | Chain 开始执行 | 追踪执行流程     |
| `on_chain_end`       | Chain 执行结束 | 收集结果         |
| `on_chain_error`     | Chain 执行出错 | 错误处理         |
| `on_tool_start`      | 工具开始调用   | 记录工具使用     |
| `on_tool_end`        | 工具调用结束   | 记录工具结果     |
| `on_tool_error`      | 工具调用出错   | 错误处理         |
| `on_retriever_start` | 检索开始       | 记录检索查询     |
| `on_retriever_end`   | 检索结束       | 记录检索结果     |

### 2.2 自定义回调处理器

```python
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult

class MyCallbackHandler(BaseCallbackHandler):
    """自定义回调处理器"""

    def on_llm_start(self, serialized, prompts, **kwargs):
        """LLM 开始时触发"""
        print(f"LLM 开始，输入: {prompts[0][:50]}...")

    def on_llm_new_token(self, token, **kwargs):
        """流式输出时每个新 token 触发"""
        print(token, end="", flush=True)

    def on_llm_end(self, response: LLMResult, **kwargs):
        """LLM 结束时触发"""
        print(f"\nLLM 完成，消耗 tokens: {response.llm_output}")

    def on_llm_error(self, error, **kwargs):
        """LLM 出错时触发"""
        print(f"LLM 错误: {error}")

    def on_chain_start(self, serialized, inputs, **kwargs):
        """Chain 开始时触发"""
        print(f"Chain 开始: {serialized.get('name', 'unknown')}")

    def on_tool_start(self, serialized, input_str, **kwargs):
        """工具开始时触发"""
        print(f"工具调用: {serialized.get('name')}")

    def on_tool_end(self, output, **kwargs):
        """工具结束时触发"""
        print(f"工具结果: {output[:100]}")
```

### 2.3 使用回调

```python
from langchain_openai import ChatOpenAI

# 方式1: 构造函数传入
llm = ChatOpenAI(callbacks=[MyCallbackHandler()])

# 方式2: 调用时传入
response = llm.invoke("你好", config={"callbacks": [MyCallbackHandler()]})

# 方式3: 全局配置
from langchain_core.runnables import RunnableConfig
config = RunnableConfig(callbacks=[MyCallbackHandler()])
```

### 2.4 异步回调

```python
class AsyncCallbackHandler(BaseCallbackHandler):
    async def on_llm_start(self, serialized, prompts, **kwargs):
        await some_async_operation()

    async def on_llm_new_token(self, token, **kwargs):
        await stream_to_client(token)

# 使用异步回调
response = await llm.ainvoke("你好", config={"callbacks": [AsyncCallbackHandler()]})
```

---

## 3. LCEL 表达式语言

### 3.1 什么是 LCEL

LCEL (LangChain Expression Language) 是声明式构建链的方式，使用 `|` 管道符连接组件。

### 3.2 管道操作符 `|`

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 基础链
chain = prompt | llm | output_parser

# 等价于
chain = prompt.pipe(llm).pipe(output_parser)
```

### 3.3 链的组合模式

```python
# 顺序执行
chain = step1 | step2 | step3

# 嵌套链
inner_chain = step1 | step2
full_chain = inner_chain | step3

# 带分支的链 (使用 RunnableParallel)
from langchain_core.runnables import RunnableParallel

parallel_chain = RunnableParallel(
    summary=summary_chain,
    keywords=keywords_chain
)
```

---

## 4. Runnable 基础组件

### 4.1 Runnable 接口

所有 LCEL 组件都实现 Runnable 接口：

| 方法                    | 说明                   |
| ----------------------- | ---------------------- |
| `invoke(input)`         | 同步调用，处理单个输入 |
| `ainvoke(input)`        | 异步调用               |
| `batch(inputs)`         | 批量处理               |
| `abatch(inputs)`        | 异步批量处理           |
| `stream(input)`         | 流式输出               |
| `astream(input)`        | 异步流式输出           |
| `astream_events(input)` | 异步事件流             |

### 4.2 RunnablePassthrough

透传输入，常用于预处理：

```python
from langchain_core.runnables import RunnablePassthrough

# 直接透传
passthrough = RunnablePassthrough()
result = passthrough.invoke("hello")  # 返回 "hello"

# 带预处理的透传
def preprocess(text):
    return text.upper()

chain = RunnablePassthrough(preprocess) | llm
```

### 4.3 RunnableLambda

将普通函数转为 Runnable：

```python
from langchain_core.runnables import RunnableLambda

# 从函数创建
def count_words(text):
    return {"word_count": len(text.split())}

counter = RunnableLambda(count_words)
result = counter.invoke("hello world")  # {"word_count": 2}

# 带异步支持
async def async_process(text):
    await asyncio.sleep(1)
    return text.upper()

async_runnable = RunnableLambda(async_process)
```

### 4.4 RunnableParallel

并行执行多个 Runnable：

```python
from langchain_core.runnables import RunnableParallel

# 并行执行
parallel = RunnableParallel(
    summary=summary_chain,
    sentiment=sentiment_chain,
    keywords=keywords_chain
)

result = parallel.invoke({"text": "这是一段测试文本"})
# 返回 {"summary": "...", "sentiment": "...", "keywords": [...]}
```

### 4.5 RunnableSequence

显式顺序执行：

```python
from langchain_core.runnables import RunnableSequence

sequence = RunnableSequence(
    first=preprocess,
    middle=[step1, step2],
    last=format_output
)

# 等价于 preprocess | step1 | step2 | format_output
```

### 4.6 RunnableBranch

条件分支执行：

```python
from langchain_core.runnables import RunnableBranch

def is_question(text):
    return "?" in text or "？" in text

branch = RunnableBranch(
    (is_question, question_chain),      # 条件匹配时执行
    (lambda x: len(x) > 100, long_chain),  # 另一个条件
    default_chain                        # 默认分支
)

result = branch.invoke("什么是AI？")  # 走 question_chain
```

### 4.7 RunnableConfig

运行时配置：

```python
from langchain_core.runnables import RunnableConfig

config = RunnableConfig(
    callbacks=[MyCallback()],           # 回调处理器
    max_concurrency=5,                  # 最大并发数
    run_name="my_chain",               # 运行名称
    tags=["production"],                # 标签
    metadata={"version": "1.0"},       # 元数据
    recursion_limit=25,                 # 递归限制
)

result = chain.invoke(input, config=config)
```

---

## 5. 流式处理 Streaming

### 5.1 基础流式输出

```python
# 同步流式
for chunk in llm.stream("写一首诗"):
    print(chunk.content, end="", flush=True)

# 异步流式
async for chunk in llm.astream("写一首诗"):
    print(chunk.content, end="", flush=True)
```

### 5.2 链的流式输出

```python
chain = prompt | llm | StrOutputParser()

for chunk in chain.stream({"topic": "春天"}):
    print(chunk, end="", flush=True)
```

### 5.3 事件流 (astream_events)

```python
async for event in chain.astream_events({"topic": "春天"}, version="v2"):
    if event["event"] == "on_chat_model_stream":
        print(event["data"]["chunk"].content, end="")
    elif event["event"] == "on_tool_start":
        print(f"工具开始: {event['name']}")
```

### 5.4 自定义流式处理

```python
class StreamProcessor:
    def __init__(self):
        self.buffer = ""

    def process_token(self, token):
        self.buffer += token
        # 自定义处理逻辑
        if len(self.buffer) > 100:
            self.flush()

    def flush(self):
        print(self.buffer, end="")
        self.buffer = ""

processor = StreamProcessor()
for chunk in llm.stream("写一篇长文"):
    processor.process_token(chunk.content)
processor.flush()
```

---

## 6. 错误处理与重试

### 6.1 Fallbacks 降级机制

```python
from langchain_core.runnables import RunnableWithFallbacks

# 主模型 + 降级模型
primary_llm = ChatOpenAI(model="gpt-4")
fallback_llm = ChatOpenAI(model="gpt-3.5-turbo")

chain_with_fallback = primary_llm.with_fallbacks([fallback_llm])

# 如果 gpt-4 失败，自动使用 gpt-3.5
result = chain_with_fallback.invoke("你好")
```

### 6.2 重试策略

```python
from langchain_core.runnables import RunnableRetry

# 基础重试
chain_with_retry = chain.with_retry(
    stop_after_attempt=3,      # 最多重试3次
    wait_exponential_jitter=True,  # 指数退避+抖动
)

# 自定义重试条件
def should_retry(error):
    return isinstance(error, TimeoutError)

chain_with_retry = chain.with_retry(
    stop_after_attempt=3,
    retry_if_exception_type=(TimeoutError,),
)
```

### 6.3 超时控制

```python
# 设置超时
chain_with_timeout = chain.with_config(timeout=30)  # 30秒超时

# 异步超时
import asyncio
try:
    result = await asyncio.wait_for(
        chain.ainvoke("你好"),
        timeout=30.0
    )
except asyncio.TimeoutError:
    print("请求超时")
```

### 6.4 全局错误处理

```python
from langchain_core.runnables import RunnableWithMessageHistory

class ErrorHandler:
    def handle_error(self, error, context):
        # 记录错误
        logger.error(f"Error: {error}, Context: {context}")
        # 发送告警
        send_alert(error)
        # 返回默认值
        return "抱歉，处理出错了"

error_handler = ErrorHandler()
```

---

## 7. 缓存机制

### 7.1 内存缓存

```python
from langchain_core.globals import set_llm_cache
from langchain_core.caches import InMemoryCache

# 设置全局缓存
set_llm_cache(InMemoryCache())

# 第一次调用会请求API
result1 = llm.invoke("什么是AI？")

# 第二次相同调用会使用缓存
result2 = llm.invoke("什么是AI？")
```

### 7.2 Redis 缓存

```python
from langchain_community.cache import RedisCache
import redis

redis_client = redis.Redis(host="localhost", port=6379)
set_llm_cache(RedisCache(redis_client))
```

### 7.3 SQLite 缓存

```python
from langchain_community.cache import SQLiteCache

set_llm_cache(SQLiteCache(database_path=".langchain.db"))
```

### 7.4 语义缓存

```python
from langchain_community.cache import RedisSemanticCache
from langchain_openai import OpenAIEmbeddings

embedding = OpenAIEmbeddings()
semantic_cache = RedisSemanticCache(
    redis_url="redis://localhost:6379",
    embedding=embedding,
    score_threshold=0.2  # 相似度阈值
)
set_llm_cache(semantic_cache)
```

### 7.5 自定义缓存

```python
from langchain_core.caches import BaseCache

class CustomCache(BaseCache):
    def lookup(self, prompt, llm_string):
        # 查找缓存
        key = self._generate_key(prompt, llm_string)
        return self.cache.get(key)

    def update(self, prompt, llm_string, return_val):
        # 更新缓存
        key = self._generate_key(prompt, llm_string)
        self.cache[key] = return_val

    def clear(self):
        # 清除缓存
        self.cache.clear()
```

---

## 8. 日志与追踪

### 8.1 LangSmith 集成

```python
import os

# 启用 LangSmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-api-key"
os.environ["LANGCHAIN_PROJECT"] = "my-project"

# 所有调用都会自动追踪
result = llm.invoke("你好")
```

### 8.2 自定义日志

```python
import logging

logger = logging.getLogger("langchain")
logger.setLevel(logging.INFO)

class LoggingCallback(BaseCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kwargs):
        logger.info(f"LLM Start: {prompts[0][:100]}")

    def on_llm_end(self, response, **kwargs):
        logger.info(f"LLM End: {response.llm_output}")

    def on_tool_start(self, serialized, input_str, **kwargs):
        logger.info(f"Tool Start: {serialized['name']}")

    def on_tool_end(self, output, **kwargs):
        logger.info(f"Tool End: {output[:100]}")
```

### 8.3 性能监控

```python
import time

class PerformanceMonitor(BaseCallbackHandler):
    def __init__(self):
        self.timers = {}

    def on_llm_start(self, serialized, prompts, **kwargs):
        self.timers['llm'] = time.time()

    def on_llm_end(self, response, **kwargs):
        elapsed = time.time() - self.timers['llm']
        logger.info(f"LLM 耗时: {elapsed:.2f}秒")

    def on_tool_start(self, serialized, input_str, **kwargs):
        self.timers['tool'] = time.time()

    def on_tool_end(self, output, **kwargs):
        elapsed = time.time() - self.timers['tool']
        logger.info(f"工具耗时: {elapsed:.2f}秒")
```

---

## 9. 安全与认证

### 9.1 API Key 管理

```python
from langchain_core.utils import get_from_env

# 从环境变量获取
api_key = get_from_env("OPENAI_API_KEY", "OPENAI_API_KEY")

# 使用 SecretStr
from pydantic import SecretStr

class Config:
    api_key: SecretStr = SecretStr("sk-xxx")
```

### 9.2 输入验证

```python
from pydantic import BaseModel, validator

class UserInput(BaseModel):
    query: str

    @validator('query')
    def validate_query(cls, v):
        if len(v) > 1000:
            raise ValueError('查询过长')
        if any(word in v.lower() for word in ['hack', 'exploit']):
            raise ValueError('不安全的输入')
        return v

def safe_invoke(input_text):
    validated = UserInput(query=input_text)
    return chain.invoke(validated.query)
```

### 9.3 输出过滤

```python
def filter_output(text):
    """过滤敏感信息"""
    import re
    # 隐藏手机号
    text = re.sub(r'1[3-9]\d{9}', '***手机***', text)
    # 隐藏邮箱
    text = re.sub(r'[\w.+-]+@[\w-]+\.[\w.]+', '***邮箱***', text)
    return text

chain_with_filter = chain | RunnableLambda(filter_output)
```

---

## 10. 实战示例

### 10.1 带完整中间件的链

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableLambda,
    RunnableConfig,
    RunnableWithFallbacks,
)

# 1. 定义回调
class ProductionCallback(BaseCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kwargs):
        logger.info(f"开始处理: {prompts[0][:50]}")

    def on_llm_end(self, response, **kwargs):
        logger.info(f"处理完成")

    def on_llm_error(self, error, **kwargs):
        logger.error(f"处理失败: {error}")
        alert_system.notify(error)

# 2. 创建带中间件的 LLM
llm = ChatOpenAI(
    model="gpt-4",
    callbacks=[ProductionCallback()],
    max_retries=3,
    timeout=30,
)

# 3. 创建链
prompt = ChatPromptTemplate.from_template("回答：{question}")
output_parser = StrOutputParser()

# 4. 添加预处理和后处理
def preprocess(input):
    return {"question": input["question"].strip()}

def postprocess(output):
    return {"answer": output, "timestamp": datetime.now()}

chain = (
    RunnableLambda(preprocess)
    | prompt
    | llm.with_fallbacks([ChatOpenAI(model="gpt-3.5-turbo")])
    | output_parser
    | RunnableLambda(postprocess)
)

# 5. 使用
result = chain.invoke(
    {"question": "什么是AI？"},
    config=RunnableConfig(
        tags=["production"],
        metadata={"user_id": "123"},
    )
)
```

### 10.2 带重试和缓存的链

```python
from langchain_core.globals import set_llm_cache
from langchain_core.caches import InMemoryCache

# 设置缓存
set_llm_cache(InMemoryCache())

# 创建带重试的链
chain = (
    prompt
    | llm.with_retry(stop_after_attempt=3)
    | output_parser
)

# 第一次调用
result1 = chain.invoke({"question": "什么是机器学习？"})

# 第二次相同调用会使用缓存
result2 = chain.invoke({"question": "什么是机器学习？"})
```

### 10.3 流式处理链

```python
async def stream_with_events(question):
    chain = prompt | llm | StrOutputParser()

    async for event in chain.astream_events(
        {"question": question},
        version="v2"
    ):
        if event["event"] == "on_chat_model_stream":
            token = event["data"]["chunk"].content
            yield token
        elif event["event"] == "on_tool_start":
            yield f"\n[工具调用: {event['name']}]\n"

# 使用
async for token in stream_with_events("写一首诗"):
    print(token, end="", flush=True)
```

---

## 概念速查表

| 概念 | 类/函数               | 用途           |
| ---- | --------------------- | -------------- |
| 回调 | `BaseCallbackHandler` | 拦截事件       |
| 管道 | `\|` 操作符           | 组合链         |
| 透传 | `RunnablePassthrough` | 直接传递输入   |
| 函数 | `RunnableLambda`      | 函数转Runnable |
| 并行 | `RunnableParallel`    | 并行执行       |
| 分支 | `RunnableBranch`      | 条件执行       |
| 降级 | `with_fallbacks()`    | 失败时降级     |
| 重试 | `with_retry()`        | 自动重试       |
| 缓存 | `InMemoryCache`       | 结果缓存       |
| 流式 | `stream()`            | 流式输出       |
| 配置 | `RunnableConfig`      | 运行时配置     |
| 追踪 | LangSmith             | 调用追踪       |

---

## 学习路径

1. **入门**: Callbacks → LCEL → Runnable
2. **进阶**: Streaming → 错误处理 → 缓存
3. **高级**: 自定义中间件 → 性能优化 → 生产部署
