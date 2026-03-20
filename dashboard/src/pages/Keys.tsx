import { useEffect, useState } from 'react'
import client from '../api/client'
import type { APIKey } from '../types'

function Keys() {
  const [keys, setKeys] = useState<APIKey[]>([])
  const [name, setName] = useState('')
  const [project, setProject] = useState('')
  const [newKey, setNewKey] = useState<string | null>(null)

  const fetchKeys = async () => {
    const res = await client.get('/keys')
    setKeys(res.data)
  }

  useEffect(() => {
    fetchKeys()
  }, [])

  const createKey = async () => {
    if (!name) return
    const res = await client.post('/keys', { name, project: project || null })
    setNewKey(res.data.key)
    setName('')
    setProject('')
    fetchKeys()
  }

  const revokeKey = async (id: string) => {
    await client.delete(`/keys/${id}`)
    fetchKeys()
  }

  return (
    <div style={{ padding: '32px', flex: 1 }}>
      <h2 style={{ marginBottom: '24px', fontSize: '20px' }}>API Keys</h2>

      {/* create key form */}
      <div style={{
        background: '#1a1a1a',
        border: '1px solid #2a2a2a',
        borderRadius: '8px',
        padding: '24px',
        marginBottom: '24px',
      }}>
        <p style={{ marginBottom: '16px', fontSize: '14px', color: '#888' }}>Create New Key</p>
        <div style={{ display: 'flex', gap: '12px', marginBottom: '12px' }}>
          <input
            placeholder="Key name"
            value={name}
            onChange={e => setName(e.target.value)}
            style={{
              background: '#0f0f0f',
              border: '1px solid #2a2a2a',
              borderRadius: '6px',
              padding: '8px 12px',
              color: '#f0f0f0',
              fontSize: '14px',
              flex: 1,
            }}
          />
          <input
            placeholder="Project (optional)"
            value={project}
            onChange={e => setProject(e.target.value)}
            style={{
              background: '#0f0f0f',
              border: '1px solid #2a2a2a',
              borderRadius: '6px',
              padding: '8px 12px',
              color: '#f0f0f0',
              fontSize: '14px',
              flex: 1,
            }}
          />
          <button
            onClick={createKey}
            style={{
              background: '#6366f1',
              border: 'none',
              borderRadius: '6px',
              padding: '8px 20px',
              color: '#fff',
              fontSize: '14px',
              cursor: 'pointer',
            }}
          >
            Create
          </button>
        </div>

        {/* show new key */}
        {newKey && (
          <div style={{
            background: '#0f0f0f',
            border: '1px solid #6366f1',
            borderRadius: '6px',
            padding: '12px',
            fontSize: '13px',
            fontFamily: 'monospace',
            color: '#6366f1',
          }}>
            ⚠️ Copy this key now — it won't be shown again: {newKey}
          </div>
        )}
      </div>

      {/* keys table */}
      <div style={{
        background: '#1a1a1a',
        border: '1px solid #2a2a2a',
        borderRadius: '8px',
        padding: '24px',
      }}>
        <p style={{ marginBottom: '16px', fontSize: '14px', color: '#888' }}>Active Keys</p>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '14px' }}>
          <thead>
            <tr style={{ color: '#888', textAlign: 'left' }}>
              <th style={{ padding: '8px 0' }}>Name</th>
              <th style={{ padding: '8px 0' }}>Project</th>
              <th style={{ padding: '8px 0' }}>Created</th>
              <th style={{ padding: '8px 0' }}>Last Used</th>
              <th style={{ padding: '8px 0' }}></th>
            </tr>
          </thead>
          <tbody>
            {keys.map(key => (
              <tr key={key.id} style={{ borderTop: '1px solid #2a2a2a' }}>
                <td style={{ padding: '10px 0' }}>{key.name}</td>
                <td style={{ padding: '10px 0' }}>{key.project ?? '-'}</td>
                <td style={{ padding: '10px 0' }}>{new Date(key.created_at).toLocaleDateString()}</td>
                <td style={{ padding: '10px 0' }}>{key.last_used_at ? new Date(key.last_used_at).toLocaleDateString() : '-'}</td>
                <td style={{ padding: '10px 0' }}>
                  <button
                    onClick={() => revokeKey(key.id)}
                    style={{
                      background: 'transparent',
                      border: '1px solid #ef4444',
                      borderRadius: '4px',
                      padding: '4px 10px',
                      color: '#ef4444',
                      fontSize: '12px',
                      cursor: 'pointer',
                    }}
                  >
                    Revoke
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Keys