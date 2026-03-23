import { useEffect, useState } from 'react'
import client from '../api/client'
import type { APIKey } from '../types/index'

function Keys() {
  const [keys, setKeys] = useState<APIKey[]>([])
  const [name, setName] = useState('')
  const [project, setProject] = useState('')
  const [editProject, setEditProject] = useState('')
  const [spendLimit, setSpendLimit] = useState<number | ''>('')
  const [spendLimitAction, setSpendLimitAction] = useState('warn')
  const [rateLimitRequests, setRateLimitRequests] = useState<number | ''>('')
  const [rateLimitWindow, setRateLimitWindow] = useState<number | ''>('')
  const [webhookUrl, setWebhookUrl] = useState('')
  const [newKey, setNewKey] = useState<string | null>(null)
  const [editingKey, setEditingKey] = useState<APIKey | null>(null)
  const [editSpendLimit, setEditSpendLimit] = useState<number | ''>('')
  const [editSpendLimitAction, setEditSpendLimitAction] = useState('warn')
  const [editRateLimitRequests, setEditRateLimitRequests] = useState<number | ''>('')
  const [editRateLimitWindow, setEditRateLimitWindow] = useState<number | ''>('')
  const [editWebhookUrl, setEditWebhookUrl] = useState('')

  const fetchKeys = async () => {
    const res = await client.get('/keys')
    setKeys(res.data)
  }

  useEffect(() => {
    fetchKeys()
  }, [])
  const createKey = async () => {
    if (!name || !project) return
    const res = await client.post('/keys', {
      name,
      project,
      spend_limit_usd: spendLimit === '' ? null : spendLimit,
      spend_limit_action: spendLimitAction,
      rate_limit_requests: rateLimitRequests === '' ? null : rateLimitRequests,
      rate_limit_window: rateLimitWindow === '' ? null : rateLimitWindow,
      webhook_url: webhookUrl || null,
    })
    setNewKey(res.data.key)
    setName('')
    setProject('')
    setSpendLimit('')
    setSpendLimitAction('warn')
    setRateLimitRequests('')
    setRateLimitWindow('')
    setWebhookUrl('')
    fetchKeys()
  }

  const revokeKey = async (id: string) => {
    await client.delete(`/keys/${id}`)
    fetchKeys()
  }

  const openEdit = (key: APIKey) => {
    setEditingKey(key)
    setEditProject(key.project)
    setEditSpendLimit(key.spend_limit_usd ?? '')
    setEditSpendLimitAction(key.spend_limit_action ?? 'warn')
    setEditRateLimitRequests(key.rate_limit_requests ?? '')
    setEditRateLimitWindow(key.rate_limit_window ?? '')
    setEditWebhookUrl(key.webhook_url ?? '')
  }

  const saveEdit = async () => {
    if (!editingKey) return
    await client.patch(`/keys/${editingKey.id}`, {
      project: editProject || null,
      spend_limit_usd: editSpendLimit === '' ? null : editSpendLimit,
      spend_limit_action: editSpendLimitAction,
      rate_limit_requests: editRateLimitRequests === '' ? null : editRateLimitRequests,
      rate_limit_window: editRateLimitWindow === '' ? null : editRateLimitWindow,
      webhook_url: editWebhookUrl || null,
    })
    setEditingKey(null)
    fetchKeys()
  }

  return (
    <div className="keys-page">
      <h2>API Keys</h2>

      <div className="card">
        <p className="card-title">Create New Key</p>

        <div className="form-row">
          <input
            className="input"
            placeholder="Key name *"
            value={name}
            onChange={e => setName(e.target.value)}
          />
          <input
            className="input"
            placeholder="Project *"
            value={project}
            onChange={e => setProject(e.target.value)}
          />
        </div>

        <div className="form-row">
          <input
            className="input"
            type="number"
            placeholder="Rate limit (requests)"
            value={rateLimitRequests}
            onChange={e => setRateLimitRequests(e.target.value === '' ? '' : parseInt(e.target.value))}
          />
          <input
            className="input"
            type="number"
            placeholder="Rate limit window (seconds)"
            value={rateLimitWindow}
            onChange={e => setRateLimitWindow(e.target.value === '' ? '' : parseInt(e.target.value))}
          />
        </div>

        <div className="form-row">
          <input
            className="input"
            type="number"
            placeholder="Monthly spend limit (USD)"
            value={spendLimit}
            onChange={e => setSpendLimit(e.target.value === '' ? '' : parseFloat(e.target.value))}
          />
          <select
            className="select"
            value={spendLimitAction}
            onChange={e => setSpendLimitAction(e.target.value)}
          >
            <option value="warn">Warn only</option>
            <option value="block">Block requests</option>
          </select>
        </div>

        <div className="form-row">
          <input
            className="input"
            placeholder="Webhook URL (optional)"
            value={webhookUrl}
            onChange={e => setWebhookUrl(e.target.value)}
          />
          <button
            className="btn-primary"
            onClick={createKey}
            disabled={!name || !project}
            style={{ opacity: !name || !project ? 0.5 : 1 }}
          >
            Create Key
          </button>
        </div>

        {newKey && (
          <div className="new-key-banner">
            ⚠️ Copy this key now — it won't be shown again: {newKey}
          </div>
        )}
      </div>

      <div className="card">
        <p className="card-title">Active Keys</p>
        <table className="table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Project</th>
              <th>Rate Limit</th>
              <th>Spend Limit</th>
              <th>Created</th>
              <th>Last Used</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {keys.map(key => (
              <tr key={key.id}>
                <td>{key.name}</td>
                <td>{key.project ?? '-'}</td>
                <td>{key.rate_limit_requests ? `${key.rate_limit_requests}/${key.rate_limit_window}s` : 'default'}</td>
                <td>{key.spend_limit_usd ? `$${key.spend_limit_usd} (${key.spend_limit_action})` : '-'}</td>
                <td>{new Date(key.created_at).toLocaleDateString()}</td>
                <td>{key.last_used_at ? new Date(key.last_used_at).toLocaleDateString() : '-'}</td>
                <td style={{ display: 'flex', gap: '8px' }}>
                  <button className="btn-secondary" onClick={() => openEdit(key)}>Edit</button>
                  <button className="btn-danger" onClick={() => revokeKey(key.id)}>Revoke</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {editingKey && (
        <div className="modal-overlay" onClick={() => setEditingKey(null)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <h3>Edit Key — {editingKey.name}</h3>

            <div className="form-row">
              <input
                className="input"
                placeholder="Project *"
                value={editProject}
                onChange={e => setEditProject(e.target.value)}
              />
            </div>

            <div className="form-row">
              <input
                className="input"
                type="number"
                placeholder="Rate limit (requests)"
                value={editRateLimitRequests}
                onChange={e => setEditRateLimitRequests(e.target.value === '' ? '' : parseInt(e.target.value))}
              />
              <input
                className="input"
                type="number"
                placeholder="Rate limit window (seconds)"
                value={editRateLimitWindow}
                onChange={e => setEditRateLimitWindow(e.target.value === '' ? '' : parseInt(e.target.value))}
              />
            </div>

            <div className="form-row">
              <input
                className="input"
                type="number"
                placeholder="Monthly spend limit (USD)"
                value={editSpendLimit}
                onChange={e => setEditSpendLimit(e.target.value === '' ? '' : parseFloat(e.target.value))}
              />
              <select
                className="select"
                value={editSpendLimitAction}
                onChange={e => setEditSpendLimitAction(e.target.value)}
              >
                <option value="warn">Warn only</option>
                <option value="block">Block requests</option>
              </select>
            </div>

            <div className="form-row">
              <input
                className="input"
                placeholder="Webhook URL (optional)"
                value={editWebhookUrl}
                onChange={e => setEditWebhookUrl(e.target.value)}
              />
            </div>

            <div className="modal-actions">
              <button className="btn-secondary" onClick={() => setEditingKey(null)}>Cancel</button>
              <button
                className="btn-primary"
                onClick={saveEdit}
                disabled={!editProject}
                style={{ opacity: !editProject ? 0.5 : 1 }}
              >
                Save Changes
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Keys