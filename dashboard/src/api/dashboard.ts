import client from './client'
import type { Stats, UsageByModel, UsageByProject, UsageOverTime } from '../types/index'

export const getStats = async (): Promise<Stats> => {
  const res = await client.get('/dashboard/stats')
  return res.data
}

export const getUsageByModel = async (): Promise<UsageByModel[]> => {
  const res = await client.get('/dashboard/usage/by-model')
  return res.data
}

export const getUsageByProject = async (): Promise<UsageByProject[]> => {
  const res = await client.get('/dashboard/usage/by-project')
  return res.data
}

export const getUsageOverTime = async (): Promise<UsageOverTime[]> => {
  const res = await client.get('/dashboard/usage/over-time')
  return res.data
}

export const getSpendSummary = async () => {
  const res = await client.get('/dashboard/spend')
  return res.data
}