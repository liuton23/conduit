import { NavLink } from 'react-router-dom'
import { LayoutDashboard, Key, LogOut } from 'lucide-react'
import { logout } from '../api/client'

const links = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/keys', label: 'API Keys', icon: Key },
]

function Sidebar() {
  const handleLogout = async () => {
    await logout()
    window.location.reload()
  }

  return (
    <div className="sidebar">
      <p className="sidebar-title">Conduit</p>
      {links.map(link => (
        <NavLink
          key={link.to}
          to={link.to}
          end
          className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}
        >
          <link.icon size={16} />
          {link.label}
        </NavLink>
      ))}
      <div className="sidebar-bottom">
        <button className="sidebar-logout" onClick={handleLogout}>
          <LogOut size={16} />
          Logout
        </button>
      </div>
    </div>
  )
}

export default Sidebar