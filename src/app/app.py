import gradio as gr
import numpy as np
from PIL import Image
import datetime

from src.pipeline.prediction_pipeline import PredictionPipeline
from src.app.storage_tips import get_storage_html
from src.components.mongodb_client import MongoDBClient


pipeline: PredictionPipeline | None = None
db = MongoDBClient()


def _get_pipeline() -> PredictionPipeline:
    global pipeline
    if pipeline is None:
        pipeline = PredictionPipeline()
    return pipeline


CSS = """
:root {
    --primary: #3b82f6;
    --success: #10b981;
    --error: #ef4444;
    --bg-dark: #0f172a;
    --card-bg: rgba(30, 41, 59, 0.7);
    --border: rgba(255, 255, 255, 0.1);
}

.main-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
}

.hero-section {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(16, 185, 129, 0.1));
    padding: 40px;
    border-radius: 24px;
    border: 1px solid var(--border);
    margin-bottom: 30px;
    text-align: center;
    backdrop-filter: blur(10px);
}

.hero-section h1 {
    font-size: 2.5rem;
    margin-bottom: 10px;
    background: linear-gradient(to right, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.dashboard-grid {
    display: grid;
    gap: 24px;
}

.card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 24px;
    backdrop-filter: blur(12px);
    transition: transform 0.2s ease;
}

.storage-card {
    background: rgba(59, 130, 246, 0.05);
    border-left: 4px solid var(--primary);
    padding: 20px;
    border-radius: 12px;
    margin-top: 15px;
}

.badge {
    padding: 6px 14px;
    border-radius: 9999px;
    font-weight: 600;
    font-size: 0.85rem;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.badge-fresh { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
.badge-rotten { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }

.confidence-container {
    margin-top: 10px;
}

.confidence-bar-bg {
    height: 8px;
    width: 100%;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
    overflow: hidden;
}

.confidence-bar-fill {
    height: 100%;
    background: var(--primary);
    border-radius: 4px;
    transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
}

.history-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px;
    border-bottom: 1px solid var(--border);
}

.history-item:last-child { border-bottom: none; }

.history-thumb {
    width: 48px;
    height: 48px;
    border-radius: 8px;
    object-fit: cover;
}
"""


def _to_pil(image: object) -> Image.Image:
    if image is None:
        raise ValueError("No image provided.")
    if isinstance(image, Image.Image):
        return image.convert("RGB")
    if isinstance(image, np.ndarray):
        return Image.fromarray(image.astype("uint8")).convert("RGB")
    raise TypeError("Unsupported image type.")


def create_confidence_html(label, score):
    percentage = score * 100
    return f"""
    <div class="confidence-container">
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px; font-size: 0.8rem; opacity: 0.8;">
            <span>{label}</span>
            <span>{percentage:.1f}%</span>
        </div>
        <div class="confidence-bar-bg">
            <div class="confidence-bar-fill" style="width: {percentage}%"></div>
        </div>
    </div>
    """


def predict_single(image, history):
    if image is None:
        return None, "", "", "", history

    try:
        pil_img = _to_pil(image)
    except Exception as e:
        return None, f"<div class='badge badge-rotten'>Error: {e}</div>", "", "", history

    pipe = _get_pipeline()
    result = pipe.predict(pil_img)
    annotated_img = pipe.annotate(pil_img, result)

    cat = result["category"]
    fresh = result["freshness"]

    # Generate Badge HTML
    fresh_class = "badge-fresh" if fresh["label"] == "Fresh" else "badge-rotten"
    fresh_badge = f"<div class='badge {fresh_class}'>{fresh['label'].upper()}</div>"
    
    cat_badge = f"<div class='badge' style='background: rgba(59, 130, 246, 0.2); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3);'>{cat['label'].upper()}</div>"

    # Generate Metrics HTML
    cat_html = create_confidence_html("Category Confidence", cat["score"])
    fresh_html = create_confidence_html("Freshness Confidence", fresh["score"])
    metrics_html = f"<div class='card'>{cat_badge} {fresh_badge}{cat_html}{fresh_html}</div>"

    # Get Storage Insights
    storage_html = f"<div class='card'>{get_storage_html(cat['label'])}</div>"

    # Save to MongoDB
    db.save_prediction(result)

    # Update History
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    new_entry = {
        "time": timestamp,
        "label": f"{fresh['label']} {cat['label']}",
        "freshness": fresh["label"]
    }
    updated_history = [new_entry] + history[:4] # Keep last 5

    history_html = "<div class='card'><h3>Session History</h3>"
    for item in updated_history:
        color = "#34d399" if item['freshness'] == "Fresh" else "#f87171"
        history_html += f"""
        <div class="history-item">
            <div style="font-size: 0.75rem; opacity: 0.5; min-width: 60px;">{item['time']}</div>
            <div style="font-weight: 500; color: {color};">{item['label']}</div>
        </div>
        """
    history_html += "</div>"

    return annotated_img, metrics_html, storage_html, history_html, updated_history


