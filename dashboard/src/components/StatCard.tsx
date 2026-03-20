interface Props {
  title: string
  value: string | number
  subtitle?: string
}

function StatCard({ title, value, subtitle }: Props) {
  return (
    <div style={{
      background: '#1a1a1a',
      border: '1px solid #2a2a2a',
      borderRadius: '8px',
      padding: '24px',
    }}>
      <p style={{ color: '#888', fontSize: '14px', marginBottom: '8px' }}>{title}</p>
      <p style={{ fontSize: '28px', fontWeight: '600' }}>{value}</p>
      {subtitle && <p style={{ color: '#888', fontSize: '12px', marginTop: '4px' }}>{subtitle}</p>}
    </div>
  )
}

export default StatCard