import { useState, useRef, useEffect } from 'react'
import ChatBox from './components/ChatBox'
import InputBox from './components/InputBox'
import Header from './components/Header'
import './index.css'

function App() {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const messagesEndRef = useRef(null)

  // 滚动到底部
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // 发送消息（流式）
  const sendMessage = async (content) => {
    if (!content.trim() || isLoading) return

    // 添加用户消息
    const userMessage = { role: 'user', content }
    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)
    setError(null)

    // 添加助手消息占位
    const assistantMessage = { role: 'assistant', content: '' }
    setMessages(prev => [...prev, assistantMessage])

    try {
      const response = await fetch('/api/chat/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: content, stream: true }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6))
              if (data.content) {
                setMessages(prev => {
                  const newMessages = [...prev]
                  const lastMessage = newMessages[newMessages.length - 1]
                  lastMessage.content += data.content
                  return newMessages
                })
              }
            } catch (e) {
              // 忽略解析错误
            }
          }
        }
      }
    } catch (err) {
      setError(err.message)
      setMessages(prev => {
        const newMessages = [...prev]
        const lastMessage = newMessages[newMessages.length - 1]
        lastMessage.content = `抱歉，发生了错误：${err.message}`
        return newMessages
      })
    } finally {
      setIsLoading(false)
    }
  }

  // 清空对话
  const clearChat = async () => {
    try {
      await fetch('/api/clear', { method: 'POST' })
      setMessages([])
      setError(null)
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="chat-container">
      <Header onClear={clearChat} messageCount={messages.length} />
      <ChatBox messages={messages} isLoading={isLoading} messagesEndRef={messagesEndRef} />
      <InputBox onSend={sendMessage} isLoading={isLoading} />
    </div>
  )
}

export default App
