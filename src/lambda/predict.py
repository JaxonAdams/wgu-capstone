import os
import json

import boto3
import joblib
import pandas as pd


# Cached values -- reused on warm starts
s3 = boto3.client("s3")

MODEL_BUCKET = os.environ.get("MODEL_BUCKET_NAME")
MODEL_KEY = os.environ.get("MODEL_KEY")
LOCAL_MODEL_PATH = "/tmp/rf.pkl"

model = None
feature_order = None


def download_model():

    global model, feature_order
    if model is None or feature_order is None:
        print("Downloading .pkl file...")
        s3.download_file(MODEL_BUCKET, MODEL_KEY, LOCAL_MODEL_PATH)
        print("Download complete. Loading .pkl file...")
        model_data = joblib.load(LOCAL_MODEL_PATH)

        model = model_data["model"]
        feature_order = model_data["features"]


def handler(event, _):

    download_model()

    try:
        body = json.loads(event.get("body", "{}"))
        data = body.get("data", {})

        # Construct DataFrame with the correct feature order
        input_df = pd.DataFrame([{f: data.get(f) for f in feature_order}])

        # prediction = model.predict(input_df)
        proba = model.predict_proba(input_df)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            # "body": json.dumps({"will_default": bool(prediction[0])})
            "body": json.dumps({
                "will_default": bool(proba[0][1] > 0.5),
                "probability": proba[0][1],
                "input": input_df.to_dict(orient="records")[0],
                "feature_order": feature_order,
            }),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }