import { useEffect, useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import { getStats, getUsageByModel, getUsageOverTime } from '../api/dashboard'
import type { Stats, UsageByModel, UsageOverTime } from '../types/index'
import StatCard from '../components/StatCard'

function Dashboard() {
  const [stats, setStats] = useState<Stats | null>(null)
  const [byModel, setByModel] = useState<UsageByModel[]>([])
  const [overTime, setOverTime] = useState<UsageOverTime[]>([])

  useEffect(() => {
    getStats().then(setStats)
    getUsageByModel().then(setByModel)
    getUsageOverTime().then(setOverTime)
  }, [])

  return (
    <div className="dashboard-page">
      <h2>Overview</h2>

      <div className="stat-grid">
        <StatCard title="Total Requests" value={stats?.total_requests ?? '-'} />
        <StatCard title="Total Tokens" value={stats?.total_tokens?.toLocaleString() ?? '-'} />
        <StatCard title="Total Cost" value={stats ? `$${stats.total_cost_usd.toFixed(4)}` : '-'} />
        <StatCard title="Avg Latency" value={stats ? `${stats.avg_latency_ms.toFixed(0)}ms` : '-'} />
      </div>

      <div className="chart-card">
        <p className="chart-title">Requests Over Time</p>
        <ResponsiveContainer width="100%" height={200}>
          <BarChart data={overTime}>
            <XAxis dataKey="date" tick={{ fill: '#888', fontSize: 12 }} />
            <YAxis tick={{ fill: '#888', fontSize: 12 }} />
            <Tooltip contentStyle={{ background: '#1a1a1a', border: '1px solid #2a2a2a' }} />
            <Bar dataKey="requests" fill="#6366f1" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="table-card">
        <p className="table-title">Usage by Model</p>
        <table className="dashboard-table">
          <thead>
            <tr>
              <th>Model</th>
              <th>Requests</th>
              <th>Tokens</th>
              <th>Cost</th>
            </tr>
          </thead>
          <tbody>
            {byModel.map(row => (
              <tr key={row.model}>
                <td>{row.model}</td>
                <td>{row.requests}</td>
                <td>{row.tokens.toLocaleString()}</td>
                <td>${row.cost_usd.toFixed(4)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Dashboard