import { useState } from 'react'
import { login, register } from '../api/client'

interface Props {
  onLogin: () => void
  isRegistered: boolean
}

function Login({ onLogin, isRegistered }: Props) {
  const [accessKey, setAccessKey] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async () => {
    if (!accessKey) return
    setLoading(true)
    setError('')

    try {
      if (isRegistered) {
        await login(accessKey)
      } else {
        await register(accessKey)
      }
      onLogin()
    } catch {
      setError(isRegistered ? 'Invalid access key' : 'Registration failed')
    }

    setLoading(false)
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <h1>Conduit</h1>
        <p className="login-subtitle">
          {isRegistered
            ? 'Enter your access key to continue'
            : 'Create an access key to get started'
          }
        </p>

        <input
          className={`login-input ${error ? 'error' : ''}`}
          type="password"
          placeholder="Access key"
          value={accessKey}
          onChange={e => setAccessKey(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleSubmit()}
        />

        {!isRegistered && (
          <p style={{ color: '#888', fontSize: '12px', marginBottom: '8px' }}>
            Minimum 8 characters. Store this safely — you'll need it to log in.
          </p>
        )}

        {error && <p className="login-error">{error}</p>}

        <button
          className="login-btn"
          onClick={handleSubmit}
          disabled={loading}
        >
          {loading
            ? (isRegistered ? 'Signing in...' : 'Creating...')
            : (isRegistered ? 'Sign in' : 'Create access key')
          }
        </button>
      </div>
    </div>
  )
}

export default Login