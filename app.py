import gradio as gr
import tensorflow as tf
import numpy as np
from PIL import Image
import json
import os

# === Configuration ===
MODEL_PATH = "road_classifier.h5"
CLASS_MAP_PATH = "class_indices.json"
IMG_SIZE = (224, 224)

# === Load model ===
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# === Load class indices ===
class_indices = {}
try:
    with open(CLASS_MAP_PATH, "r") as f:
        class_indices = json.load(f)
    # Check for duplicate indices
    if len(class_indices) != len(set(class_indices.values())):
        print("Warning: Duplicate indices found in class_indices")
    index_to_class = {v: k for k, v in class_indices.items()}
except Exception as e:
    print(f"Error loading class indices: {e}")
    index_to_class = {}

# === Prediction function ===
def predict(img):
    if model is None or not index_to_class:
        return {"error": "Model or class indices not loaded properly"}
    if img is None:
        return {"error": "No image uploaded"}

    try:
        # Convert and resize image
        img = img.convert("RGB")
        img = img.resize(IMG_SIZE)
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Get predictions
        preds = model.predict(img_array)
        top_indices = np.argsort(preds[0])[::-1][:3]  # Top 3 predictions
        result = {index_to_class.get(i, f"Unknown_{i}"): float(preds[0][i]) for i in top_indices}
        return result
    except Exception as e:
        return {"error": str(e)}

# === Gradio Interface ===
demo = gr.Interface(
    fn=predict,
    inputs=gr.Image(type="pil"),
    outputs=gr.Label(num_top_classes=3),
    title="Road Issue Classifier",
    description="Upload a road image and get predicted issue type with confidence."
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)  # Full launch configuration
