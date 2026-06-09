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


EXPECTED_FIELDS = [
    "tconst",
    "startYear",
    "Country",
    "genres",
    "runtimeMinutes",
    "lead_actors_ids"
]

# Fields that can be used to generate a prediction
PREDICTION_FIELDS = [
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

# Fields that must contain caracters when a value is provided
TEXT_FIELDS = [
    "Country",
    "genres"
]


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No data provided"
            }), 400

        # At least one field other than tconst must be provided
        has_prediction_data = any(
            field in data
            and data[field] is not None
            and str(data[field]).strip() != ""
            for field in PREDICTION_FIELDS
        )

        if not has_prediction_data:
            return jsonify({
                "error": "At least one field other than the IMDb ID must be filled in."
            }), 400

        # Validate text fields only when a value was provided
        for field in TEXT_FIELDS:
            if (
                field in data
                and data[field] is not None
                and str(data[field]).strip() != ""
                and any(character.isdigit() for character in str(data[field]))
            ):
                return jsonify({
                    "error": f"Invalid value for {field}: numbers are not allowed"
                }), 400
            
            
        # Replace empty fields with missing values
        for field in EXPECTED_FIELDS:
            if field not in data or data[field] is None or data[field] == "":
                if field in NUMERIC_FIELDS:
                    data[field] = np.nan
                else:
                    data[field] = pd.NA

        
        for field in NUMERIC_FIELDS:
            if pd.notna(data[field]):
                try:
                    data[field] = int(data[field])
                except (TypeError, ValueError):
                    return jsonify({
                        "error": f"Invalid value for {field}: a number is required"
                    }), 400

        
        df = pd.DataFrame([data])

        
        processed_data = prepare_data(df)

        
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