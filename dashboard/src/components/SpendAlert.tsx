interface SpendItem {
  key_id: string
  key_name: string
  project: string
  spend_limit_usd: number
  spend_limit_action: string
  current_spend_usd: number
  percentage: number
}

interface Props {
  items: SpendItem[]
}

function SpendAlert({ items }: Props) {
  if (items.length === 0) return null

  return (
    <div className="card">
      <p className="card-title">Budget Alerts</p>
      <div className="spend-alert-list">
        {items.map(item => (
          <div key={item.key_id} className="spend-alert-item">
            <div className="spend-alert-header">
              <div>
                <span className="spend-alert-name">{item.key_name}</span>
                <span className="spend-alert-project">{item.project}</span>
              </div>
              <div className="spend-alert-amounts">
                <span className={item.percentage >= 100 ? 'spend-over' : item.percentage >= 80 ? 'spend-warning' : 'spend-ok'}>
                  ${item.current_spend_usd.toFixed(4)}
                </span>
                <span className="spend-limit">/ ${item.spend_limit_usd} ({item.spend_limit_action})</span>
              </div>
            </div>
            <div className="spend-bar-bg">
              <div
                className={`spend-bar-fill ${item.percentage >= 100 ? 'spend-bar-over' : item.percentage >= 80 ? 'spend-bar-warning' : 'spend-bar-ok'}`}
                style={{ width: `${Math.min(item.percentage, 100)}%` }}
              />
            </div>
            <p className="spend-bar-label">{item.percentage}% used</p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default SpendAlert