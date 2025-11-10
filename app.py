import gradio as gr
import google.generativeai as genai

# 🔑 Ask user for API key in the UI
def configure_key(api_key):
    try:
        genai.configure(api_key=api_key)
        global model, chat
        model = genai.GenerativeModel("gemini-2.5-flash")
        chat = model.start_chat(history=[])
        return "✅ API Key configured successfully! You can now start chatting."
    except Exception as e:
        return f"❌ Error: {str(e)}"

# 💬 Chat function
def chat_with_gemini(user_input, history):
    try:
        response = chat.send_message(user_input)
        reply = response.text
        history.append((user_input, reply))
    except Exception as e:
        reply = f"⚠️ Error: {e}"
        history.append((user_input, reply))
    return history, history

# 🧱 Gradio UI
with gr.Blocks(theme="soft") as demo:
    gr.Markdown("## 🤖 Gemini 2.5 Flash Chatbot\nEnter your Google API key to start chatting with Gemini!")

    api_input = gr.Textbox(label="Enter your Google API Key", type="password", placeholder="Paste your API key here...")
    key_status = gr.Textbox(label="Status", interactive=False)

    api_button = gr.Button("Set API Key")
    api_button.click(configure_key, api_input, key_status)

    chatbot = gr.Chatbot(height=450)
    msg = gr.Textbox(placeholder="Type your message here...", label="Your Message")
    clear = gr.Button("Clear Chat")

    msg.submit(chat_with_gemini, [msg, chatbot], [chatbot, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

demo.launch()
