import { useState, useRef, useEffect } from 'react'
import { PaperAirplaneIcon } from '@heroicons/react/24/solid'

function InputBox({ onSend, isLoading }) {
  const [input, setInput] = useState('')
  const inputRef = useRef(null)

  // 自动聚焦
  useEffect(() => {
    inputRef.current?.focus()
  }, [])

  // 发送消息
  const handleSend = () => {
    if (input.trim() && !isLoading) {
      onSend(input)
      setInput('')
    }
  }

  // 回车发送
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  // 自动调整高度
  const handleInput = (e) => {
    setInput(e.target.value)
    e.target.style.height = 'auto'
    e.target.style.height = Math.min(e.target.scrollHeight, 150) + 'px'
  }

  return (
    <footer className="chat-input">
      <div className="input-wrapper">
        <textarea
          ref={inputRef}
          value={input}
          onChange={handleInput}
          onKeyDown={handleKeyDown}
          placeholder="输入您的旅行需求... (Enter 发送，Shift+Enter 换行)"
          className="input-field"
          rows={1}
          disabled={isLoading}
        />
        <button
          onClick={handleSend}
          disabled={!input.trim() || isLoading}
          className="send-button"
        >
          {isLoading ? (
            <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
          ) : (
            <PaperAirplaneIcon className="w-5 h-5" />
          )}
        </button>
      </div>
      <p className="text-xs text-gray-400 text-center mt-2 max-w-3xl mx-auto">
        旅游助手可以帮你规划行程、查询天气、推荐景点和美食
      </p>
    </footer>
  )
}

export default InputBox
