import { ChatInterface } from './components/ChatInterface'

function App() {
  return (
    <div className="min-h-screen w-screen bg-slate-950 flex flex-col items-center justify-center p-4 md:p-8">
      <header className="mb-8 text-center">
        <h1 className="text-4xl font-black text-white tracking-tighter mb-2">
          INDI<span className="text-indigo-500">GO</span> <span className="font-light text-slate-400">OPERATIONS COPIOT</span>
        </h1>
        <p className="text-slate-500 text-sm font-medium tracking-widest uppercase">Enterprise AI Operations Platform</p>
      </header>
      
      <main className="w-full max-w-6xl flex-1 flex flex-col">
        <ChatInterface />
      </main>
      
      <footer className="mt-8 text-slate-700 text-[10px] font-bold uppercase tracking-[0.2em]">
        StatusNeo x IndiGo AI Hackathon 2026
      </footer>
    </div>
  )
}

export default App
