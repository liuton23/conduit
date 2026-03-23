import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './styles/global.css'
import './styles/layout.css'
import './styles/components.css'
import './styles/pages/dashboard.css'
import './styles/pages/keys.css'
import './styles/pages/login.css'
import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)