import axios from 'axios'

const client = axios.create({
  baseURL: import.meta.env.PROD
    ? '/api'
    : 'http://localhost:8000',
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

export default client