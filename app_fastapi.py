from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from vector_store import query_embeddings
from whatsapp import send_whatsapp_message
from pinecone import Pinecone
from anthropic import Anthropic
from config import (
    WHATSAPP_TOKEN,
    WHATSAPP_VERIFY_TOKEN,
    WHATSAPP_PHONE_NUMBER_ID,
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME,
    ANTHROPIC_API_KEY
)

app = FastAPI()

# Sanity check for required environment variables
required_vars = {
    "WHATSAPP_TOKEN": WHATSAPP_TOKEN,
    "WHATSAPP_VERIFY_TOKEN": WHATSAPP_VERIFY_TOKEN,
    "WHATSAPP_PHONE_NUMBER_ID": WHATSAPP_PHONE_NUMBER_ID,
    "PINECONE_API_KEY": PINECONE_API_KEY,
    "PINECONE_INDEX_NAME": PINECONE_INDEX_NAME,
    "ANTHROPIC_API_KEY": ANTHROPIC_API_KEY
}

missing_vars = [name for name, value in required_vars.items() if not value]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {missing_vars}")

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

# Initialize Anthropic client
anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)

# WhatsApp verification
@app.get("/webhook")
async def verify_webhook(request: Request):
    params = request.query_params
    if params.get("hub.verify_token") == WHATSAPP_VERIFY_TOKEN:
        return int(params.get("hub.challenge"))
    return JSONResponse(content="Invalid token", status_code=403)

# WhatsApp messages
@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()

    try:
        # Safely extract WhatsApp message payload
        value = data.get("entry", [{}])[0].get("changes", [{}])[0].get("value", {})
        messages = value.get("messages")

        # Ignore non-message events (e.g., delivery/read statuses)
        if not messages:
            return JSONResponse(content={"status": "ignored"})

        msg_obj = messages[0]

        # Handle only text messages; ignore others for now
        if "text" in msg_obj and "body" in msg_obj["text"]:
            message = msg_obj["text"]["body"]
        else:
            return JSONResponse(content={"status": "ignored_non_text"})

        from_number = msg_obj.get("from")

        # Use existing vector store function for search
        context_chunks = query_embeddings(message, top_k=3)
        
        if context_chunks:
            context = "\n\n".join(context_chunks)
            
            # Ask Anthropic with context (Messages API requires top-level system)
            completion = anthropic.messages.create(
                model="claude-3-5-sonnet-20240620",
                system="You are a helpful AI assistant. Answer questions based on the provided context from uploaded documents. If the context doesn't contain relevant information, say so politely. Keep answers concise and helpful.",
                messages=[
                    {"role": "user", "content": f"Context from documents:\n{context}\n\nQuestion: {message}\n\nAnswer based on the context:"}
                ],
                max_tokens=400
            )

            reply = completion.content[0].text
        else:
            # No relevant context found
            reply = "I don't have any relevant information in my knowledge base to answer your question. Please make sure documents have been uploaded through the web interface, or try rephrasing your question."

        # Send reply back to WhatsApp
        url = f"https://graph.facebook.com/v17.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
        headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
        payload = {
            "messaging_product": "whatsapp",
            "to": from_number,
            "type": "text",
            "text": {"body": reply}
        }
        
        # Use the whatsapp module function instead of direct requests
        send_whatsapp_message(from_number, reply)

    except KeyError as e:
        print(f"Error parsing WhatsApp message: {e}")
        return JSONResponse(content={"status": "error", "detail": "Invalid message format"}, status_code=400)
    except Exception as e:
        print(f"Error processing message: {e}")
        return JSONResponse(content={"status": "error", "detail": str(e)}, status_code=500)

    return JSONResponse(content={"status": "ok"})