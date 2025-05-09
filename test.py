import gradio as gr
import json
from ollama import Client  # Import the Client class

# Configuration
MODEL = "deepseek-r1:1.5b"  # Or any other model you have in Ollama
OLLAMA_URL = "http://localhost:11434"  # Default, change if needed
system_message = "You are a helpful assistant." #You can change the system message

# Initialize Ollama client
ollama_client = Client(host=OLLAMA_URL)

def chat(message, history):
    """
    Modified chat function to use Ollama instead of OpenAI.
    It maintains a similar structure to the original function
    for compatibility with Gradio's expected input/output.
    """
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]

    print("History is:")
    print(history)
    print("And messages is:")
    print(messages)
    # Ollama expects a single list of messages, not a stream.
    # We build the messages list as before.

    # Format history for Ollama.  Ollama expects the history to be
    # in the same format as the user and assistant messages:
    # { 'role': 'user' or 'assistant', 'content': '...' }
    ollama_messages = []
    if system_message:
        ollama_messages.append({'role': 'system', 'content': system_message})
    for turn in history:
        ollama_messages.append({'role': 'user', 'content': turn[0]}) # User message
        ollama_messages.append({'role': 'assistant', 'content': turn[1]}) # Assistant response
    ollama_messages.append({'role': 'user', 'content': message})

    try:
        # Call Ollama API
        response = ollama_client.chat(model=MODEL, messages=ollama_messages)
        # The response from Ollama is a dictionary.  Extract the text.
        reply = response['message']['content']
        print(f"Ollama Response: {reply}")
        yield reply #Changed from response += to yield reply
    except Exception as e:
        error_message = f"Error calling Ollama: {e}"
        print(error_message)
        yield error_message # Return the error message

# Setup Gradio interface
inputs = [gr.Textbox(label="Message"), gr.State([])] #gr.State to hold conversation history
outputs = gr.Chatbot(label="Chat with Ollama")

# Create a Gradio ChatInterface
iface = gr.ChatInterface(
    fn=chat,
    type="messages",
    title="Ollama Chat Interface",
    description=f"Chat with the Ollama model: {MODEL}",
)

if __name__ == "__main__":
    iface.launch(inbrowser=True)
