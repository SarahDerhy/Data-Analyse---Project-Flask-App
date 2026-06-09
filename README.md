# Movie Rating Predictor 

## 1. Project Description

This project is the third and final part of a series of assignments on machine learning applied to movie data from IMDb.

In Part 2, we built and trained a machine learning model to predict the average IMDb rating of movies. We developed a `prepare_data()` function that handles the feature engineering and preprocessing steps required before feeding data into the model.

In this part, we wrapped the trained model into a functional Flask web application. The user can fill in a form with movie details, and the application returns a predicted IMDb rating in real time.

---

## 2. Team Members

| Name        | ID        |
| ----------- | --------- |
| Sarah Derhy | 340889435 |
| Shirel Amar | 207065103 |

---

## 3. Project Structure

After extracting the trained model, the project structure should be:

```text
Data-Analyse---Project-Flask-App/
│
├── api.py
├── assets_data_prep.py
├── requirements.txt
├── README.md
├── trained_model.7z
├── trained_model.pkl
│
└── templates/
    └── index.html
```

---

## 4. Installation

### Prerequisite

* Python 3.10 or later
* Recommended version: Python 3.12

### Step 1 – Clone the repository

```bash
git clone https://github.com/SarahDerhy/Data-Analyse---Project-Flask-App
cd Data-Analyse---Project-Flask-App
```

### Step 2 – Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

### Step 3 – Install the dependencies

```bash
pip install -r requirements.txt
```

### Step 4 – Extract the trained model

The trained model is provided as `trained_model.7z` because the uncompressed file is too large to upload directly to GitHub.


Extract the model:

```bash
python -c "import py7zr; py7zr.SevenZipFile('trained_model.7z','r').extractall('.')"
```

After extraction, the file `trained_model.pkl` must be located in the root directory of the project.

---

## 5. Run the Server

```bash
python api.py
```

---

## 6. Open the Application

Open the following address in a web browser:

```text
http://localhost:5000
```

---

## 7. Input Fields

All input fields are optional. However, at least one field other than `tconst` must be filled in to generate a prediction.

Missing values are handled by the preprocessing pipeline. Providing more information may improve the relevance of the prediction.

| Field             | Description                        | Expected values                                                                                   | Why is this field optional?                                                                                                                                                |
| ----------------- | ---------------------------------- | ------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `tconst`          | IMDb identifier                    | Format: `tt` followed by digits, for example `tt1234567`                                          | This field is used to try to retrieve directors associated with the movie. If no IMDb ID is provided, or if no directors are found, the prediction can still be generated. |
| `startYear`       | Year the movie was released        | Number between 1 and 2025, for example `2019`                                                     | Missing values are handled by the preprocessing pipeline.                                                                                                                  |
| `Country`         | Country or countries of production | Country name or comma-separated country names, for example `USA` or `France,India`                | Missing values are handled by the preprocessing pipeline.                                                                                                                  |
| `genres`          | Genre or genres of the movie       | Genre name or comma-separated genre names, for example `Drama` or `Drama,Action`                  | Missing values are handled by the preprocessing pipeline.                                                                                                                  |
| `runtimeMinutes`  | Total runtime in minutes           | Positive integer, for example `120`                                                               | Missing values are handled by the preprocessing pipeline.                                                                                                                  |
| `lead_actors_ids` | IMDb IDs of the lead actors        | Format: `nm` followed by digits, separated by commas if needed, for example `nm0000123,nm0000456` | Missing values are handled by the preprocessing pipeline.                                                                                                                  |

---

## 8. Input Validation

The application returns a clear error message in the following situations:

* All fields are empty.
* Only the `tconst` field is filled in.
* A numeric field contains an invalid value.
* The `Country` or `genres` fields contain numbers.
* An unexpected internal error occurs.

---

## 9. Internet Connection

An internet connection is required for the first prediction because the application downloads the IMDb crew dataset in order to retrieve director information.

The dataset is cached while the Flask server is running, so subsequent predictions are faster.
