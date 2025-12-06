from flask import Flask, request, jsonify, render_template
import numpy as np
from PIL import Image
import io
import tensorflow as tf
import os

MODEL_PATH = "my_binary_class_model.h5"

app = Flask(__name__)


# Load model 
print("Loading model...", MODEL_PATH)
model = tf.keras.models.load_model(MODEL_PATH)
model.make_predict_function()
print("Model loaded.")


# Image preprocessing

def preprocess_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((256, 256))  # match model input size
    arr = np.array(img).astype("float32") / 255.0
    arr = np.expand_dims(arr, axis=0)  # batch dimension
    return arr


# Routes

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")  # serve UI

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "no file part"}), 400

    file = request.files["file"]
    img_bytes = file.read()

    try:
        x = preprocess_image(img_bytes)
        preds = model.predict(x)

        if preds.shape[-1] == 1:
            score = float(preds[0][0])
            label = "fresh" if score < 0.5 else "spoiled"
            return jsonify({"label": label, "score": score})
        else:
            probs = preds[0].tolist()
            top_idx = int(np.argmax(probs))
            return jsonify({"predicted_index": top_idx, "probs": probs})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run app
# -------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
