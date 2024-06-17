import gradio as gr

from services.agent import legislatia


with open("front/css.svelte", "r") as file:
    css = file.read()

with open("front/description.txt", "r", encoding="utf-8") as file:
    description = file.read()


gr.ChatInterface(legislatia,
                 chatbot=gr.Chatbot(show_label=False),
                 title="🇫🇷 LégislatIA 🇫🇷",
                 description=description,
                 theme=gr.themes.Default(primary_hue="blue",
                                         secondary_hue="blue",
                                         neutral_hue="blue"),
                 css=css,
                 analytics_enabled=False,
                 submit_btn="▶️",
                 retry_btn="🔄",
                 undo_btn="↩️",
                 clear_btn="🗑️",
                 placeholder="Poser votre question..."
                 ).launch()
