import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { useEffect, useState } from 'react'
import Sidebar from './components/Sidebar'
import Dashboard from './pages/Dashboard'
import Keys from './pages/Keys'
import Login from './pages/Login'
import { setApiKey, validateApiKey } from './api/client'

function App() {
  const [authed, setAuthed] = useState(false)

  useEffect(() => {
    const cached = sessionStorage.getItem('conduit_key')
    if (cached) {
      validateApiKey(cached).then(valid => {
        if (valid) {
          setApiKey(cached)
          setAuthed(true)
        } else {
          sessionStorage.removeItem('conduit_key')
        }
      })
    }
  }, [])

  const handleLogin = (key: string) => {
    setApiKey(key)
    sessionStorage.setItem('conduit_key', key)
    setAuthed(true)
  }

  if (!authed) {
    return <Login onLogin={handleLogin} />
  }

  return (
    <BrowserRouter>
      <div style={{ display: 'flex', minHeight: '100vh' }}>
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