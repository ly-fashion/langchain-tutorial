# LangChain 完全知识图谱

> 最全面的 LangChain 知识点总结，涵盖所有核心概念和组件

---

## 目录

- [1. 基础架构](#1-基础架构)
- [2. LLMs 语言模型](#2-llms-语言模型)
- [3. Chat Models 聊天模型](#3-chat-models-聊天模型)
- [4. Prompt Templates 提示词模板](#4-prompt-templates-提示词模板)
- [5. Output Parsers 输出解析器](#5-output-parsers-输出解析器)
- [6. Chains 链](#6-chains-链)
- [7. Memory 记忆系统](#7-memory-记忆系统)
- [8. Agents 智能代理](#8-agents-智能代理)
- [9. Tools 工具](#9-tools-工具)
- [10. Retrievers 检索器](#10-retrievers-检索器)
- [11. Document Loaders 文档加载器](#11-document-loaders-文档加载器)
- [12. Text Splitters 文本分割器](#12-text-splitters-文本分割器)
- [13. Vector Stores 向量数据库](#13-vector-stores-向量数据库)
- [14. Embeddings 嵌入模型](#14-embeddings-嵌入模型)
- [15. Callbacks 回调系统](#15-callbacks-回调系统)
- [16. LCEL 表达式语言](#16-lcel-表达式语言)
- [17. Runnables 可运行组件](#17-runnables-可运行组件)
- [18. Indexing 索引系统](#18-indexing-索引系统)
- [19. Evaluation 评估系统](#19-evaluation-评估系统)
- [20. Tracing 追踪系统](#20-tracing-追踪系统)
- [21. Caching 缓存机制](#21-caching-缓存机制)
- [22. Streaming 流式处理](#22-streaming-流式处理)
- [23. Structured Output 结构化输出](#23-structured-output-结构化输出)
- [24. Multi-modal 多模态](#24-multi-modal-多模态)
- [25. LangGraph 图状态机](#25-langgraph-图状态机)
- [26. LangSmith 监控平台](#26-langsmith-监控平台)
- [27. 部署与生产](#27-部署与生产)

---

## 1. 基础架构

### 1.1 核心理念

```
LangChain = LLM + 数据 + 计算
```

### 1.2 架构组件

```
┌─────────────────────────────────────────────────────────┐
│                    LangChain 生态系统                      │
├─────────────────────────────────────────────────────────┤
│  langchain-core      │ 核心抽象和接口                      │
│  langchain-community │ 第三方集成                          │
│  langchain           │ 认知架构（Chains, Agents, Retrieval）│
│  langgraph           │ 有状态的多Actor应用                  │
│  langsmith           │ 追踪、评估、监控                    │
└─────────────────────────────────────────────────────────┘
```

### 1.3 核心抽象

| 抽象                | 说明               |
| ------------------- | ------------------ |
| Runnable            | 所有组件的基础接口 |
| RunnableSequence    | 顺序执行           |
| RunnableParallel    | 并行执行           |
| RunnableBranch      | 条件分支           |
| RunnablePassthrough | 透传               |
| RunnableLambda      | 函数包装           |

---

## 2. LLMs 语言模型

### 2.1 支持的模型提供商

| 提供商      | 模型示例             |
| ----------- | -------------------- |
| OpenAI      | GPT-4, GPT-3.5-turbo |
| Anthropic   | Claude-3, Claude-2   |
| Google      | Gemini, PaLM         |
| Azure       | Azure OpenAI         |
| HuggingFace | Llama, Mistral       |
| Ollama      | 本地模型             |
| 本地        | 自托管模型           |

### 2.2 基础用法

```python
from langchain_openai import OpenAI

llm = OpenAI(model="gpt-3.5-turbo")
result = llm.invoke("你好")
```

### 2.3 关键参数

| 参数              | 说明         |
| ----------------- | ------------ |
| model             | 模型名称     |
| temperature       | 创造性 (0-2) |
| max_tokens        | 最大输出长度 |
| top_p             | 核采样       |
| frequency_penalty | 频率惩罚     |
| presence_penalty  | 存在惩罚     |
| timeout           | 超时时间     |
| max_retries       | 最大重试次数 |
| streaming         | 是否流式输出 |

### 2.4 异步调用

```python
result = await llm.ainvoke("你好")
async for chunk in llm.astream("你好"):
    print(chunk)
```

### 2.5 批量调用

```python
results = llm.batch(["你好", "世界"])
```

---

## 3. Chat Models 聊天模型

### 3.1 消息类型

| 类型            | 说明                 |
| --------------- | -------------------- |
| SystemMessage   | 系统提示             |
| HumanMessage    | 用户消息             |
| AIMessage       | AI 回复              |
| ToolMessage     | 工具调用结果         |
| FunctionMessage | 函数调用结果（旧版） |

### 3.2 基础用法

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

chat = ChatOpenAI(model="gpt-4")
messages = [
    SystemMessage(content="你是一个有帮助的助手"),
    HumanMessage(content="你好")
]
response = chat.invoke(messages)
```

### 3.3 结构化输出

```python
from pydantic import BaseModel

class Answer(BaseModel):
    answer: str
    confidence: float

structured_chat = chat.with_structured_output(Answer)
result = structured_chat.invoke("什么是AI？")
```

### 3.4 工具调用

```python
tools = [get_weather, calculate]
chat_with_tools = chat.bind_tools(tools)
response = chat_with_tools.invoke("北京天气怎么样？")
```

---

## 4. Prompt Templates 提示词模板

### 4.1 模板类型

| 类型                   | 说明       |
| ---------------------- | ---------- |
| PromptTemplate         | 基础模板   |
| ChatPromptTemplate     | 聊天模板   |
| FewShotPromptTemplate  | 少样本模板 |
| PipelinePromptTemplate | 管道模板   |
| MessagesPlaceholder    | 消息占位符 |

### 4.2 PromptTemplate

```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "请用{language}解释什么是{topic}"
)
result = prompt.invoke({"language": "中文", "topic": "AI"})
```

### 4.3 ChatPromptTemplate

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}"),
    ("human", "{question}")
])
```

### 4.4 FewShotPromptTemplate

```python
from langchain_core.prompts import FewShotPromptTemplate

examples = [
    {"input": "好", "output": "正面"},
    {"input": "差", "output": "负面"},
]

prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="判断情感：",
    suffix="输入：{input}\n输出：",
)
```

### 4.5 MessagesPlaceholder

```python
from langchain_core.prompts import MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个有帮助的助手"),
    MessagesPlaceholder("history"),
    ("human", "{input}")
])
```

### 4.6 模板组合

```python
# 管道组合
prompt1 = PromptTemplate.from_template("总结：{text}")
prompt2 = PromptTemplate.from_template("翻译成{language}：{text}")
pipeline = prompt1 | prompt2
```

---

## 5. Output Parsers 输出解析器

### 5.1 解析器类型

| 类型                  | 说明              |
| --------------------- | ----------------- |
| StrOutputParser       | 字符串解析        |
| JsonOutputParser      | JSON 解析         |
| PydanticOutputParser  | Pydantic 模型解析 |
| XMLOutputParser       | XML 解析          |
| CSVOutputParser       | CSV 解析          |
| DatetimeOutputParser  | 日期时间解析      |
| EnumOutputParser      | 枚举解析          |
| PydanticToolsParser   | 工具输出解析      |
| JsonOutputToolsParser | 工具 JSON 解析    |

### 5.2 StrOutputParser

```python
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()
chain = prompt | llm | parser
```

### 5.3 JsonOutputParser

```python
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()
prompt = PromptTemplate(
    template="回答问题\n{format_instructions}\n{question}",
    partial_variables={"format_instructions": parser.get_format_instructions()}
)
```

### 5.4 PydanticOutputParser

```python
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

class Movie(BaseModel):
    title: str = Field(description="电影名称")
    year: int = Field(description="年份")
    rating: float = Field(description="评分")

parser = PydanticOutputParser(pydantic_object=Movie)
```

### 5.5 自定义解析器

```python
from langchain_core.output_parsers import BaseOutputParser

class CustomParser(BaseOutputParser):
    def parse(self, text: str):
        # 自定义解析逻辑
        return parsed_result

    def get_format_instructions(self):
        return "请按照以下格式输出..."
```

### 5.6 输出修复

```python
from langchain.output_parsers import OutputFixingParser

fixing_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)
```

---

## 6. Chains 链

### 6.1 链的类型

| 类型                         | 说明         |
| ---------------------------- | ------------ |
| LLMChain                     | 基础 LLM 链  |
| SequentialChain              | 顺序链       |
| TransformChain               | 转换链       |
| RouterChain                  | 路由链       |
| ConversationChain            | 对话链       |
| RetrievalQA                  | 检索问答链   |
| ConversationalRetrievalChain | 对话检索链   |
| StuffDocumentsChain          | 文档填充链   |
| MapReduceDocumentsChain      | MapReduce 链 |
| RefineDocumentsChain         | 迭代优化链   |

### 6.2 LCEL 链（推荐）

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

chain = prompt | llm | output_parser
result = chain.invoke({"input": "你好"})
```

### 6.3 顺序链

```python
from langchain.chains import SequentialChain

chain = SequentialChain(
    chains=[chain1, chain2, chain3],
    input_variables=["input"],
    output_variables=["output"]
)
```

### 6.4 路由链

```python
from langchain.chains import LLMRouterChain

router_chain = LLMRouterChain.from_llm(llm, router_prompt)
```

### 6.5 检索问答链

```python
from langchain.chains import RetrievalQA

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # stuff, map_reduce, refine, map_rerank
    retriever=retriever
)
```

### 6.6 对话检索链

```python
from langchain.chains import ConversationalRetrievalChain

chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory
)
```

### 6.7 文档处理链类型

| 类型       | 说明     | 适用场景 |
| ---------- | -------- | -------- |
| stuff      | 填充     | 短文档   |
| map_reduce | 映射归约 | 长文档   |
| refine     | 迭代优化 | 需要精确 |
| map_rerank | 映射重排 | 需要评分 |

---

## 7. Memory 记忆系统

### 7.1 记忆类型

| 类型                            | 说明             |
| ------------------------------- | ---------------- |
| ConversationBufferMemory        | 缓冲记忆（全部） |
| ConversationBufferWindowMemory  | 滑动窗口         |
| ConversationSummaryMemory       | 摘要记忆         |
| ConversationSummaryBufferMemory | 混合记忆         |
| ConversationEntityMemory        | 实体记忆         |
| ConversationKGMemory            | 知识图谱记忆     |
| VectorStoreRetrieverMemory      | 向量检索记忆     |
| RedisChatMessageHistory         | Redis 存储       |
| FileChatMessageHistory          | 文件存储         |

### 7.2 ConversationBufferMemory

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(return_messages=True)
memory.save_context({"input": "你好"}, {"output": "你好！"})
variables = memory.load_memory_variables({})
```

### 7.3 ConversationBufferWindowMemory

```python
memory = ConversationBufferWindowMemory(k=5, return_messages=True)
```

### 7.4 ConversationSummaryMemory

```python
memory = ConversationSummaryMemory(llm=llm, return_messages=True)
```

### 7.5 ConversationSummaryBufferMemory

```python
memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=200,
    return_messages=True
)
```

### 7.6 ConversationEntityMemory

```python
memory = ConversationEntityMemory(llm=llm, return_messages=True)
```

### 7.7 在链中使用记忆

```python
from langchain_core.prompts import MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个有帮助的助手"),
    MessagesPlaceholder("history"),
    ("human", "{input}")
])

chain = prompt | llm | output_parser
```

### 7.8 持久化记忆

```python
from langchain.memory import RedisChatMessageHistory

history = RedisChatMessageHistory(
    session_id="user_123",
    url="redis://localhost:6379"
)
```

---

## 8. Agents 智能代理

### 8.1 Agent 类型

| 类型                   | 说明            |
| ---------------------- | --------------- |
| OpenAI Functions Agent | OpenAI 函数调用 |
| OpenAI Tools Agent     | OpenAI 工具调用 |
| ReAct Agent            | 推理-行动代理   |
| Plan-and-Execute Agent | 规划执行代理    |
| Self-Ask Agent         | 自问自答代理    |
| Conversational Agent   | 对话代理        |
| XML Agent              | XML 代理        |
| Structured Chat Agent  | 结构化聊天代理  |

### 8.2 创建 Agent

```python
from langchain.agents import create_react_agent, AgentExecutor

agent = create_react_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)
result = executor.invoke({"input": "北京天气怎么样？"})
```

### 8.3 OpenAI Functions Agent

```python
from langchain.agents import create_openai_functions_agent

agent = create_openai_functions_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)
```

### 8.4 OpenAI Tools Agent

```python
from langchain.agents import create_openai_tools_agent

agent = create_openai_tools_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)
```

### 8.5 Agent 输出模式

```python
# stream_mode 参数
result = executor.stream(input, stream_mode="values")  # 完整状态
result = executor.stream(input, stream_mode="updates")  # 增量更新
result = executor.stream(input, stream_mode="messages")  # 消息流
result = executor.stream(input, stream_mode="debug")    # 调试信息
```

### 8.6 带记忆的 Agent

```python
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()
agent = create_react_agent(llm, tools, checkpointer=checkpointer)
result = agent.invoke(input, config={"configurable": {"thread_id": "123"}})
```

---

## 9. Tools 工具

### 9.1 工具类型

| 类型           | 说明       |
| -------------- | ---------- |
| @tool 装饰器   | 自定义工具 |
| StructuredTool | 结构化工具 |
| BaseTool       | 基础工具类 |
| Toolkits       | 工具包     |

### 9.2 @tool 装饰器

```python
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """查询城市天气"""
    return f"{city}天气晴朗"

@tool
def calculate(expression: str) -> str:
    """计算数学表达式"""
    return str(eval(expression))
```

### 9.3 StructuredTool

```python
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

class WeatherInput(BaseModel):
    city: str = Field(description="城市名称")

def get_weather(city: str) -> str:
    return f"{city}天气晴朗"

tool = StructuredTool.from_function(
    func=get_weather,
    name="weather",
    description="查询天气",
    args_schema=WeatherInput
)
```

### 9.4 BaseTool

```python
from langchain_core.tools import BaseTool

class CustomTool(BaseTool):
    name = "custom_tool"
    description = "自定义工具"

    def _run(self, query: str) -> str:
        return f"处理: {query}"

    async def _arun(self, query: str) -> str:
        return f"异步处理: {query}"
```

### 9.5 工具包 (Toolkits)

```python
from langchain_community.agent_toolkits import (
    SQLDatabaseToolkit,
    JsonToolkit,
    FileManagementToolkit,
    GmailToolkit,
)

# SQL 工具包
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()
```

### 9.6 内置工具

| 工具                | 说明         |
| ------------------- | ------------ |
| WikipediaQueryRun   | 维基百科查询 |
| DuckDuckGoSearchRun | 搜索         |
| ShellTool           | Shell 命令   |
| PythonREPL          | Python 执行  |
| RequestsToolkit     | HTTP 请求    |

---

## 10. Retrievers 检索器

### 10.1 检索器类型

| 类型                           | 说明           |
| ------------------------------ | -------------- |
| VectorStoreRetriever           | 向量检索       |
| BM25Retriever                  | BM25 检索      |
| EnsembleRetriever              | 集成检索       |
| MultiQueryRetriever            | 多查询检索     |
| SelfQueryRetriever             | 自查询检索     |
| ParentDocumentRetriever        | 父文档检索     |
| ContextualCompressionRetriever | 上下文压缩检索 |
| RePhraseQueryRetriever         | 重述查询检索   |
| WebResearchRetriever           | 网络研究检索   |
| ArxivRetriever                 | Arxiv 检索     |
| WikipediaRetriever             | 维基百科检索   |

### 10.2 VectorStoreRetriever

```python
retriever = vectorstore.as_retriever(
    search_type="similarity",  # similarity, mmr, similarity_score_threshold
    search_kwargs={"k": 4}
)
docs = retriever.invoke("查询")
```

### 10.3 BM25Retriever

```python
from langchain_community.retrievers import BM25Retriever

retriever = BM25Retriever.from_documents(docs)
retriever.k = 4
```

### 10.4 EnsembleRetriever

```python
from langchain.retrievers import EnsembleRetriever

retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.5, 0.5]
)
```

### 10.5 MultiQueryRetriever

```python
from langchain.retrievers import MultiQueryRetriever

retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(),
    llm=llm
)
```

### 10.6 SelfQueryRetriever

```python
from langchain.retrievers import SelfQueryRetriever

retriever = SelfQueryRetriever.from_llm(
    llm=llm,
    vectorstore=vectorstore,
    document_contents="...",
    metadata_field_info=metadata_field_info
)
```

### 10.7 ParentDocumentRetriever

```python
from langchain.retrievers import ParentDocumentRetriever

retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter
)
```

### 10.8 ContextualCompressionRetriever

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

compressor = LLMChainExtractor.from_llm(llm)
retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=base_retriever
)
```

---

## 11. Document Loaders 文档加载器

### 11.1 支持的格式

| 格式       | 加载器                        |
| ---------- | ----------------------------- |
| PDF        | PyPDFLoader, PDFPlumberLoader |
| CSV        | CSVLoader                     |
| JSON       | JSONLoader                    |
| TXT        | TextLoader                    |
| Markdown   | UnstructuredMarkdownLoader    |
| HTML       | UnstructuredHTMLLoader        |
| Word       | Docx2txtLoader                |
| Excel      | UnstructuredExcelLoader       |
| PowerPoint | UnstructuredPowerPointLoader  |
| Email      | UnstructuredEmailLoader       |
| Image      | UnstructuredImageLoader       |
| Audio      | OpenAIWhisperLoader           |
| Video      | YouTubeLoader                 |
| Web        | WebBaseLoader                 |
| Sitemap    | SitemapLoader                 |
| Git        | GitLoader                     |
| Notion     | NotionDirectoryLoader         |
| Obsidian   | ObsidianLoader                |

### 11.2 PDF 加载

```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("document.pdf")
docs = loader.load()
```

### 11.3 Web 加载

```python
from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://example.com")
docs = loader.load()
```

### 11.4 CSV 加载

```python
from langchain_community.document_loaders import CSVLoader

loader = CSVLoader("data.csv")
docs = loader.load()
```

### 11.5 目录加载

```python
from langchain_community.document_loaders import DirectoryLoader

loader = DirectoryLoader("./docs", glob="**/*.pdf")
docs = loader.load()
```

### 11.6 YouTube 加载

```python
from langchain_community.document_loaders import YouTubeLoader

loader = YouTubeLoader.from_youtube_url("https://youtube.com/watch?v=...")
docs = loader.load()
```

### 11.7 Git 加载

```python
from langchain_community.document_loaders import GitLoader

loader = GitLoader(repo_path="./repo", branch="main")
docs = loader.load()
```

---

## 12. Text Splitters 文本分割器

### 12.1 分割器类型

| 类型                                  | 说明            |
| ------------------------------------- | --------------- |
| RecursiveCharacterTextSplitter        | 递归字符分割    |
| CharacterTextSplitter                 | 字符分割        |
| TokenTextSplitter                     | Token 分割      |
| MarkdownTextSplitter                  | Markdown 分割   |
| HTMLHeaderTextSplitter                | HTML 标题分割   |
| PythonCodeTextSplitter                | Python 代码分割 |
| RecursiveJsonSplitter                 | JSON 分割       |
| NLTKTextSplitter                      | NLTK 句子分割   |
| SpacyTextSplitter                     | Spacy 句子分割  |
| SentenceTransformersTokenTextSplitter | 句子转换器分割  |

### 12.2 RecursiveCharacterTextSplitter（推荐）

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", "。", "！", "？", ".", " ", ""]
)
chunks = splitter.split_documents(docs)
```

### 12.3 Markdown 分割

```python
from langchain.text_splitter import MarkdownTextSplitter

splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=0)
chunks = splitter.split_text(markdown_text)
```

### 12.4 Token 分割

```python
from langchain.text_splitter import TokenTextSplitter

splitter = TokenTextSplitter(chunk_size=100, chunk_overlap=20)
chunks = splitter.split_text(text)
```

### 12.5 代码分割

```python
from langchain.text_splitter import PythonCodeTextSplitter

splitter = PythonCodeTextSplitter(chunk_size=1000, chunk_overlap=0)
chunks = splitter.split_text(python_code)
```

### 12.6 HTML 分割

```python
from langchain.text_splitter import HTMLHeaderTextSplitter

splitter = HTMLHeaderTextSplitter(
    headers_to_split_on=[("h1", "Header 1"), ("h2", "Header 2")]
)
chunks = splitter.split_text(html)
```

---

## 13. Vector Stores 向量数据库

### 13.1 支持的数据库

| 数据库        | 类型        |
| ------------- | ----------- |
| FAISS         | 本地        |
| Chroma        | 本地        |
| Pinecone      | 云          |
| Weaviate      | 云/自托管   |
| Qdrant        | 云/自托管   |
| Milvus        | 云/自托管   |
| PGVector      | PostgreSQL  |
| Redis         | 内存/持久化 |
| Elasticsearch | 云/自托管   |
| MongoDB Atlas | 云          |
| Supabase      | 云          |
| DuckDB        | 本地        |

### 13.2 FAISS

```python
from langchain_community.vectorstores import FAISS

vectorstore = FAISS.from_documents(docs, embeddings)
retriever = vectorstore.as_retriever()
```

### 13.3 Chroma

```python
from langchain_community.vectorstores import Chroma

vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory="./chroma_db"
)
```

### 13.4 Pinecone

```python
from langchain_community.vectorstores import Pinecone

vectorstore = Pinecone.from_documents(docs, embeddings, index_name="my-index")
```

### 13.5 Qdrant

```python
from langchain_community.vectorstores import Qdrant

vectorstore = Qdrant.from_documents(
    docs, embeddings,
    location=":memory:",
    collection_name="my-collection"
)
```

### 13.6 相似度搜索

```python
# 基础搜索
results = vectorstore.similarity_search("查询", k=4)

# 带分数搜索
results = vectorstore.similarity_search_with_score("查询", k=4)

# MMR 搜索（多样性）
results = vectorstore.max_marginal_relevance_search("查询", k=4)
```

### 13.7 持久化与加载

```python
# 保存
vectorstore.save_local("faiss_index")

# 加载
vectorstore = FAISS.load_local("faiss_index", embeddings)
```

---

## 14. Embeddings 嵌入模型

### 14.1 支持的模型

| 提供商         | 模型                                           |
| -------------- | ---------------------------------------------- |
| OpenAI         | text-embedding-3-small, text-embedding-3-large |
| HuggingFace    | sentence-transformers                          |
| Cohere         | embed-multilingual                             |
| Azure          | Azure OpenAI Embeddings                        |
| Ollama         | 本地嵌入模型                                   |
| FakeEmbeddings | 测试用                                         |

### 14.2 OpenAI Embeddings

```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector = embeddings.embed_query("你好")
vectors = embeddings.embed_documents(["你好", "世界"])
```

### 14.3 HuggingFace Embeddings

```python
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
vector = embeddings.embed_query("你好")
```

### 14.4 本地 Embeddings

```python
from langchain_community.embeddings import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="llama2")
vector = embeddings.embed_query("你好")
```

### 14.5 缓存 Embeddings

```python
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore

store = LocalFileStore("./cache/")
cached_embeddings = CacheBackedEmbeddings.from_bytes_store(
    embeddings, store, namespace=embeddings.model
)
```

---

## 15. Callbacks 回调系统

### 15.1 回调事件

| 事件               | 触发时机   |
| ------------------ | ---------- |
| on_llm_start       | LLM 开始   |
| on_llm_new_token   | 新 token   |
| on_llm_end         | LLM 结束   |
| on_llm_error       | LLM 错误   |
| on_chain_start     | Chain 开始 |
| on_chain_end       | Chain 结束 |
| on_chain_error     | Chain 错误 |
| on_tool_start      | 工具开始   |
| on_tool_end        | 工具结束   |
| on_tool_error      | 工具错误   |
| on_retriever_start | 检索开始   |
| on_retriever_end   | 检索结束   |

### 15.2 自定义回调

```python
from langchain_core.callbacks import BaseCallbackHandler

class MyCallback(BaseCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kwargs):
        print(f"LLM 开始: {prompts}")

    def on_llm_end(self, response, **kwargs):
        print(f"LLM 结束")

    def on_llm_new_token(self, token, **kwargs):
        print(token, end="")

    def on_llm_error(self, error, **kwargs):
        print(f"LLM 错误: {error}")
```

### 15.3 使用回调

```python
# 构造函数
llm = ChatOpenAI(callbacks=[MyCallback()])

# 调用时
result = llm.invoke("你好", config={"callbacks": [MyCallback()]})

# 全局配置
config = RunnableConfig(callbacks=[MyCallback()])
```

### 15.4 异步回调

```python
class AsyncCallback(BaseCallbackHandler):
    async def on_llm_start(self, serialized, prompts, **kwargs):
        await some_async_operation()
```

---

## 16. LCEL 表达式语言

### 16.1 核心概念

```
LCEL = LangChain Expression Language
使用 | 管道符组合组件
```

### 16.2 基础用法

```python
chain = prompt | llm | output_parser
result = chain.invoke({"input": "你好"})
```

### 16.3 批量处理

```python
results = chain.batch([{"input": "你好"}, {"input": "世界"}])
```

### 16.4 流式输出

```python
for chunk in chain.stream({"input": "你好"}):
    print(chunk, end="")
```

### 16.5 异步调用

```python
result = await chain.ainvoke({"input": "你好"})
```

### 16.6 链的组合

```python
# 顺序
chain = step1 | step2 | step3

# 并行
parallel = RunnableParallel(a=chain1, b=chain2)

# 分支
branch = RunnableBranch(
    (condition1, chain1),
    (condition2, chain2),
    default_chain
)
```

---

## 17. Runnables 可运行组件

### 17.1 Runnable 接口

| 方法           | 说明       |
| -------------- | ---------- |
| invoke         | 同步调用   |
| ainvoke        | 异步调用   |
| batch          | 批量处理   |
| abatch         | 异步批量   |
| stream         | 流式输出   |
| astream        | 异步流式   |
| astream_events | 异步事件流 |

### 17.2 RunnablePassthrough

```python
from langchain_core.runnables import RunnablePassthrough

passthrough = RunnablePassthrough()
result = passthrough.invoke("hello")  # 返回 "hello"
```

### 17.3 RunnableLambda

```python
from langchain_core.runnables import RunnableLambda

def process(text):
    return text.upper()

runnable = RunnableLambda(process)
result = runnable.invoke("hello")  # 返回 "HELLO"
```

### 17.4 RunnableParallel

```python
from langchain_core.runnables import RunnableParallel

parallel = RunnableParallel(
    summary=summary_chain,
    keywords=keywords_chain
)
result = parallel.invoke({"text": "..."})
```

### 17.5 RunnableBranch

```python
from langchain_core.runnables import RunnableBranch

branch = RunnableBranch(
    (lambda x: len(x) > 100, long_chain),
    (lambda x: len(x) > 50, medium_chain),
    short_chain
)
```

### 17.6 RunnableSequence

```python
from langchain_core.runnables import RunnableSequence

sequence = RunnableSequence(first, middle, last)
```

### 17.7 RunnableConfig

```python
from langchain_core.runnables import RunnableConfig

config = RunnableConfig(
    callbacks=[callback],
    max_concurrency=5,
    run_name="my_chain",
    tags=["production"],
    metadata={"version": "1.0"}
)
```

### 17.8 RunnableWithFallbacks

```python
chain_with_fallback = primary_chain.with_fallbacks([fallback_chain])
```

### 17.9 RunnableRetry

```python
chain_with_retry = chain.with_retry(
    stop_after_attempt=3,
    wait_exponential_jitter=True
)
```

---

## 18. Indexing 索引系统

### 18.1 索引 API

```python
from langchain.indexes import index, IndexingResult

result = index(
    docs_source=loader,
    record_manager=record_manager,
    vector_store=vectorstore,
    cleanup="incremental",  # full, incremental, None
    source_id_key="source"
)
```

### 18.2 RecordManager

```python
from langchain.indexes import SQLRecordManager

record_manager = SQLRecordManager(
    namespace="my_collection",
    db_url="sqlite:///record_manager.db"
)
record_manager.create_schema()
```

### 18.3 增量索引

```python
# 首次索引
result = index(docs, record_manager, vectorstore, cleanup=None)

# 增量更新
result = index(docs, record_manager, vectorstore, cleanup="incremental")
```

---

## 19. Evaluation 评估系统

### 19.1 评估类型

| 类型                    | 说明           |
| ----------------------- | -------------- |
| StringEvaluator         | 字符串评估     |
| TrajectoryEvaluator     | 轨迹评估       |
| ComparisonEvaluator     | 比较评估       |
| PairwiseStringEvaluator | 成对字符串评估 |

### 19.2 内置评估器

| 评估器                  | 说明           |
| ----------------------- | -------------- |
| ExactMatch              | 精确匹配       |
| StringDistance          | 字符串距离     |
| RegexMatch              | 正则匹配       |
| LLMEvalChain            | LLM 评估       |
| QAEvalChain             | QA 评估        |
| ContextQAEvalChain      | 上下文 QA 评估 |
| CriteriaEvalChain       | 标准评估       |
| PairwiseStringEvalChain | 成对评估       |
| EmbeddingDistance       | 嵌入距离       |

### 19.3 LLM 评估

```python
from langchain.evaluation import load_evaluator

evaluator = load_evaluator("criteria", criteria="helpfulness", llm=llm)
result = evaluator.evaluate_strings(
    prediction="...",
    reference="...",
    input="..."
)
```

### 19.4 QA 评估

```python
from langchain.evaluation import QAEvalChain

chain = QAEvalChain.from_llm(llm)
results = chain.evaluate(examples, predictions)
```

### 19.5 自定义评估器

```python
from langchain.evaluation import StringEvaluator

class CustomEvaluator(StringEvaluator):
    def _evaluate_strings(self, prediction, reference=None, input=None, **kwargs):
        # 自定义评估逻辑
        return {"score": 1.0, "reasoning": "..."}
```

---

## 20. Tracing 追踪系统

### 20.1 LangSmith 集成

```python
import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-api-key"
os.environ["LANGCHAIN_PROJECT"] = "my-project"
```

### 20.2 自动追踪

所有 LangChain 调用都会自动追踪

### 20.3 手动追踪

```python
from langchain_core.tracers import LangChainTracer

tracer = LangChainTracer(project_name="my-project")
result = llm.invoke("你好", config={"callbacks": [tracer]})
```

### 20.4 追踪上下文

```python
from langchain_core.runnables import RunnableConfig

config = RunnableConfig(
    run_name="my_run",
    tags=["test"],
    metadata={"version": "1.0"}
)
```

---

## 21. Caching 缓存机制

### 21.1 缓存类型

| 类型               | 说明            |
| ------------------ | --------------- |
| InMemoryCache      | 内存缓存        |
| SQLiteCache        | SQLite 缓存     |
| RedisCache         | Redis 缓存      |
| MomentoCache       | Momento 缓存    |
| GPTCache           | GPT 缓存        |
| CassandraCache     | Cassandra 缓存  |
| SQLAlchemyCache    | SQLAlchemy 缓存 |
| RedisSemanticCache | 语义缓存        |

### 21.2 内存缓存

```python
from langchain_core.globals import set_llm_cache
from langchain_core.caches import InMemoryCache

set_llm_cache(InMemoryCache())
```

### 21.3 SQLite 缓存

```python
from langchain_community.cache import SQLiteCache

set_llm_cache(SQLiteCache(database_path=".langchain.db"))
```

### 21.4 Redis 缓存

```python
from langchain_community.cache import RedisCache
import redis

set_llm_cache(RedisCache(redis.Redis()))
```

### 21.5 语义缓存

```python
from langchain_community.cache import RedisSemanticCache

set_llm_cache(RedisSemanticCache(
    redis_url="redis://localhost:6379",
    embedding=embeddings,
    score_threshold=0.2
))
```

### 21.6 自定义缓存

```python
from langchain_core.caches import BaseCache

class CustomCache(BaseCache):
    def lookup(self, prompt, llm_string):
        ...
    def update(self, prompt, llm_string, return_val):
        ...
    def clear(self):
        ...
```

---

## 22. Streaming 流式处理

### 22.1 基础流式

```python
for chunk in llm.stream("写一首诗"):
    print(chunk.content, end="")
```

### 22.2 链式流式

```python
chain = prompt | llm | StrOutputParser()
for chunk in chain.stream({"topic": "春天"}):
    print(chunk, end="")
```

### 22.3 异步流式

```python
async for chunk in llm.astream("写一首诗"):
    print(chunk.content, end="")
```

### 22.4 事件流

```python
async for event in chain.astream_events(input, version="v2"):
    if event["event"] == "on_chat_model_stream":
        print(event["data"]["chunk"].content, end="")
```

### 22.5 Agent 流式

```python
for state in agent.stream(input, stream_mode="values"):
    print(state["messages"][-1].content)
```

---

## 23. Structured Output 结构化输出

### 23.1 with_structured_output

```python
from pydantic import BaseModel

class Answer(BaseModel):
    answer: str
    confidence: float

structured_llm = llm.with_structured_output(Answer)
result = structured_llm.invoke("什么是AI？")
```

### 23.2 Pydantic 输出

```python
from langchain_core.output_parsers import PydanticOutputParser

parser = PydanticOutputParser(pydantic_object=Answer)
chain = prompt | llm | parser
```

### 23.3 JSON 输出

```python
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser(pydantic_object=Answer)
chain = prompt | llm | parser
```

### 23.4 工具调用输出

```python
structured_llm = llm.bind_tools([tool1, tool2])
response = structured_llm.invoke("查询天气")
```

---

## 24. Multi-modal 多模态

### 24.1 图片输入

```python
from langchain_core.messages import HumanMessage

message = HumanMessage(content=[
    {"type": "text", "text": "描述这张图片"},
    {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,..."}}
])
response = llm.invoke([message])
```

### 24.2 图片 URL

```python
message = HumanMessage(content=[
    {"type": "text", "text": "描述这张图片"},
    {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}}
])
```

### 24.3 本地图片

```python
import base64

with open("image.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

message = HumanMessage(content=[
    {"type": "text", "text": "描述这张图片"},
    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
])
```

### 24.4 多图片

```python
message = HumanMessage(content=[
    {"type": "text", "text": "对比这两张图片"},
    {"type": "image_url", "image_url": {"url": "url1"}},
    {"type": "image_url", "image_url": {"url": "url2"}}
])
```

---

## 25. LangGraph 图状态机

### 25.1 核心概念

```
LangGraph = 有状态的多Actor应用框架
基于图的状态机，支持循环和条件分支
```

### 25.2 基础用法

```python
from langgraph.graph import StateGraph, END

class State(TypedDict):
    messages: list

def node(state):
    return {"messages": [...]}

graph = StateGraph(State)
graph.add_node("agent", node)
graph.add_edge("agent", END)
graph.set_entry_point("agent")

app = graph.compile()
result = app.invoke({"messages": [...]})
```

### 25.3 条件边

```python
def should_continue(state):
    return "continue" if condition else "end"

graph.add_conditional_edges("agent", should_continue, {
    "continue": "tools",
    "end": END
})
```

### 25.4 带工具的 Agent

```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(llm, tools)
result = agent.invoke({"messages": [("human", "...")]})
```

### 25.5 检查点

```python
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()
app = graph.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "123"}}
result = app.invoke(input, config=config)
```

### 25.6 持久化

```python
from langgraph.checkpoint.sqlite import SqliteSaver

checkpointer = SqliteSaver.from_conn_string(":memory:")
app = graph.compile(checkpointer=checkpointer)
```

---

## 26. LangSmith 监控平台

### 26.1 功能

- 调用追踪
- 性能监控
- 评估测试
- 数据集管理
- 提示词管理

### 26.2 配置

```python
import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-api-key"
os.environ["LANGCHAIN_PROJECT"] = "my-project"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
```

### 26.3 手动追踪

```python
from langsmith import Client

client = Client()
run = client.create_run(
    project_name="my-project",
    name="my_run",
    run_type="chain",
    inputs={"input": "..."}
)
```

### 26.4 评估

```python
from langsmith import Client

client = Client()
results = client.run_on_dataset(
    dataset_name="my-dataset",
    llm_or_chain=chain,
    evaluation=eval_config
)
```

---

## 27. 部署与生产

### 27.1 LangServe

```python
from fastapi import FastAPI
from langserve import add_routes

app = FastAPI()
add_routes(app, chain, path="/chain")

# 启动
# uvicorn app:app --host 0.0.0.0 --port 8000
```

### 27.2 客户端调用

```python
from langserve import RemoteRunnable

chain = RemoteRunnable("http://localhost:8000/chain/")
result = chain.invoke({"input": "你好"})
```

### 27.3 流式调用

```python
for chunk in chain.stream({"input": "你好"}):
    print(chunk, end="")
```

### 27.4 生产最佳实践

1. **缓存**: 使用 Redis 或语义缓存
2. **重试**: 配置重试策略
3. **超时**: 设置合理超时
4. **监控**: 启用 LangSmith
5. **日志**: 使用回调记录日志
6. **限流**: 控制请求频率
7. **降级**: 配置 fallback 模型
8. **安全**: 验证输入输出

---

## 知识点速查表

| 类别   | 核心组件                                                |
| ------ | ------------------------------------------------------- |
| 模型   | OpenAI, Anthropic, Google, HuggingFace                  |
| 提示词 | PromptTemplate, ChatPromptTemplate, FewShot             |
| 解析器 | StrOutputParser, JsonOutputParser, PydanticOutputParser |
| 链     | LCEL, SequentialChain, RetrievalQA                      |
| 记忆   | BufferMemory, SummaryMemory, EntityMemory               |
| 代理   | ReAct Agent, OpenAI Agent, Plan-and-Execute             |
| 工具   | @tool, StructuredTool, Toolkits                         |
| 检索   | VectorRetriever, BM25, MultiQuery, SelfQuery            |
| 加载器 | PDF, CSV, JSON, Web, YouTube                            |
| 分割器 | RecursiveCharacter, Token, Markdown                     |
| 向量库 | FAISS, Chroma, Pinecone, Qdrant                         |
| 嵌入   | OpenAI, HuggingFace, Cohere                             |
| 回调   | BaseCallbackHandler                                     |
| 缓存   | InMemory, Redis, SQLite, Semantic                       |
| 评估   | LLM Eval, QA Eval, Criteria Eval                        |
| 追踪   | LangSmith                                               |
| 部署   | LangServe, LangGraph                                    |

---

## 学习路径

### 入门阶段

1. LLMs 和 Chat Models
2. Prompt Templates
3. Output Parsers
4. Chains (LCEL)

### 进阶阶段

5. Memory 系统
6. Agents 和 Tools
7. Document Loaders
8. Text Splitters

### 高级阶段

9. Vector Stores 和 Embeddings
10. Retrievers
11. LangGraph
12. 评估和追踪

### 生产阶段

13. 缓存优化
14. 流式处理
15. 部署 (LangServe)
16. 监控 (LangSmith)