with gr.Blocks(title="Food Freshness Prediction System") as demo:
    initial_history = db.get_history(limit=5)
    history_state = gr.State(initial_history)
    
    with gr.Column(elem_classes=["main-container"]):
        # Hero Section
        gr.HTML(
            """
            <div class="hero-section">
                <h1>Food Freshness Intelligence</h1>
                <p style="opacity: 0.8; font-size: 1.1rem;">Advanced AI-powered produce analysis for a sustainable kitchen.</p>
            </div>
            """
        )

        with gr.Row(equal_height=False):
            # Left Column: Interaction
            with gr.Column(scale=3):
                with gr.Tabs():
                    with gr.Tab("📷 Upload Image"):
                        in_upload = gr.Image(sources=["upload"], type="numpy", label="Drop an image here", height=400)
                        btn_upload = gr.Button("Analyze Freshness", variant="primary", size="lg")
                    
                    with gr.Tab("🤳 Live Webcam"):
                        in_webcam = gr.Image(sources=["webcam"], type="numpy", label="Webcam Feed", height=400)
                        btn_webcam = gr.Button("Capture & Analyze", variant="primary", size="lg")

                gr.Markdown(
                    """
                    ### 💡 Best Practices
                    - Ensure the item is well-lit and centered.
                    - Solid backgrounds help the model focus on the produce.
                    - For small items (berries), hold them closer to the camera.
                    """
                )

            # Right Column: Results & History
            with gr.Column(scale=2):
                out_img = gr.Image(label="Analysis Overlay", height=300, elem_classes=["card"])
                out_metrics = gr.HTML("<div class='card' style='opacity: 0.5;'>Waiting for analysis...</div>")
                out_storage = gr.HTML("")
                
                # Initial history HTML
                def render_initial_history(hist):
                    if not hist:
                        return "<div class='card'><h3>Session History</h3><p style='opacity: 0.5;'>No predictions yet.</p></div>"
                    
                    html = "<div class='card'><h3>Session History</h3>"
                    for item in hist:
                        color = "#34d399" if item['freshness'] == "Fresh" else "#f87171"
                        html += f"""
                        <div class="history-item">
                            <div style="font-size: 0.75rem; opacity: 0.5; min-width: 60px;">{item['time']}</div>
                            <div style="font-weight: 500; color: {color};">{item['label']}</div>
                        </div>
                        """
                    html += "</div>"
                    return html

                out_history = gr.HTML(render_initial_history(initial_history))

        # Event Bindings
        inputs = [in_upload, history_state]
        outputs = [out_img, out_metrics, out_storage, out_history, history_state]
        btn_upload.click(predict_single, inputs=inputs, outputs=outputs)
        
        btn_webcam.click(predict_single, inputs=[in_webcam, history_state], outputs=outputs)

        # Footer
        gr.HTML(
            """
            <div style="text-align: center; margin-top: 50px; padding: 20px; border-top: 1px solid var(--border); opacity: 0.6; font-size: 0.9rem;">
                Powered by MobileNetV2 Deep Learning • Food Freshness Prediction System v2.0
            </div>
            """
        )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, quiet=False, show_error=True, css=CSS, theme=gr.themes.Soft())
