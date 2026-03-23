import axios from 'axios'

const client = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true, // important — sends cookies with every request
})

export const setApiKey = (key: string) => {
  client.defaults.headers.common['Authorization'] = `Bearer ${key}`
}

export const validateApiKey = async (key: string): Promise<boolean> => {
  try {
    setApiKey(key)
    await client.get('/keys/verify')
    return true
  } catch {
    return false
  }
}

export const getAuthStatus = async (): Promise<{ registered: boolean }> => {
  const res = await client.get('/auth/status')
  return res.data
}

export const register = async (accessKey: string): Promise<void> => {
  await client.post('/auth/register', { access_key: accessKey })
}

export const login = async (accessKey: string): Promise<void> => {
  await client.post('/auth/login', { access_key: accessKey })
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