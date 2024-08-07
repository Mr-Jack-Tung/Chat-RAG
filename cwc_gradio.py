import gradio as gr
from model_manager import ModelManager


class CWCGradio:

    def __init__(self):
        self.model_manager = ModelManager()
        self.chat_history = []

    def chat(self, message):
        response = self.model_manager.process_input(message)
        self.chat_history.append((message, response))
        return "", self.chat_history

    def update_model(self, model):
        self.model_manager.update_model(model)
        self.chat_history = []  # Clear chat history

    def launch(self):
        with gr.Blocks(theme="monochrome", fill_height=True, fill_width=True) as iface:
            gr.Markdown("# Chat RAG: Interactive Coding Assistant")
            gr.Markdown("This app is a chat-based coding assistant with a graphical user interface built using "
                        "Gradio. It allows users to interact with various language models to ask coding questions, "
                        "with the ability to upload files for additional context. The app utilizes RAG ("
                        "Retrieval-Augmented Generation) to provide more informed responses based on the loaded "
                        "documents and user queries.")
            with gr.Row():
                with gr.Column(scale=6):
                    selected_model = gr.Dropdown(
                        choices=["codestral:latest", "mistral-nemo:latest", "llama3.1:latest",
                                 "deepseek-coder-v2:latest", "gemma2:latest", "codegemma:latest"],
                        label="Select Model", value="codestral:latest", interactive=True)
                    chatbot = gr.Chatbot(show_label=False, height=500)
                    msg = gr.Textbox(show_label=False, autoscroll=True, autofocus=True,
                                     placeholder="Enter your coding question here...")
                    with gr.Row():
                        clear = gr.ClearButton([msg, chatbot])
                    msg.submit(self.chat, inputs=[msg], outputs=[msg, chatbot], show_progress="full")
                    selected_model.change(self.update_model, inputs=selected_model, show_progress="full")
                with gr.Column(scale=1):
                    gr.Files(show_label=False)

        iface.launch(inbrowser=True, share=True)
