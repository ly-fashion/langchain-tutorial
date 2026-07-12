import { marked } from 'marked'

// 配置 marked
marked.setOptions({
  breaks: true,
  gfm: true,
})

function Message({ message }) {
  const isUser = message.role === 'user'

  // 简单的 Markdown 渲染
  const renderContent = (content) => {
    if (!content) return null

    try {
      const html = marked.parse(content)
      return <div className="markdown-content" dangerouslySetInnerHTML={{ __html: html }} />
    } catch {
      return <div>{content}</div>
    }
  }

  return (
    <div className={`message ${isUser ? 'message-user' : 'message-assistant'}`}>
      <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm flex-shrink-0 ${
        isUser ? 'bg-blue-500 text-white' : 'bg-gray-200'
      }`}>
        {isUser ? '👤' : '🤖'}
      </div>
      <div className={`message-bubble ${isUser ? 'message-bubble-user' : 'message-bubble-assistant'}`}>
        {isUser ? (
          <div className="whitespace-pre-wrap">{message.content}</div>
        ) : (
          renderContent(message.content)
        )}
      </div>
    </div>
  )
}

export default Message
