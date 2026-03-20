import { useEffect, useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import { getStats, getUsageByModel, getUsageOverTime } from '../api/dashboard'
import type { Stats, UsageByModel, UsageOverTime } from '../types'
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
    <div style={{ padding: '32px', flex: 1 }}>
      <h2 style={{ marginBottom: '24px', fontSize: '20px' }}>Overview</h2>

      {/* stat cards */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(4, 1fr)',
        gap: '16px',
        marginBottom: '32px'
      }}>
        <StatCard
          title="Total Requests"
          value={stats?.total_requests ?? '-'}
        />
        <StatCard
          title="Total Tokens"
          value={stats?.total_tokens?.toLocaleString() ?? '-'}
        />
        <StatCard
          title="Total Cost"
          value={stats ? `$${stats.total_cost_usd.toFixed(4)}` : '-'}
        />
        <StatCard
          title="Avg Latency"
          value={stats ? `${stats.avg_latency_ms.toFixed(0)}ms` : '-'}
        />
      </div>

      {/* requests over time */}
      <div style={{
        background: '#1a1a1a',
        border: '1px solid #2a2a2a',
        borderRadius: '8px',
        padding: '24px',
        marginBottom: '24px'
      }}>
        <p style={{ marginBottom: '16px', fontSize: '14px', color: '#888' }}>Requests Over Time</p>
        <ResponsiveContainer width="100%" height={200}>
          <BarChart data={overTime}>
            <XAxis dataKey="date" tick={{ fill: '#888', fontSize: 12 }} />
            <YAxis tick={{ fill: '#888', fontSize: 12 }} />
            <Tooltip
              contentStyle={{ background: '#1a1a1a', border: '1px solid #2a2a2a' }}
            />
            <Bar dataKey="requests" fill="#6366f1" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* usage by model */}
      <div style={{
        background: '#1a1a1a',
        border: '1px solid #2a2a2a',
        borderRadius: '8px',
        padding: '24px',
      }}>
        <p style={{ marginBottom: '16px', fontSize: '14px', color: '#888' }}>Usage by Model</p>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '14px' }}>
          <thead>
            <tr style={{ color: '#888', textAlign: 'left' }}>
              <th style={{ padding: '8px 0' }}>Model</th>
              <th style={{ padding: '8px 0' }}>Requests</th>
              <th style={{ padding: '8px 0' }}>Tokens</th>
              <th style={{ padding: '8px 0' }}>Cost</th>
            </tr>
          </thead>
          <tbody>
            {byModel.map(row => (
              <tr key={row.model} style={{ borderTop: '1px solid #2a2a2a' }}>
                <td style={{ padding: '10px 0' }}>{row.model}</td>
                <td style={{ padding: '10px 0' }}>{row.requests}</td>
                <td style={{ padding: '10px 0' }}>{row.tokens.toLocaleString()}</td>
                <td style={{ padding: '10px 0' }}>${row.cost_usd.toFixed(4)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Dashboard