import tkinter as tk
from tkinter import ttk
import gradio as gr
import tqdm
import json
from ollama import Client  # Import the Client class

OLLAMA_URL = "http://localhost:11434"  # Default, change if needed

with open("my_tools.txt", "r", encoding="utf-8") as f:
    tools = f.read()

prompt = f"""
You are an AI agent specializing in concept development and deconstruction of
instructions into detailed, step-by-step tasks. \n
You have the following tools at your disposal: {tools}. \n
If the concept involves the use of tools beyond those listed, suggest using other tools.
"""

# Initialize Ollama client
ollama_client = Client(host=OLLAMA_URL)

# Define the list of options
options = [mod.model for mod in ollama_client.list().models]
selected_option = None

def get_selected_option():
    global selected_option
    selected_option = dropdown.get()
    print(f"You selected: {selected_option}")
    # You can now use the selected option in your Python script

    root.destroy()  # Close the popup window

# Create the main window
root = tk.Tk()
root.title("Select an Option")

# Create the dropdown
dropdown = ttk.Combobox(root, values=options)
dropdown.pack(pady=20)

# Create the submit button
submit_button = tk.Button(root, text="Submit", command=get_selected_option)

submit_button.pack(pady=10)

# Start the main loop
root.mainloop()

# Configuration
MODEL = selected_option #"codellama:7b"  # Or any other model you have in Ollama

# Initialize Ollama client
ollama_client = Client(host=OLLAMA_URL)

def chat(message, history):
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    response = ollama_client.chat(model=MODEL, messages=messages)
    # The response from Ollama is a dictionary.  Extract the text.
    reply = response['message']['content']
    return reply

# Create a Gradio ChatInterface
iface = gr.ChatInterface(
    fn=chat,
    type="messages",
    title="Ollama Chat Interface",
    description=f"Chat with the Ollama model: {MODEL}",
)

iface.launch(inbrowser=True)
