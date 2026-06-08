# Movie Rating Predictor 🎬

## 1. Project Description
This project is the third and final part of a series of assignments on machine learning applied to movie data from IMDb.

In Part 2, we built and trained a machine learning model to predict the average IMDb rating of movies. We developed a `prepare_data()` function that handles all the feature engineering and preprocessing steps required before feeding data into the model.

In this part, we wrapped that model into a functional Flask web application. The user can fill in a form with movie details, and the app returns a predicted IMDb rating in real time.

---

## 2. Team Members
| Name | ID |
|------|------|
| Sarah Derhy | 340889435 |
| Shirel Amar | 207065103 |

---

## 3. Installation

### Prerequisite
- Python 3.10 or later (recommended: Python 3.12)

---

### Step 1 – Clone the repository
```bash
git clone https://github.com/SarahDerhy/Data-Analyse---Project-Flask-App
cd Data-Analyse---Project-Flask-App
```

---

### Step 2 – Create virtual environment
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
---

### Step 3 – Extract the trained model (terminal method)

The model is stored in a compressed file: `trained_model.7z`.


```bash
pip install py7zr
```

Then extract:

```bash
python -c "import py7zr; py7zr.SevenZipFile('trained_model.7z','r').extractall('.')"
```

---

### Step 4 – Install dependencies
```bash
pip install -r requirements.txt
```

---

## 4. Run the server
```bash
python api.py
```

---

## 5. Open the app
http://127.0.0.1:5000

---

## 6. Input Fields

All input fields are optional. Users may provide only the information available to them. Missing values are handled by the preprocessing pipeline. However, providing more information may improve the relevance of the prediction.

| Field                      | Description                        | Expected values                                                               |
|---------------------------|------------------------------------|------------------------------------------------------------------------------|
| tconst (optional)         | IMDb identifier                    | Format: tt followed by digits (example: tt1234567)                          |
| startYear (optional)      | Year the movie was released        | Number between 1 and 2025 (example: 2019)                                    |
| Country (optional)        | Country or countries of production | Country name(s), comma-separated (example: USA or France,India)             |
| genres (optional)         | Genre or genres of the movie       | Genre name(s), comma-separated (example: Drama or Drama,Action)             |
| runtimeMinutes (optional) | Total runtime in minutes           | Positive integer (example: 120)                                             |
| lead_actors_ids (optional)| IMDb IDs of the lead actors        | Format: nm followed by digits, comma-separated (example: nm0000123,nm0000456) |

---

