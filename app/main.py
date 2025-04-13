from fastapi import FastAPI

app = FastAPI(title="IIT Project API")

@app.get("/")
async def root():
    return {"message": "Welcome to IIT Project API"} 