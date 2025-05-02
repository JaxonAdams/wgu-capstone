import io
import os

import boto3
import joblib
import pandas as pd
from flask import Flask, request, jsonify


app = Flask(__name__)


def load_ml_model(s3_bucket_name, s3_key):

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

        # Construct DataFrame with the correct feature order
        input_df = pd.DataFrame([{f: data.get(f) for f in feature_order}])

        # prediction = model.predict(input_df)
        proba = model.predict_proba(input_df)

        response_data = {
            "will_default": bool(proba[0][1] > 0.5),
            "probability": proba[0][1],
            "input": input_df.to_dict(orient="records")[0],
            "feature_order": feature_order,
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Load ML model on startup
model, feature_order = load_ml_model(
    os.environ.get("MODEL_BUCKET_NAME"),
    os.environ.get("MODEL_KEY"),
)
