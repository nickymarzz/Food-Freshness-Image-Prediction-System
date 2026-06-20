from __future__ import annotations

import base64
import io
from typing import Any

import numpy as np
import uvicorn
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

from src.pipeline.prediction_pipeline import PredictionPipeline


app = FastAPI(title="Food Freshness Classifier API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline: PredictionPipeline | None = None


def _get_pipeline() -> PredictionPipeline:
    global pipeline
    if pipeline is None:
        pipeline = PredictionPipeline()
    return pipeline


def _read_upload_as_rgb_numpy(upload: UploadFile) -> np.ndarray:
    try:
        img = Image.open(upload.file).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {e}") from e
    return np.array(img)


def _pil_to_base64_jpeg(img: Image.Image, quality: int = 90) -> str:
    buf = io.BytesIO()
    img.convert("RGB").save(buf, format="JPEG", quality=quality, optimize=True)
    return base64.b64encode(buf.getvalue()).decode("ascii")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/predict/image")
async def predict_image(image: UploadFile = File(...)) -> dict[str, Any]:
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=415, detail=f"Unsupported content-type: {image.content_type!r}")

    img = _read_upload_as_rgb_numpy(image)
    pipe = _get_pipeline()

    try:
        result: dict[str, Any] = pipe.predict(img)
        annotated_img: Image.Image = pipe.annotate(img, result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}") from e

    return {
        "category": result["category"],
        "freshness": result["freshness"],
        "annotated_image": {
            "content_type": "image/jpeg",
            "base64": _pil_to_base64_jpeg(annotated_img),
        },
    }


if __name__ == "__main__":
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)
