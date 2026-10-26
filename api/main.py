
# Aplikacja do prognozowania cen mieszkań
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException


# Utworzenie aplikacji FastAPI
app = FastAPI(title="Prognozowanie cen mieszkań")


# Wczytanie wytrenowanego modelu
folder_projektu = Path(__file__).resolve().parent.parent
sciezka_modelu = folder_projektu / "models" / "model_cen_mieszkan.joblib"

model = joblib.load(sciezka_modelu)


# Strona główna API
@app.get("/")
def strona_glowna():
    return {"message": "API do prognozowania cen mieszkań działa"}


# Endpoint do prognozowania ceny domu
@app.post("/predict")
def przewidz_cene(dane: dict):
    try:
        # Przygotowanie danych wejściowych
        mieszkanie = pd.DataFrame([dane])

        # Utworzenie dodatkowych cech
        mieszkanie["Total Area"] = (
            mieszkanie["Gr Liv Area"]
            + mieszkanie["Total Bsmt SF"].fillna(0)
        )

        mieszkanie["House Age"] = (
            mieszkanie["Yr Sold"] - mieszkanie["Year Built"]
        ).clip(lower=0)

        # Sprawdzenie wymaganych kolumn
        wymagane_cechy = model.feature_names_in_
        brakujace = set(wymagane_cechy) - set(mieszkanie.columns)

        if brakujace:
            raise ValueError(
                f"Brakuje wymaganych cech: {sorted(brakujace)}"
            )

        # Ustawienie kolumn w odpowiedniej kolejności
        mieszkanie = mieszkanie[list(wymagane_cechy)]

        # Prognozowanie ceny
        cena = model.predict(mieszkanie)[0]

        return {
            "prognozowana_cena_usd": round(float(cena), 2)
        }

    except ValueError as blad:
        raise HTTPException(
            status_code=422,
            detail=str(blad)
        )
