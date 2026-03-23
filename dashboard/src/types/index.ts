export interface Stats {
  total_requests: number
  total_tokens: number
  total_cost_usd: number
  avg_latency_ms: number
}

export interface UsageByModel {
  model: string
  requests: number
  tokens: number
  cost_usd: number
}

export interface UsageByProject {
  project: string
  requests: number
  tokens: number
  cost_usd: number
}

export interface UsageOverTime {
  date: string
  requests: number
  tokens: number
  cost_usd: number
}

export interface APIKey {
  id: string
  name: string
  project: string
  is_active: boolean
  created_at: string
  last_used_at: string | null
  spend_limit_usd: number | null
  spend_limit_action: string | null
  webhook_url: string | null
  rate_limit_requests: number | null
  rate_limit_window: number | null
}