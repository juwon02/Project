// FastAPI /health 엔드포인트 호출. 백엔드 주소를 여기 한 곳에서만 관리한다.
const API_BASE_URL = 'http://localhost:8000'

export async function fetchHealth() {
  const response = await fetch(`${API_BASE_URL}/health`)
  if (!response.ok) {
    throw new Error(`서버 응답 오류: ${response.status}`)
  }
  return response.json()
}
