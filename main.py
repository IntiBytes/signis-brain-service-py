from analyzer.stats import compute_stats
from analyzer.scorer import score_robots
from fastapi import FastAPI
from models.schemas import BrainRequest, BrainResponse
from dotenv import load_dotenv
from analyzer.recommender import generate_recommendations

load_dotenv()

app = FastAPI(
    title="Signis Brain Service",
    description="Signis Brain Service API",
    version="0.0.1",
)


@app.get("/health")
def read_root():
    return {"status": "OK"}


@app.post("/evaluate", response_model=BrainResponse)
def evaluate(request: BrainRequest):
    score, verdict = score_robots(request)
    recommendations, issues, warnings, good_practices = generate_recommendations(
        request
    )

    stats, meta = compute_stats(request)

    return BrainResponse(
        score=score,
        verdict=verdict,
        recommendations=recommendations,
        issues=issues,
        warnings=warnings,
        good_practices=good_practices,
        stats=stats,
        meta=meta,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="[IP_ADDRESS]", port=8000)
