# AI 커리어 코파일럿

채용 공고를 붙여넣으면 요구 기술·인재상·자격증을 분해하고, 보유 역량과의 갭을 분석해 마감일까지의 준비 타임라인을 안내하는 서비스. 프로젝트 배경과 원칙은 [CLAUDE.md](./CLAUDE.md) 참고.

## 사전 준비 (최초 1회, Windows)

아래 도구가 설치되어 있어야 한다. 이 환경(개발 서버)에는 **Node.js와 Docker가 설치되어 있지 않으므로**, 실행은 각자 로컬 PC에서 진행한다.

- [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/) — PostgreSQL+pgvector 컨테이너 실행용
- [Node.js LTS](https://nodejs.org/) — React(Vite) 개발 서버 실행용 (`node -v`, `npm -v`로 설치 확인)
- Python 3.11 — 백엔드 실행용 (이 환경엔 이미 3.11.9 설치되어 있음)

## 실행 순서

### 1. 저장소 클론 & 브랜치

```powershell
git clone <repo-url>
cd project
git checkout feat/phase0-setup
```

> main 브랜치는 보호되어 있다. 작업은 항상 `feat/기능명` 브랜치에서 하고, PR로 병합한다.

### 2. 환경변수 설정

```powershell
copy .env.example .env
```

`.env`를 열어 `OPENAI_API_KEY` 값을 채운다. `.env`는 절대 커밋하지 않는다 (`.gitignore`에 이미 포함됨).

### 3. DB 실행 (PostgreSQL + pgvector)

```powershell
docker compose up -d
```

컨테이너가 정상 기동됐는지 확인:

```powershell
docker compose ps
```

`db` 서비스 상태가 `healthy`가 될 때까지 몇 초 기다린다.

### 4. 백엔드 실행 (FastAPI)

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

브라우저에서 http://localhost:8000/health 접속 → `{"status": "ok", "db": "connected"}` 확인.
(패키지를 새로 설치했다면 `pip freeze > requirements.txt`로 갱신한다.)

### 5. 프론트엔드 실행 (React + Vite)

`frontend/` 폴더에는 Vite React 템플릿 구조가 이미 만들어져 있다. 의존성만 설치하면 된다.

```powershell
cd frontend
npm install
npm run dev
```

브라우저에서 http://localhost:5173 접속 → 화면에 "✅ 백엔드 연결됨" 표시 확인.

### 6. 전체 동작 확인 체크리스트

- [ ] `docker compose up`으로 PostgreSQL+pgvector 컨테이너가 뜬다
- [ ] http://localhost:8000/health 가 DB 연결 상태(`db: "connected"`)를 반환한다
- [ ] http://localhost:5173 화면에서 "백엔드 연결됨"이 표시된다
- [ ] React(5173) → FastAPI(8000) 호출이 CORS 에러 없이 성공한다

## 프로젝트 구조

```
project/
├── docker-compose.yml     # PostgreSQL + pgvector
├── .env.example           # 환경변수 키 이름만 (실제 값은 .env, 커밋 금지)
├── backend/               # FastAPI
│   └── app/
│       ├── main.py        # 진입점, CORS, /health
│       ├── config.py      # .env 로드
│       ├── database.py    # SQLAlchemy 연결
│       ├── models/        # DB 모델
│       ├── schemas/       # Pydantic 스키마
│       ├── api/           # 라우터
│       └── services/      # extractor(추출) / matcher(갭 매칭) / planner(타임라인)
├── frontend/               # React (Vite)
│   └── src/
│       ├── api/            # 백엔드 호출 함수
│       ├── components/     # 재사용 UI
│       └── pages/          # 화면 단위
└── data/                   # 정적 시드 데이터
    ├── tech_synonyms.json   # 기술 동의어 사전
    ├── certifications.json  # IT 자격증 정보
    └── job_samples/         # 테스트용 공고 샘플
```

## 개발 원칙

- 기술 스택은 임의로 변경하지 않는다 (React / FastAPI / PostgreSQL+pgvector / SQLAlchemy+Alembic / OpenAI API 고정).
- DB 스키마 변경은 Alembic 마이그레이션으로 관리한다.
- 커밋 메시지는 `feat:`, `fix:`, `chore:`, `docs:` 접두어를 사용한다.
