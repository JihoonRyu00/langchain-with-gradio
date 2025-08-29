# 🧠 문장 유사도 비교 및 Vector Store 편집기

## 1. 프로젝트 개요

이 프로젝트는 다양한 임베딩 모델(OpenAI, Upstage, Ollama)을 활용하여 문장 간의 의미적 유사도를 측정하고, 그 결과를 직관적으로 비교할 수 있는 웹 애플리케이션입니다. Gradio를 사용하여 UI를 구축했으며, 사용자가 직접 FAISS 기반의 Vector Store에 문장을 추가하거나 삭제할 수 있는 동적인 편집 기능을 제공합니다.

---

## 2. 주요 기능

-   **🔍 다중 모델 유사도 검색**:
    -   하나의 쿼리 문장에 대해 OpenAI, Upstage, Ollama 임베딩 모델별 유사도 검색 결과를 동시에 비교할 수 있습니다.
    -   유사도 점수(L2 Distance)가 낮은 순서대로 정렬하여 보여줍니다.
-   **✏️ 동적 Vector Store 관리**:
    -   UI를 통해 현재 데이터베이스에 저장된 모든 문서를 실시간으로 조회할 수 있습니다.
    -   새로운 문장과 주제를 추가할 수 있습니다.
    -   특정 문장(ID 기준) 또는 주제 전체를 데이터베이스에서 삭제할 수 있습니다.
-   **💾 영구 데이터 저장**:
    -   FAISS를 사용하여 Vector Store를 로컬 파일 시스템에 저장합니다.
    -   애플리케이션을 재시작해도 추가/삭제된 내용이 그대로 유지됩니다.

---

## 3. 프로젝트 구조
```bash
langchain-with-gradio/
├── core/
│   ├── init.py
│   └── logic.py           # 핵심 로직 (모델, DB 관리, 검색/수정 기능)
├── data/
│   └── sentences.py       # 초기 데이터셋
├── faiss_db_openai/       # OpenAI FAISS DB 저장 폴더
├── faiss_db_upstage/      # Upstage FAISS DB 저장 폴더
├── faiss_db_ollama/       # Ollama FAISS DB 저장 폴더
├── app.py                 # Gradio UI 실행 파일
├── requirements.txt       # 의존성 패키지 목록
└── .env                   # API 키 저장 파일
```
---

## 4. 설치 및 실행 방법

### 가. 환경 설정

1.  **저장소 복제**
    ```bash
    git clone <repository-url>
    cd langchain-with-gradio
    ```

2.  **가상환경 생성 및 활성화**
    ```bash
    python -m venv .venv
    # Windows
    .\.venv\Scripts\activate
    # macOS / Linux
    source .venv/bin/activate
    ```

3.  **필요 패키지 설치**
    ```bash
    pip install -r requirements.txt
    ```

4.  **.env 파일 생성**
    -   프로젝트 루트에 `.env` 파일을 생성하고 아래와 같이 API 키를 입력합니다.
    ```
    OPENAI_API_KEY="sk-..."
    UPSTAGE_API_KEY="..."
    ```

5.  **Ollama 설정**
    -   로컬 환경에 [Ollama](https://ollama.com/)를 설치합니다.
    -   터미널에서 아래 명령어를 실행하여 임베딩 모델을 다운로드합니다.
    ```bash
    ollama pull nomic-embed-text
    ```

### 나. 애플리케이션 실행

1.  **Ollama 서버 실행**
    -   **새로운 터미널**을 열고 아래 명령어를 입력하여 Ollama 서버를 실행합니다. 이 터미널은 앱을 사용하는 동안 계속 실행 상태로 두어야 합니다.
    ```bash
    ollama serve
    ```

2.  **Gradio 앱 실행**
    -   원래의 터미널로 돌아와 아래 명령어를 입력하여 Gradio 애플리케이션을 실행합니다.
    ```bash
    python app.py
    ```

3.  **웹 브라우저에서 접속**
    -   터미널에 출력된 로컬 URL (예: `http://127.0.0.1:7860`)을 웹 브라우저에서 엽니다.

---

## 5. 핵심 기술 스택

-   **UI Framework**: `Gradio`
-   **LLM Orchestration**: `LangChain`
-   **Vector Store**: `FAISS`
-   **Embedding Models**:
    -   `OpenAI`: text-embedding-3-small
    -   `Upstage`: solar-embedding-1-large
    -   `Ollama`: nomic-embed-text






