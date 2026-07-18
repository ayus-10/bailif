from ollama import Client

from config import MODEL, OLLAMA_HOST

client = Client(host=OLLAMA_HOST)


def stream_chat(messages):
    return client.chat(
        model=MODEL,
        messages=messages,
        stream=True,
    )
