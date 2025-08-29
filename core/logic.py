# core/logic.py

import os
import uuid
import pandas as pd
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_upstage import UpstageEmbeddings
from langchain_ollama import OllamaEmbeddings  # 수정된 import 문
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from data.sentences import INITIAL_SENTENCES

load_dotenv()

EMBEDDING_MODELS = {
    "OpenAI": OpenAIEmbeddings(model="text-embedding-3-small"),
    "Upstage": UpstageEmbeddings(model="solar-embedding-1-large"),
    "Ollama": OllamaEmbeddings(model="nomic-embed-text"),
}


def initialize_vector_store(model_name: str):
    """지정된 모델에 대한 FAISS Vector Store를 초기화하거나 로드합니다. (안정성 강화)"""
    embedding_function = EMBEDDING_MODELS[model_name]
    db_folder_path = f"faiss_db_{model_name.lower()}"
    try:
        if os.path.exists(db_folder_path):
            print(
                f"Loading existing FAISS DB for {model_name} from '{db_folder_path}'..."
            )
            db = FAISS.load_local(
                folder_path=db_folder_path,
                embeddings=embedding_function,
                allow_dangerous_deserialization=True,
            )
            print(f"DB for {model_name} loaded successfully.")
        else:
            print(f"Creating new FAISS DB for {model_name}...")
            docs = [
                Document(page_content=text, metadata=meta)
                for text, meta in INITIAL_SENTENCES
            ]
            db = FAISS.from_documents(docs, embedding_function)
            db.save_local(folder_path=db_folder_path)
            print(f"New DB for {model_name} created and saved successfully.")
        return db
    except Exception as e:
        print(f"Error initializing/loading vector store for {model_name}: {e}")
        return None


# --- 데이터 조회 함수 ---
def get_all_docs_as_dataframe(db: FAISS):
    """Vector Store에서 모든 문서를 DataFrame으로 반환합니다."""
    if not db or not db.docstore._dict:
        return pd.DataFrame(columns=["id", "topic", "content"])
    
    docs_with_ids = [
        {
            "id": doc_id,
            "topic": doc.metadata.get("topic", "N/A"),
            "content": doc.page_content
        }
        for doc_id, doc in db.docstore._dict.items()
    ]
    return pd.DataFrame(docs_with_ids)



# search_similar_sentences, add_sentence, delete_sentence 함수는 기존과 동일하게 유지
def search_similar_sentences(query: str, db: FAISS, k: int = 3):
    if not query or not db:
        return pd.DataFrame()
    results = db.similarity_search_with_score(query, k=k)

    formatted_results = []
    for doc, score in results:
        formatted_results.append(
            {
                "score": f"{score:.4f}",
                "topic": doc.metadata.get("topic", "N/A"),
                "content": doc.page_content,
            }
        )
    return pd.DataFrame(formatted_results)


def add_sentence(content: str, topic: str, db: FAISS, model_name: str):
    if not content or not topic or not db:
        return db, "내용과 주제를 모두 입력해주세요."
    new_doc = Document(page_content=content, metadata={"topic": topic})
    doc_id = str(uuid.uuid4())
    db.add_documents([new_doc], ids=[doc_id])
    db_folder_path = f"faiss_db_{model_name.lower()}"
    db.save_local(folder_path=db_folder_path)
    return db, f"문서(ID: {doc_id})가 성공적으로 추가되었습니다."


def delete_sentence(doc_id: str, db: FAISS, model_name: str):
    if not doc_id or not db:
        return db, "삭제할 문서의 ID를 입력해주세요."
    try:
        db.delete([doc_id])
        db_folder_path = f"faiss_db_{model_name.lower()}"
        db.save_local(folder_path=db_folder_path)
        return db, f"문서(ID: {doc_id})가 성공적으로 삭제되었습니다."
    except Exception as e:
        return db, f"삭제 중 오류 발생: {e}"


def delete_topic(topic_to_delete: str, db: FAISS, model_name: str):
    """Vector Store에서 특정 주제의 모든 문서를 삭제합니다."""
    if not topic_to_delete or not db:
        return db, "삭제할 주제를 지정해주세요."

    ids_to_delete = [
        doc_id
        for doc_id, doc in db.docstore._dict.items()
        if doc.metadata.get("topic") == topic_to_delete
    ]

    if not ids_to_delete:
        return db, f"'{topic_to_delete}' 주제의 문서가 없습니다."

    try:
        db.delete(ids_to_delete)
        db_folder_path = f"faiss_db_{model_name.lower()}"
        db.save_local(folder_path=db_folder_path)
        return (
            db,
            f"주제 '{topic_to_delete}'의 문서 {len(ids_to_delete)}개가 삭제되었습니다.",
        )
    except Exception as e:
        return db, f"주제 삭제 중 오류 발생: {e}"
