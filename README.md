# echo-board

FastAPI와 Pydantic을 사용하여 게시글 생성 및 조회 기능을 제공하는 REST API 서버입니다.


## Getting Started

### 1. 설치

1. 레포지토리 다운로드
   ```bash
   https://github.com/f-lab-edu/echo-board.git
   ```

2. Poetry 설치
   ```bash
   brew install pipx
   pipx install poetry==1.7.1 --python python3.12
   ```
3. Poetry 환경 세팅
   ```bash
   poetry install --sync
   ```
4. Poetry 가상환경 실행
   ```bash
   poetry shell
   ```

### 2. 서버 실행 방법
- 실행 : `poetry run dev`

### 3. Poetry 가상환경 종료
- 종료 : `exit`


## Development Guide
### Prerequisites
* Python 3.12 or higher
* Poetry package manager

## Project Structure
```
.
├── README.md                      # 프로젝트 소개 및 사용법 문서
├── poetry.lock                    # 의존성 잠금 파일
├── pyproject.toml                 # 프로젝트 의존성 설정
├── src/                           # 애플리케이션 소스 코드 파일
│   │── api/                       # 주요 애플리케이션 코드
│   │── config.py                   # 환경 변수 및 설정값 구성 파일
│   │── main.py                    # FastAPI 앱 객체를 생성
│   └── server.py                  # 개발용 서버 실행을 스크립트
└── tests/                         # 테스트 파일들
```
