import { TrashIcon, GlobeAltIcon } from '@heroicons/react/24/outline'

function Header({ onClear, messageCount }) {
  return (
    <header className="chat-header">
      <div className="flex items-center justify-between max-w-3xl mx-auto">
        <div className="flex items-center gap-3">
          <GlobeAltIcon className="w-8 h-8 text-blue-500" />
          <div>
            <h1 className="text-xl font-bold text-gray-800">旅游助手</h1>
            <p className="text-sm text-gray-500">
              {messageCount > 0 ? `已对话 ${messageCount} 条` : '智能规划您的旅行'}
            </p>
          </div>
        </div>
        <button
          onClick={onClear}
          className="clear-button flex items-center gap-1 text-sm"
          title="清空对话"
        >
          <TrashIcon className="w-4 h-4" />
          <span>清空</span>
        </button>
      </div>
    </header>
  )
}

export default Header
