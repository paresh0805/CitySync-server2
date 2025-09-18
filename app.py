import gradio as gr
import tensorflow as tf
import numpy as np
from PIL import Image
import json

# === Configuration ===
MODEL_PATH = "road_classifier.h5"
CLASS_MAP_PATH = "class_indices.json"
IMG_SIZE = (224, 224)

# === Load model ===
model = tf.keras.models.load_model(MODEL_PATH)

# === Load class indices ===
with open(CLASS_MAP_PATH, "r") as f:
    class_indices = json.load(f)

# Invert class_indices to get index -> class mapping
index_to_class = {v: k for k, v in class_indices.items()}

# === Prediction function ===
def predict(img):
    try:
        img = img.convert("RGB")
        img = img.resize(IMG_SIZE)
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        preds = model.predict(img_array)
        pred_index = np.argmax(preds)
        label = index_to_class.get(pred_index, "Unknown")
        confidence = float(preds[0][pred_index])

        return {label: confidence}
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
    demo.launch()
