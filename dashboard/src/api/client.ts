import axios from 'axios'

const client = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true,
})

export const getAuthStatus = async (): Promise<{ registered: boolean }> => {
  const res = await client.get('/auth/status')
  return res.data
}

export const register = async (email: string, password: string): Promise<void> => {
  await client.post('/auth/register', { email, password })
}

export const login = async (email: string, password: string): Promise<void> => {
  await client.post('/auth/login', { email, password })
}

export const logout = async (): Promise<void> => {
  await client.post('/auth/logout')
}

export const verifySession = async (): Promise<boolean> => {
  try {
    await client.get('/auth/verify')
    return true
  } catch {
    return false
  }
}

export default client