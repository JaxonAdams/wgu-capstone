import io
import os
import json

import boto3
import joblib
import pandas as pd
from flask import Flask, request, jsonify


app = Flask(__name__)


# Load config.json
with open("src/server/config.json") as f:
    config = json.load(f)


VISUALIZATION_BASE_URL = config["VISUALIZATION_BASE_URL"]


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


@app.route("/api/predict", methods=["POST"])
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
def get_visualization_urls():

    return jsonify({
        "credit_score_distribution": f"{VISUALIZATION_BASE_URL}/fico_distribution.png",
        "feature_importance": f"{VISUALIZATION_BASE_URL}/feature_importance.png",
        "correlation_heatmap": f"{VISUALIZATION_BASE_URL}/correlation_heatmap.png",
        "precision_recall_curve": f"{VISUALIZATION_BASE_URL}/precision_recall_curve.png",
        "probability_distribution": f"{VISUALIZATION_BASE_URL}/probability_distribution.png",
    })


# Load ML model on startup
model, feature_order = load_ml_model(
    os.environ.get("MODEL_BUCKET_NAME", ""),
    os.environ.get("MODEL_KEY", ""),
    is_local=os.environ.get("LOCAL", "").lower() == "true",
)

app.run(debug=True)
