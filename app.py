from flask import Flask, request, jsonify, render_template
import numpy as np
from PIL import Image
import io
import tensorflow as tf
import os
from google.cloud import storage

app = Flask(__name__)

# Model Download from GCS

GCS_MODEL_URI = os.environ.get(
    "MODEL_GCS_URI",
    "gs://food-freshness-model/model/my_binary_class_model.h5"
)

LOCAL_MODEL_PATH = "/tmp/model.h5"


def download_from_gcs(gcs_uri, local_path):
    if os.path.exists(local_path):
        print(f"Model already exists at {local_path}.")
        return

    if not gcs_uri.startswith("gs://"):
        raise ValueError("MODEL_GCS_URI must begin with gs://")

    bucket_name, blob_path = gcs_uri[5:].split("/", 1)

    print(f"Downloading model from GCS: {gcs_uri}")

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_path)
    blob.download_to_filename(local_path)

    print("Model downloaded successfully.")


# Download on startup
try:
    download_from_gcs(GCS_MODEL_URI, LOCAL_MODEL_PATH)
except Exception as e:
    print("Error downloading model:", e)

print("Loading model from:", LOCAL_MODEL_PATH)
model = tf.keras.models.load_model(LOCAL_MODEL_PATH)
model.make_predict_function()
print("Model loaded successfully.")

# Preprocessing

def preprocess_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((256, 256))
    arr = np.array(img).astype("float32") / 255.0
    arr = np.expand_dims(arr, axis=0)
    return arr

# Routes

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

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

# Main
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
