import { useEffect, useState } from 'react'
import { fetchHealth } from '../api/health'

// Phase 0 완료 기준 확인용 화면: 마운트 시 /health를 호출해 백엔드·DB 연결 상태를 보여준다.
export default function HealthCheck() {
  const [status, setStatus] = useState('checking')
  const [detail, setDetail] = useState(null)

  useEffect(() => {
    fetchHealth()
      .then((data) => {
        setDetail(data)
        setStatus(data.db === 'connected' ? 'connected' : 'error')
      })
      .catch((error) => {
        setDetail({ message: error.message })
        setStatus('error')
      })
  }, [])

  return (
    <div>
      <h1>AI 커리어 코파일럿</h1>
      {status === 'checking' && <p>백엔드 연결 확인 중...</p>}
      {status === 'connected' && <p>✅ 백엔드 연결됨 (DB: {detail.db})</p>}
      {status === 'error' && (
        <p>❌ 백엔드 연결 실패 — {detail?.detail ?? detail?.message}</p>
      )}
    </div>
  )
}
