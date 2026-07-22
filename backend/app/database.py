"""SQLAlchemy 엔진/세션 설정. FastAPI 라우터는 get_db 의존성을 통해서만 DB에 접근한다."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모든 SQLAlchemy 모델(app/models/*)이 상속할 베이스 클래스.
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
