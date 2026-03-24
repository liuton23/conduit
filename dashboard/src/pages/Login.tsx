import { useState } from 'react'
import { login, register } from '../api/client'

interface Props {
  onLogin: () => void
  isRegistered: boolean
}

interface PasswordRequirement {
  label: string
  met: boolean
}

function getPasswordRequirements(password: string): PasswordRequirement[] {
  return [
    { label: '8+ characters', met: password.length >= 8 },
    { label: 'Uppercase letter', met: /[A-Z]/.test(password) },
    { label: 'Lowercase letter', met: /[a-z]/.test(password) },
    { label: 'Number', met: /[0-9]/.test(password) },
    { label: 'Special character', met: /[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]/.test(password) },
  ]
}

function Login({ onLogin, isRegistered }: Props) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const requirements = getPasswordRequirements(password)
  const allMet = requirements.every(r => r.met)
  const passwordsMatch = password === confirmPassword && confirmPassword.length > 0

  const handleSubmit = async () => {
    if (!email || !password) return
    if (!isRegistered && !allMet) return
    if (!isRegistered && !passwordsMatch) return

    setLoading(true)
    setError('')

    try {
      if (isRegistered) {
        await login(email, password)
      } else {
        await register(email, password)
      }
      onLogin()
    } catch (err: any) {
      const detail = err?.response?.data?.detail
      if (Array.isArray(detail)) {
        setError(detail.join(', '))
      } else {
        setError(detail || (isRegistered ? 'Invalid email or password' : 'Registration failed'))
      }
    }

    setLoading(false)
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <h1>Conduit</h1>
        <p className="login-subtitle">
          {isRegistered ? 'Sign in to your account' : 'Create your account to get started'}
        </p>

        <input
          className={`login-input ${error ? 'error' : ''}`}
          type="email"
          placeholder="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleSubmit()}
        />

        <input
          className={`login-input ${error ? 'error' : ''}`}
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleSubmit()}
        />

        {/* everything below spawns after user starts typing password */}
        {!isRegistered && password.length > 0 && (
          <>
            <input
              className={`login-input ${confirmPassword.length > 0 && !passwordsMatch ? 'error' : ''}`}
              type="password"
              placeholder="Confirm password"
              value={confirmPassword}
              onChange={e => setConfirmPassword(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleSubmit()}
            />

            {confirmPassword.length > 0 && !passwordsMatch && (
              <p className="login-error">Passwords do not match</p>
            )}

            <div className="password-requirements">
              {requirements.map(req => (
                <div key={req.label} className={`password-req ${req.met ? 'met' : 'unmet'}`}>
                  <span>{req.met ? '✓' : '✗'}</span>
                  <span>{req.label}</span>
                </div>
              ))}
            </div>
          </>
        )}

        {error && <p className="login-error">{error}</p>}

        <button
          className="login-btn"
          onClick={handleSubmit}
          disabled={loading || (!isRegistered && (!allMet || !passwordsMatch))}
        >
          {loading
            ? (isRegistered ? 'Signing in...' : 'Creating account...')
            : (isRegistered ? 'Sign in' : 'Create account')
          }
        </button>
      </div>
    </div>
  )
}

export default Login