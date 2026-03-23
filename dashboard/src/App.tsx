import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { useState, useEffect } from 'react'
import Sidebar from './components/Sidebar'
import Dashboard from './pages/Dashboard'
import Keys from './pages/Keys'
import Login from './pages/Login'
import { getAuthStatus, verifySession } from './api/client'

function App() {
  const [authed, setAuthed] = useState(false)
  const [isRegistered, setIsRegistered] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const init = async () => {
      const [status, sessionValid] = await Promise.all([
        getAuthStatus(),
        verifySession()
      ])
      setIsRegistered(status.registered)
      setAuthed(sessionValid)
      setLoading(false)
    }
    init()
  }, [])

  if (loading) {
    return (
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        background: '#0f0f0f',
        color: '#888',
        fontSize: '14px'
      }}>
        Loading...
      </div>
    )
  }

  if (!authed) {
    return (
      <Login
        onLogin={() => setAuthed(true)}
        isRegistered={isRegistered}
      />
    )
  }
  return (
    <BrowserRouter>
      <div className="app">
        <Sidebar />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/keys" element={<Keys />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App