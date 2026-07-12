import Message from './Message'

function ChatBox({ messages, isLoading, messagesEndRef }) {
  return (
    <main className="chat-messages">
      {messages.length === 0 && (
        <div className="flex flex-col items-center justify-center h-full text-gray-400">
          <div className="text-6xl mb-4">🌍</div>
          <h2 className="text-xl font-medium mb-2">欢迎使用旅游助手</h2>
          <p className="text-sm">我可以帮你规划行程、查询天气、推荐景点...</p>
          <div className="mt-6 grid grid-cols-2 gap-3 max-w-sm">
            {[
              { icon: '🗺️', text: '北京有什么好玩的？' },
              { icon: '🌤️', text: '上海天气怎么样？' },
              { icon: '📋', text: '帮我规划成都3日游' },
              { icon: '💰', text: '去杭州需要多少钱？' },
            ].map((item, i) => (
              <div
                key={i}
                className="bg-white rounded-lg p-3 text-sm text-gray-600 border hover:border-blue-300 cursor-pointer transition-colors"
              >
                <span className="mr-2">{item.icon}</span>
                {item.text}
              </div>
            ))}
          </div>
        </div>
      )}

      {messages.map((message, index) => (
        <Message key={index} message={message} />
      ))}

      {isLoading && messages[messages.length - 1]?.content === '' && (
        <div className="flex gap-3 max-w-3xl mr-auto">
          <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white text-sm">
            🤖
          </div>
          <div className="message-bubble message-bubble-assistant">
            <div className="typing-indicator">
              <div className="typing-dot"></div>
              <div className="typing-dot"></div>
              <div className="typing-dot"></div>
            </div>
          </div>
        </div>
      )}

      <div ref={messagesEndRef} />
    </main>
  )
}

export default ChatBox
