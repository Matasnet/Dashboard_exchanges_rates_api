# Aplikacja do Analizy Kursów Walut

## Opis
Jest to interaktywna aplikacja webowa do analizy historycznych i bieżących kursów wymiany walut, stworzona przy użyciu frameworka Dash. Aplikacja umożliwia wybór walut oraz zakresu dat w celu wyświetlenia tabeli kursów wymiany, porównania wielu walut oraz przeprowadzenia analizy statystycznej i predykcji przyszłych kursów.

## Funkcje
- **Kurs wymiany**: Umożliwia wybór dwóch walut oraz zakresu dat w celu wyświetlenia tabeli kursów wymiany. Dane mogą być pobrane jako plik CSV.
- **Porównanie wielu walut**: Pozwala na porównanie kursów bazowej waluty względem wielu innych walut w wybranym zakresie dat. Wyniki są wyświetlane w formie wykresu.
- **Analiza statystyczna i predykcja**: Oferuje statystyczną analizę wybranych walut oraz przewidywanie przyszłych kursów na podstawie regresji liniowej.

## Technologie
- **Język programowania**: Python
- **Framework**: Dash
- **Biblioteki**: Pandas, scikit-learn, Plotly, Requests
- **Źródło danych**: [Frankfurter API](https://api.frankfurter.app)

## Instalacja
1. Skopiuj repozytorium:
    ```bash
    git clone https://github.com/TwojeRepozytorium/analiza-kursow-walut.git
    ```
2. Przejdź do katalogu projektu:
    ```bash
    cd analiza-kursow-walut
    ```
3. Zainstaluj wymagane biblioteki:
    ```bash
    pip install -r requirements.txt
    ```

## Uruchomienie
Aby uruchomić aplikację, wykonaj poniższe polecenie:
```bash
python app.py
