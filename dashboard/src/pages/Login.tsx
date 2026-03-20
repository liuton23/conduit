import { useState } from 'react'
import { validateApiKey } from '../api/client'

interface Props {
  onLogin: (key: string) => void
}

function Login({ onLogin }: Props) {
  const [key, setKey] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async () => {
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

  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '100vh',
      background: '#0f0f0f',
    }}>
      <div style={{
        background: '#1a1a1a',
        border: '1px solid #2a2a2a',
        borderRadius: '12px',
        padding: '40px',
        width: '400px',
      }}>
        <h1 style={{ fontSize: '22px', marginBottom: '8px' }}>Conduit</h1>
        <p style={{ color: '#888', fontSize: '14px', marginBottom: '24px' }}>
          Enter your API key to continue
        </p>
        <input
          type="password"
          placeholder="cdt-..."
          value={key}
          onChange={e => setKey(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleSubmit()}
          style={{
            width: '100%',
            background: '#0f0f0f',
            border: `1px solid ${error ? '#ef4444' : '#2a2a2a'}`,
            borderRadius: '6px',
            padding: '10px 12px',
            color: '#f0f0f0',
            fontSize: '14px',
            marginBottom: '8px',
            boxSizing: 'border-box',
          }}
        />
        {error && (
          <p style={{ color: '#ef4444', fontSize: '13px', marginBottom: '12px' }}>
            {error}
          </p>
        )}
        <button
          onClick={handleSubmit}
          disabled={loading}
          style={{
            width: '100%',
            background: loading ? '#4a4a4a' : '#6366f1',
            border: 'none',
            borderRadius: '6px',
            padding: '10px',
            color: '#fff',
            fontSize: '14px',
            cursor: loading ? 'not-allowed' : 'pointer',
            marginTop: '4px',
          }}
        >
          {loading ? 'Validating...' : 'Continue'}
        </button>
      </div>
    </div>
  )
}

export default Login