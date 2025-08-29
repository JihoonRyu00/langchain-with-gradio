# app.py

import gradio as gr
import pandas as pd
from core.logic import (
    initialize_vector_store,
    get_all_docs_as_dataframe,
    search_similar_sentences,
    add_sentence,
    delete_sentence,
    delete_topic
)

# --- Vector Store 초기화 ---
print("Initializing Vector Stores...")
db_openai = initialize_vector_store("OpenAI")
db_upstage = initialize_vector_store("Upstage")
db_ollama = initialize_vector_store("Ollama")
print("Initialization complete.")


# --- UI 헬퍼 함수 ---
def search_all_models(query):
    return (
        search_similar_sentences(query, db_openai),
        search_similar_sentences(query, db_upstage),
        search_similar_sentences(query, db_ollama)
    )

def add_and_refresh(content, topic):
    global db_openai, db_upstage, db_ollama
    if not content or not topic:
        return get_all_docs_as_dataframe(db_openai), "내용과 주제를 모두 입력해주세요."
    add_sentence(content, topic, db_openai, "OpenAI")
    add_sentence(content, topic, db_upstage, "Upstage")
    _, msg = add_sentence(content, topic, db_ollama, "Ollama")
    return get_all_docs_as_dataframe(db_openai), msg

def delete_and_refresh(id_to_delete):
    global db_openai, db_upstage, db_ollama
    if not id_to_delete:
        return get_all_docs_as_dataframe(db_openai), "삭제할 문서의 ID를 입력해주세요."
    _, msg = delete_sentence(id_to_delete, db_openai, "OpenAI")
    delete_sentence(id_to_delete, db_upstage, "Upstage")
    delete_sentence(id_to_delete, db_ollama, "Ollama")
    return get_all_docs_as_dataframe(db_openai), msg

def delete_topic_and_refresh(topic_to_delete):
    global db_openai, db_upstage, db_ollama
    if not topic_to_delete:
        return get_all_docs_as_dataframe(db_openai), "삭제할 주제명을 입력해주세요."
    _, msg = delete_topic(topic_to_delete, db_openai, "OpenAI")
    delete_topic(topic_to_delete, db_upstage, "Upstage")
    delete_topic(topic_to_delete, db_ollama, "Ollama")
    return get_all_docs_as_dataframe(db_openai), msg



# --- Gradio 전체 UI 구성 ---
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🧠 문장 유사도 비교 및 Vector Store 편집기")

    with gr.Tabs():
        with gr.TabItem("1. 유사도 검색"):
            with gr.Row():
                query_input = gr.Textbox(label="문장 입력", placeholder="비교할 문장을 입력하세요...", scale=4)
                search_btn = gr.Button("검색 실행", variant="primary", scale=1)
            with gr.Row():
                openai_output = gr.DataFrame(label="OpenAI", interactive=False)
                upstage_output = gr.DataFrame(label="Upstage", interactive=False)
                ollama_output = gr.DataFrame(label="Ollama", interactive=False)

        with gr.TabItem("2. Vector Store 편집"):
            status_output = gr.Textbox(label="처리 상태", interactive=False, lines=1)
            
            gr.Markdown("### 📖 현재 저장된 문서 목록")
            # ✅ 변경점: management_area를 DataFrame으로 직접 정의
            doc_list_df = gr.DataFrame(
                label="전체 문서 목록",
                headers=["id", "topic", "content"],
                interactive=False
            )

            # ✅ 변경점 2: 추가/삭제 기능을 별도의 Accordion으로 묶어 분리
            with gr.Accordion("⚙️ 컨트롤 패널 (문장 추가/삭제)", open=True):
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("#### ➕ 새 문장 추가")
                        add_content_input = gr.Textbox(label="문장 내용")
                        add_topic_input = gr.Textbox(label="주제", info="기존 주제 또는 새 주제명을 입력하세요.")
                        add_btn = gr.Button("추가하기", variant="primary")
                    with gr.Column():
                        gr.Markdown("#### ➖ 삭제")
                        delete_sentence_id_input = gr.Textbox(label="삭제할 문장 ID", placeholder="위 표에서 ID를 복사하세요.")
                        delete_sentence_btn = gr.Button("문장 삭제", variant="stop")
                        delete_topic_name_input = gr.Textbox(label="삭제할 주제명", placeholder="위 표에서 주제명을 입력하세요.")
                        delete_topic_btn = gr.Button("주제 전체 삭제", variant="stop")

    # --- 이벤트 핸들러 연결 ---
    search_btn.click(fn=search_all_models, inputs=query_input, outputs=[openai_output, upstage_output, ollama_output])
    
    add_btn.click(
        fn=add_and_refresh,
        inputs=[add_content_input, add_topic_input],
        outputs=[doc_list_df, status_output]
    )
    delete_sentence_btn.click(
        fn=delete_and_refresh,
        inputs=delete_sentence_id_input,
        outputs=[doc_list_df, status_output]
    )
    delete_topic_btn.click(
        fn=delete_topic_and_refresh,
        inputs=delete_topic_name_input,
        outputs=[doc_list_df, status_output]
    )

    # 페이지 로드 시 DataFrame을 채우는 이벤트
    demo.load(fn=lambda: get_all_docs_as_dataframe(db_openai), outputs=doc_list_df)

if __name__ == "__main__":
    demo.launch()