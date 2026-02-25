from analyzer.scorer import score_robots
from analyzer.parser import parse_robots
from fastapi import FastAPI
from models.schemas import BrainRequest, BrainResponse
from dotenv import load_dotenv
from analyzer.recommender import generate_recommendations

load_dotenv()

app = FastAPI(title="Signis Brain Service", description="Signis Brain Service API", version="0.0.1")


@app.get("/health")
def read_root():
    return {"status": "OK"}

@app.post("/evaluate", response_model=BrainResponse)
def evaluate(request: BrainRequest):
    score, verdict = score_robots(request)
    recommendations = generate_recommendations(request)

    return BrainResponse(
        score=score,
        verdict=verdict,
        recommendations=recommendations,
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="[IP_ADDRESS]", port=8000)
