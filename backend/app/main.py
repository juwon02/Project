"""FastAPI 진입점. CORS 설정과 /health 엔드포인트만 갖춘 Phase 0 최소 서버."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.config import settings
from app.database import engine

app = FastAPI(title="AI 커리어 코파일럿 API")

# React 개발 서버(5173)와 FastAPI(8000)는 origin이 달라 브라우저가 기본적으로 요청을 차단한다.
# 이를 허용하지 않으면 프론트엔드에서 /health 호출 자체가 CORS 에러로 실패한다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.cors_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    """DB에 실제 쿼리를 날려 연결 상태까지 확인한다 (서버가 떠 있다고 DB도 살아있는 건 아니므로)."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "db": "connected"}
    except Exception as exc:
        return {"status": "error", "db": "disconnected", "detail": str(exc)}
