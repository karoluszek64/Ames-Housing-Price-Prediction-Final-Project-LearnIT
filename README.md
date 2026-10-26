# Ames Housing: Prognozowanie cen nieruchomości

**Projekt dyplomowy z kursu LearnIT Data Science**

## Opis projektu

Celem projektu jest przewidywanie cen sprzedaży domów w Ames w stanie Iowa (USA) na podstawie informacji o nieruchomościach. Projekt obejmuje analizę danych, przygotowanie cech, porównanie modeli regresyjnych oraz udostępnienie prognoz przez API.

Projekt ma charakter edukacyjny. Prognozy modelu nie stanowią profesjonalnej wyceny nieruchomości.

## Cele projektu

1. Poznanie danych i przeprowadzenie analizy eksploracyjnej (EDA).
2. Oczyszczenie danych i przygotowanie cech do modelowania.
3. Porównanie skuteczności modeli regresyjnych.
4. Wybór i dostrojenie najlepszego modelu.
5. Ocena wyników i analiza najważniejszych cech.
6. Przygotowanie kalkulatora cen nieruchomości w formie API i uruchomienie go w kontenerze Docker.

## Umiejętności wykorzystane w projekcie

Projekt realizuje założenia kursu w obszarach **regresji, feature engineering i interpretowalności modeli**. Obejmuje przewidywanie wartości liczbowej, tworzenie dodatkowych cech nieruchomości oraz analizę znaczenia cech i błędów prognoz.

Zgodnie z założeniami dotyczącymi wdrożenia przygotowano **kalkulator cen nieruchomości w formie API**.

## Zbiór danych

Wykorzystano zbiór **Ames Housing**, zawierający informacje o domach sprzedanych w Ames w stanie Iowa. Zmienną przewidywaną jest `SalePrice`, czyli cena sprzedaży nieruchomości w dolarach amerykańskich.

Podczas przygotowania danych utworzono dodatkowe cechy, między innymi `Total Area` (łączna powierzchnia) oraz `House Age` (wiek domu). Identyfikatory `PID` i `Order` pominięto podczas modelowania.

## Metodologia

Dane podzielono na zbiór treningowy (80%) i testowy (20%). Porównano cztery modele: DummyRegressor, regresję liniową, Random Forest oraz Gradient Boosting. Do oceny modeli zastosowano pięciokrotną walidację krzyżową, a dla wybranego modelu przeprowadzono strojenie hiperparametrów za pomocą `RandomizedSearchCV`.

Eksperymenty rejestrowano w MLflow. Sprawdzono również, które cechy mają największy wpływ na prognozy oraz dla jakich nieruchomości model popełnia większe błędy.

## Wyniki

Najlepszym modelem końcowym został **Gradient Boosting Regressor**. Po strojeniu uzyskano następujące wyniki na zbiorze testowym:

| Metryka | Wynik |
| --- | ---: |
| MAE | **14 511,48 USD** |
| RMSE | **24 338,01 USD** |
| R² | **0,9261** |

Średnie błędy MAE z pięciokrotnej walidacji krzyżowej na danych treningowych:

| Model | Średnie MAE CV (USD) |
| --- | ---: |
| Gradient Boosting | **14 735,43** |
| Random Forest | 15 994,11 |
| Regresja liniowa | 16 512,79 |
| DummyRegressor | 56 104,00 |

Największe znaczenie dla prognoz miały ogólna jakość nieruchomości (`Overall Qual`) i jej łączna powierzchnia (`Total Area`). Większe błędy występowały między innymi przy części droższych domów.

**Ograniczenie:** zbiór testowy wykorzystano wcześniej do porównania modeli, dlatego końcowy wynik nie jest całkowicie niezależną oceną jakości modelu.

## Green IT

Porównano czas trenowania, wielkość zapisanych modeli oraz ich dokładność. Gradient Boosting okazał się korzystnym rozwiązaniem pod względem jakości prognoz i wykorzystania zasobów. Trenowanie tego modelu w porównaniu Green IT trwało około **2,35 s**, a zapisany model zajmował około **0,152 MB**. Nie wykonywano bezpośredniego pomiaru zużycia energii.

## Notebooki i kalkulator cen

**`01_data_cleaning.ipynb`** przedstawia wczytanie danych, sprawdzenie ich jakości, czyszczenie i przygotowanie zbioru do dalszej analizy.

**`02_analysis_and_modeling.ipynb`** zawiera analizę eksploracyjną, tworzenie nowych cech, porównanie i strojenie modeli regresyjnych, interpretację wyników, eksperymenty MLflow oraz analizę Green IT.

**`api/main.py`** zawiera aplikację FastAPI pełniącą funkcję kalkulatora cen nieruchomości. Po przesłaniu danych domu aplikacja korzysta z wytrenowanego modelu i zwraca przewidywaną cenę w USD. Dodatkowo oblicza cechy `Total Area` i `House Age`. Przykładowe dane znajdują się w pliku `data/przykladowy_dom.json`.

**Gdzie znajduje się kalkulator?** Po lokalnym uruchomieniu aplikacji `api/main.py` jest dostępny w dokumentacji interaktywnej pod adresem [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). W sekcji `POST /predict` można wybrać `Try it out`, wkleić dane przykładowego domu i otrzymać prognozę. Kalkulator działa jako API, a nie osobna strona internetowa z formularzem.

**`Dockerfile`** zawiera konfigurację kontenera umożliwiającego uruchomienie tego samego kalkulatora w środowisku Docker. Po zbudowaniu obrazu i uruchomieniu kontenera z mapowaniem portu 8001 na 8000 dokumentacja API jest dostępna pod adresem [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs).

API sprawdzono lokalnie oraz w Dockerze. W obu przypadkach przykładowe zapytanie zakończyło się odpowiedzią HTTP 200 i prognozą **177 809,45 USD**.

## Podsumowanie

Projekt pokazuje pełny proces tworzenia modelu regresyjnego, od przygotowania danych i oceny wyników po udostępnienie kalkulatora cen w FastAPI i Dockerze. Uzyskane wyniki są obiecujące w ramach analizowanego zbioru, jednak model wymagałby dodatkowej walidacji przed zastosowaniem w rzeczywistym procesie wyceny nieruchomości.
