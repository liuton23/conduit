import { NavLink } from 'react-router-dom'
import { logout } from '../api/client'

const links = [
  { to: '/', label: '📊 Dashboard' },
  { to: '/keys', label: '🔑 API Keys' },
]

function Sidebar() {
  const handleLogout = async () => {
    await logout()
    window.location.reload()
  }

  return (
    <div style={{
      width: '220px',
      minHeight: '100vh',
      background: '#141414',
      borderRight: '1px solid #2a2a2a',
      padding: '24px 16px',
      display: 'flex',
      flexDirection: 'column',
      gap: '8px',
    }}>
      <p style={{
        fontSize: '18px',
        fontWeight: '700',
        marginBottom: '24px',
        paddingLeft: '12px'
      }}>
        Conduit
      </p>
      {links.map(link => (
        <NavLink
          key={link.to}
          to={link.to}
          end
          style={({ isActive }) => ({
            display: 'block',
            padding: '10px 12px',
            borderRadius: '6px',
            textDecoration: 'none',
            color: isActive ? '#fff' : '#888',
            background: isActive ? '#2a2a2a' : 'transparent',
            fontSize: '14px',
          })}
        >
          {link.label}
        </NavLink>
      ))}

      {/* logout at bottom */}
      <div style={{ marginTop: 'auto' }}>
        <button
          onClick={handleLogout}
          style={{
            width: '100%',
            background: 'transparent',
            border: '1px solid #2a2a2a',
            borderRadius: '6px',
            padding: '10px 12px',
            color: '#888',
            fontSize: '14px',
            cursor: 'pointer',
            textAlign: 'left',
          }}
        >
          🚪 Logout
        </button>
      </div>
    </div>
  )
}

export default Sidebar