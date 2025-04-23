from fastapi import FastAPI

app = FastAPI(
    title="Pediatric Fever Chatbot API",
    description="API for handling pediatric fever-related conversations using AI.",
    version="1.0.0"
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Pediatric Fever Chatbot API"}
