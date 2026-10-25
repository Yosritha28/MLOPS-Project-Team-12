from fastapi import FastAPI

app = FastAPI(title="ResumeIQ API", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok", "service": "resumeiq-backend"}