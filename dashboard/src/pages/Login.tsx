import { useState } from 'react'
import { validateApiKey } from '../api/client'
import client from '../api/client'
import './Login.css'

interface Props {
  onLogin: (key: string) => void
}

function Login({ onLogin }: Props) {
  const [view, setView] = useState<'login' | 'create'>('login')
  const [key, setKey] = useState('')
  const [name, setName] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [newKey, setNewKey] = useState('')

  const handleLogin = async () => {
    if (!key) return
    setLoading(true)
    setError('')
    const valid = await validateApiKey(key)
    if (!valid) {
      setError('Invalid or revoked API key')
      setLoading(false)
      return
    }
    onLogin(key)
    setLoading(false)
  }

  const handleCreate = async () => {
    if (!name) return
    setLoading(true)
    setError('')
    try {
      const res = await client.post('/keys', { name })
      setNewKey(res.data.key)
    } catch {
      setError('Failed to create key')
    }
    setLoading(false)
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <h1>Conduit</h1>

        <div className="login-tabs">
          <button
            className={`login-tab ${view === 'login' ? 'active' : ''}`}
            onClick={() => { setView('login'); setError('') }}
          >
            Sign in
          </button>
          <button
            className={`login-tab ${view === 'create' ? 'active' : ''}`}
            onClick={() => { setView('create'); setError('') }}
          >
            Create key
          </button>
        </div>

        {view === 'login' && (
          <>
            <p className="login-subtitle">Enter your API key to continue</p>
            <input
              className={`login-input ${error ? 'error' : ''}`}
              type="password"
              placeholder="cdt-..."
              value={key}
              onChange={e => setKey(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleLogin()}
            />
            {error && <p className="login-error">{error}</p>}
            <button className="login-btn" onClick={handleLogin} disabled={loading}>
              {loading ? 'Validating...' : 'Continue'}
            </button>
          </>
        )}

        {view === 'create' && (
          <>
            <p className="login-subtitle">Create your first API key to get started</p>

            {!newKey ? (
              <>
                <input
                  className={`login-input ${error ? 'error' : ''}`}
                  placeholder="Key name (e.g. my-app)"
                  value={name}
                  onChange={e => setName(e.target.value)}
                  onKeyDown={e => e.key === 'Enter' && handleCreate()}
                />
                {error && <p className="login-error">{error}</p>}
                <button className="login-btn" onClick={handleCreate} disabled={loading}>
                  {loading ? 'Creating...' : 'Create Key'}
                </button>
              </>
            ) : (
              <>
                <p className="login-subtitle">
                  Your key has been created. Copy it now — it won't be shown again.
                </p>
                <div className="new-key-banner">{newKey}</div>
                <button className="login-btn" onClick={() => onLogin(newKey)}>
                  Continue to Dashboard
                </button>
              </>
            )}
          </>
        )}
      </div>
    </div>
  )
}

export default Login