import re
import pandas as pd
import numpy as np
import pycountry
from functools import lru_cache

@lru_cache(maxsize=1)
def load_crew():
    crew = pd.read_csv(
        "https://datasets.imdbws.com/title.crew.tsv.gz",
        sep="\t",
        compression="gzip",
        usecols=["tconst", "directors"],
        low_memory=False
    )

    return crew.replace("\\N", pd.NA)


def prepare_data(df):
    df = df.copy()

    main_genres = ["Drama","Comedy","Documentary","Romance","Action","Crime","Thriller","Horror","Adventure","Mystery"]

    def build_country_pattern():
        country_names = [country.name for country in pycountry.countries]

        country_names += ["USA","UK","United States","United States of America", "England", "Britain","Great Britain",
                        "East Germany",
                        "West Germany",
                        "Czechoslovakia",
                        "Soviet Union",
                        "Yugoslavia"]

        return "|".join(
            sorted(map(re.escape, country_names), key=len, reverse=True)
        )

    # Load crew file and merge it with df:
    crew = load_crew()
    country_pattern = build_country_pattern()


    df = df.merge(crew[["tconst", "directors"]], on="tconst", how="left")

    df["directors_list"] = df["directors"].astype("string").str.split(",")

    # Count directors for each movie
    df["num_directors"] = (pd.to_numeric(df["directors_list"].str.len(),errors="coerce")
                            .fillna(0)
                            .astype(int))



    df["genres"] = (df["genres"].fillna("").astype(str).str.replace(r"[\[\]'\"]", "", regex=True)
                    .str.replace(r"\s*,\s*", ",", regex=True)
                    .str.strip()
                    .replace("", np.nan))

    # Create one binary column for each frequent genre
    genre_dummies = (df["genres"].astype("string").fillna("").str.get_dummies(sep=","))

    main_genre_dummies = (genre_dummies.reindex(columns=main_genres, fill_value=0).add_prefix("genre_"))

    df = pd.concat([df, main_genre_dummies], axis=1)

    # 1 if the movie contains at least one less frequent genre
    rare_genres = genre_dummies.columns.difference(main_genres)

    df["genre_Other"] = (genre_dummies[rare_genres].any(axis=1).astype(int))

    
    df["Country"] = (df["Country"].replace("Not Found", np.nan).astype("string").str.strip()
                    .str.replace(r"\[\s*\d+\s*\]", "", regex=True)
                    .str.extract(f"({country_pattern})", expand=False)
                    .str.strip())

    # Normalize country variants
    country_lower = df["Country"].str.lower().str.strip()

    df["Country"] = df["Country"].mask(
        country_lower.isin(["usa","us","u.s.","u.s.a.","united states","united states of america"]),"USA")

    df["Country"] = df["Country"].mask(country_lower.isin(["uk","united kingdom","england","britain","great britain"]),"UK")

    # Create country groups
    country_lower = df["Country"].str.lower().str.strip()

    country_mapping = {
        "usa": "USA",
        "uk": "UK",
        "france": "France",
        "india": "India",
        "italy": "Italy",
        "japan": "Japan",
        "canada": "Canada"
    }

    df["country_group"] = country_lower.map(country_mapping)

    # Known countries outside the selected groups become Other
    df.loc[
        df["Country"].notna() & df["country_group"].isna(),"country_group"] = "Other"

    # Country-related features
    df["country_known"] = df["Country"].notna().astype(int)


    # Invalid or post-2025 release years become missing values
    df["startYear"] = pd.to_numeric(df["startYear"], errors="coerce")

    df["startYear"] = df["startYear"].where(
        df["startYear"].between(1, 2025),
        np.nan
    )

    # Decade as a categorical feature
    df["decade"] = (((df["startYear"] // 10) * 10).astype("Int64").astype("string")+ "s").astype(object)

    # Number of genres
    df["num_genres"] = (df["genres"].astype("string").str.split(",").str.len().fillna(0).astype(int))

    # Number of lead actors
    df["num_lead_actors"] = (df["lead_actors_ids"].fillna("").astype(str).str.count(r"nm\d+").astype(int))


    df["directors_x_genres"] = (df["num_directors"] * df["num_genres"])

    df["film_age"] = 2026 - df["startYear"]

    df["age_x_country_known"] = (df["film_age"] * df["country_known"])

    # Remove unused columns and leakage features
    df = df.drop(columns=[
        "averageRating",
        "numVotes",
        "BoxOffice",
        "tconst",
        "primaryTitle",
        "lead_actors_ids",
        "plot",
        "Language",
        "Country",
        "directors",
        "directors_list",
        "startYear",
        "budget",
        "film_age",
        "genres"], 
        errors="ignore")

    # Convert categorical missing values to np.nan for sklearn compatibility
    categorical_cols = ["country_group", "decade"]

    df[categorical_cols] = (df[categorical_cols].astype(object).where(df[categorical_cols].notna(), np.nan))

    return df