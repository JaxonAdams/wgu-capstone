import io
import os
import json
from functools import wraps

import boto3
import joblib
import pandas as pd
from dotenv import load_dotenv
from flask_cors import CORS
from flask import Flask, request, jsonify


app = Flask(__name__)
CORS(app, origins=["https://wgu-capstone-client.onrender.com", "http://localhost:*"])


load_dotenv("src/server/.env")


API_TOKEN = os.getenv("API_TOKEN")
VISUALIZATION_BASE_URL = os.getenv("VISUALIZATION_BASE_URL")


def load_ml_model(s3_bucket_name, s3_key, is_local=True):

    print("Loading ML model...")

    if is_local or not (s3_bucket_name and s3_key):
        model = joblib.load("data/models/rf.pkl")
    else:
        # Fetch from S3
        s3 = boto3.client("s3")
        obj = s3.get_object(Bucket=s3_bucket_name, Key=s3_key)
        
        with io.BytesIO(obj["Body"].read()) as b_stream:
            model = joblib.load(b_stream)

    return model["model"], model["features"]


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({'message': 'Missing or invalid token'}), 401

        token = auth_header.split(" ")[1]
        if token != API_TOKEN:
            return jsonify({'message': 'Unauthorized'}), 403

        return f(*args, **kwargs)
    return decorated


@app.route("/")
@app.route("/ping", methods=["GET"])
def ping():

    return "pong", 200


@app.route("/api/predict", methods=["POST"])
@token_required
def predict():

    try:
        body = request.get_json()
        data = body.get("data", {})
        metadata = body.get("_metadata", {})

        # Construct DataFrame with the correct feature order
        input_df = pd.DataFrame([{f: data.get(f) for f in feature_order}])

        # prediction = model.predict(input_df)
        proba = model.predict_proba(input_df)

        response_data = {
            "will_default": bool(proba[0][1] > 0.5),
        }

        if metadata.get("verbose", False):
            response_data |= {
                "probability": proba[0][1],
                "input": input_df.to_dict(orient="records")[0],
                "feature_order": feature_order,
            }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route("/api/visualizations", methods=["GET"])
@token_required
def get_visualization_urls():

    return jsonify({
        "credit_score_distribution": f"{VISUALIZATION_BASE_URL}/fico_distribution.png",
        "feature_importance": f"{VISUALIZATION_BASE_URL}/feature_importance.png",
        "correlation_heatmap": f"{VISUALIZATION_BASE_URL}/correlation_heatmap.png",
        "precision_recall_curve": f"{VISUALIZATION_BASE_URL}/precision_recall_curve.png",
        "probability_distribution": f"{VISUALIZATION_BASE_URL}/probability_distribution.png",
        "performance": f"{VISUALIZATION_BASE_URL}/performance.png",
        "confusion_matrix": f"{VISUALIZATION_BASE_URL}/confusion_matrix.png",
    })


# Load ML model on startup
model, feature_order = load_ml_model(
    os.environ.get("MODEL_BUCKET_NAME", ""),
    os.environ.get("MODEL_KEY", ""),
    is_local=os.environ.get("LOCAL", "").lower() == "true",
)

app.run(debug=True, use_reloader=False)
