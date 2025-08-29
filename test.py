import gradio as gr
# import pandas as pd  # DataFrame 사용 시 주석 해제

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("Accordion을 클릭하여 문서 목록을 확인하세요.")
    
    with gr.Group():  # management_area 역할
        for i in range(5):
            docs = ['doc1', 'doc2']  # 예시 데이터
            
            with gr.Accordion(label=str(i), open=False):  # label을 문자열로 변환
                for doc in docs:
                    with gr.Row():
                        gr.Markdown(f"{doc}")
                
                # DataFrame 사용 시 (주석 해제)
                # df = pd.DataFrame({"Documents": docs})
                # gr.DataFrame(value=df, interactive=False)

if __name__ == "__main__":
    demo.launch()