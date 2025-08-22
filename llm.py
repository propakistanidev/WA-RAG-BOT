from anthropic import Anthropic
from config import ANTHROPIC_API_KEY

client = Anthropic(api_key=ANTHROPIC_API_KEY)

def ask_anthropic(query, context):
    prompt = f"Answer the user query using the provided context.\n\nContext:\n{context}\n\nUser: {query}\nAnswer:"
    resp = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.content[0].text