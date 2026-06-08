from pathlib import Path
import numpy as np
from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib

from assets_data_prep import prepare_data


app = Flask(__name__)

# Load the trained model once when the server starts
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "trained_model.pkl"

model = joblib.load(MODEL_PATH)


# Fields expected from the HTML form
EXPECTED_FIELDS = [
    "tconst",
    "startYear",
    "Country",
    "genres",
    "runtimeMinutes",
    "lead_actors_ids"
]

# Fields that must contain numbers when a value is provided
NUMERIC_FIELDS = [
    "startYear",
    "runtimeMinutes"
]


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Replace empty fields with missing values
        for field in EXPECTED_FIELDS:
            if field not in data or data[field] is None or data[field] == "":
                if field in NUMERIC_FIELDS:
                    data[field] = np.nan
                else:
                    data[field] = pd.NA

        # Validate numeric fields only when a value was provided
        for field in NUMERIC_FIELDS:
            if pd.notna(data[field]):
                try:
                    data[field] = int(data[field])
                except (TypeError, ValueError):
                    return jsonify({
                        "error": f"Invalid value for {field}: a number is required"
                    }), 400

        # Create a one-row DataFrame
        df = pd.DataFrame([data])

        # Apply the same data preparation used during model training
        processed_data = prepare_data(df)

        # Generate the prediction
        prediction = model.predict(processed_data)[0]

        return jsonify({
            "predicted_rating": round(float(prediction), 2)
        })

    except Exception as e:
        return jsonify({
            "error": f"Internal server error: {str(e)}"
        }), 500


if __name__ == "__main__":
    app.run(debug=True)

