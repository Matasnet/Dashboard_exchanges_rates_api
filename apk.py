import dash
from dash import dcc, html, Input, Output, State, dash_table
import requests
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import date

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Pobieranie dostępnych walut z API
response = requests.get('https://api.frankfurter.app/currencies')
currencies = response.json()

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    html.H2('Dash Tab Template'),

    dcc.Tabs(
        id='tabs-1',
        children=[
            dcc.Tab(label='Home', value='tab-1'),
            dcc.Tab(label='Kurs wymiany', value='tab-2'),
            dcc.Tab(label='Porównanie wielu walut', value='tab-3'),
            dcc.Tab(label='Analiza statystyczna i predykcja', value='tab-4'),
        ],
        value='tab-1'
    ),

    html.Div(id='div-1'),
    html.Footer([
        'Created by ', 
        html.A('Matasnet', href='https://www.linkedin.com/in/mateusz-kozera/', target='_blank')
    ], style={
        'position': 'relative', 
        'bottom': '0', 
        'width': '100%', 
        'background-color': '#f1f1f1', 
        'text-align': 'center', 
        'padding': '10px 0'
    }),

])

@app.callback(
    Output('div-1', 'children'),
    [Input('tabs-1', 'value')]
)
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Witamy w aplikacji do analizy kursów walut!'),
            html.P('Ta aplikacja umożliwia analizę historycznych kursów wymiany walut oraz przewidywanie przyszłych kursów. Dane są pobierane z API Frankfurter, które dostarcza dokładne i aktualne informacje na temat kursów walutowych.'),
            html.H4('Funkcje aplikacji:'),
            html.Ul([
            html.Li([html.B('Kurs wymiany: '), html.Span('Umożliwia wybór dwóch walut oraz zakresu dat w celu wyświetlenia tabeli kursów  wymiany. Dane mogą być pobrane jako plik CSV.')]),
            html.Li([html.B('Porównanie wielu walut: '), html.Span('Pozwala na porównanie kursów bazowej waluty względem wielu innych walut  w wybranym zakresie dat. Wyniki są wyświetlane w formie wykresu.')]),
            html.Li([html.B('Analiza statystyczna i predykcja: '), html.Span('Oferuje statystyczną analizę wybranych walut oraz  przewidywanie przyszłych kursów na podstawie regresji liniowej.')])
            ]),
            html.H4('Instrukcje użytkowania:'),
            html.Ol([
                html.Li('Wybierz zakładkę, która Cię interesuje.'),
                html.Li('Wypełnij wymagane pola (waluty, zakres dat).'),
                html.Li('Kliknij przycisk pobierania CSV, jeśli chcesz pobrać dane w formacie CSV (dotyczy zakładki "Kurs wymiany").'),
                html.Li('Czekaj na załadowanie wyników - dane zostaną przedstawione w formie tabeli lub wykresu.'),
            ]),
            html.H4('Źródło danych:'),
            html.P([
            'Dane są pobierane ze strony ', 
            html.A('Frankfurter API', href='https://api.frankfurter.app', target='_blank'), 
            ', która dostarcza aktualne i historyczne kursy wymiany walut.']),
            html.H4('Dostępne waluty:'),
            html.P(f'Dostępne waluty: {", ".join(currencies.keys())}'),
        ])

    elif tab == 'tab-2':
        return html.Div([
            html.H3('Wybierz waluty i zakres dat'),
            dcc.Dropdown(
                id='currency-1-dropdown',
                options=[{'label': key, 'value': key} for key in currencies.keys()],
                value='USD',
                placeholder='Wybierz pierwszą walutę'
            ),
            dcc.Dropdown(
                id='currency-2-dropdown',
                options=[{'label': key, 'value': key} for key in currencies.keys()],
                value='EUR',
                placeholder='Wybierz drugą walutę'
            ),
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date='2022-01-01',
                end_date=date.today(),
                display_format='YYYY-MM-DD'
            ),
            html.Div(id='error-message', style={'color': 'red'}),
            html.Button("Pobierz CSV", id="btn-download-csv"),
            dcc.Download(id="download-csv"),
            dcc.Loading(
                id='loading-div-2',
                children=[
                    dash_table.DataTable(id='exchange-rate-table')
                ],
                type='circle'
            )
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Porównanie wielu walut'),
            dcc.Dropdown(
                id='base-currency-dropdown',
                options=[{'label': key, 'value': key} for key in currencies.keys()],
                value='USD',
                placeholder='Wybierz walutę bazową'
            ),
            dcc.Dropdown(
                id='compare-currencies-dropdown',
                options=[{'label': key, 'value': key} for key in currencies.keys()],
                multi=True,
                placeholder='Wybierz waluty do porównania'
            ),
            dcc.DatePickerRange(
                id='compare-date-picker-range',
                start_date='2022-01-01',
                end_date=date.today(),
                display_format='YYYY-MM-DD'
            ),
            dcc.Loading(
                id='loading-div-3',
                children=[
                    dcc.Graph(id='comparison-graph')
                ],
                type='circle'
            )
        ])
    elif tab == 'tab-4':
        return html.Div([
            html.H3('Analiza statystyczna i predykcja'),
            dcc.Dropdown(
                id='stats-currency-1-dropdown',
                options=[{'label': key, 'value': key} for key in currencies.keys()],
                value='USD',
                placeholder='Wybierz pierwszą walutę'
            ),
            dcc.Dropdown(
                id='stats-currency-2-dropdown',
                options=[{'label': key, 'value': key} for key in currencies.keys()],
                value='EUR',
                placeholder='Wybierz drugą walutę'
            ),
            dcc.DatePickerRange(
                id='stats-date-picker-range',
                start_date='2022-01-01',
                end_date=date.today(),
                display_format='YYYY-MM-DD'
            ),
            dcc.Loading(
                id='loading-div-4',
                children=[
                    html.Div(id='stats-output'),
                    dcc.Graph(id='prediction-graph')
                ],
                type='circle'
            )
        ])

@app.callback(
    Output('exchange-rate-table', 'data'),
    Output('exchange-rate-table', 'columns'),
    Output('error-message', 'children'),
    Output('download-csv', 'data'),
    [Input('currency-1-dropdown', 'value'),
     Input('currency-2-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('btn-download-csv', 'n_clicks')],
    [State('currency-1-dropdown', 'value'),
     State('currency-2-dropdown', 'value'),
     State('date-picker-range', 'start_date'),
     State('date-picker-range', 'end_date')]
)
def update_exchange_rate_table(currency1, currency2, start_date, end_date, n_clicks, currency1_state, currency2_state, start_date_state, end_date_state):
    if currency1 == currency2:
        return [], [], "Wybrane waluty muszą być różne.", None
    
    if currency1 and currency2 and start_date and end_date:
        url = f'https://api.frankfurter.app/{start_date}..{end_date}?from={currency1}&to={currency2}'
        response = requests.get(url)
        data = response.json()
        
        rates = data['rates']
        dates = list(rates.keys())
        exchange_rates = [rates[date][currency2] for date in dates]
        df = pd.DataFrame({'Data': dates, f'Kurs {currency1} do {currency2}': exchange_rates})
        
        if n_clicks is not None:
            return df.to_dict('records'), [{'name': i, 'id': i} for i in df.columns], "", dcc.send_data_frame(df.to_csv, "exchange_rates.csv")
        
        return df.to_dict('records'), [{'name': i, 'id': i} for i in df.columns], "", None
    
    return [], [], "Wybierz waluty i zakres dat", None

@app.callback(
    Output('comparison-graph', 'figure'),
    [Input('base-currency-dropdown', 'value'),
     Input('compare-currencies-dropdown', 'value'),
     Input('compare-date-picker-range', 'start_date'),
     Input('compare-date-picker-range', 'end_date')]
)
def update_comparison_graph(base_currency, compare_currencies, start_date, end_date):
    if base_currency and compare_currencies and start_date and end_date:
        data = []
        for currency in compare_currencies:
            url = f'https://api.frankfurter.app/{start_date}..{end_date}?from={base_currency}&to={currency}'
            response = requests.get(url)
            rates = response.json()['rates']
            dates = list(rates.keys())
            exchange_rates = [rates[date][currency] for date in dates]
            data.append({'x': dates, 'y': exchange_rates, 'type': 'line', 'name': f'Kurs {base_currency} do {currency}'})
        
        return {
            'data': data,
            'layout': {
                'title': f'Porównanie kursów wymiany {base_currency} do wybranych walut',
                'xaxis': {'title': 'Data'},
                'yaxis': {'title': 'Kurs wymiany'},
            }
        }
    return {
        'data': [],
        'layout': {
            'title': 'Wybierz waluty i zakres dat',
            'xaxis': {'title': 'Data'},
            'yaxis': {'title': 'Kurs wymiany'},
        }
    }

@app.callback(
    Output('stats-output', 'children'),
    Output('prediction-graph', 'figure'),
    [Input('stats-currency-1-dropdown', 'value'),
     Input('stats-currency-2-dropdown', 'value'),
     Input('stats-date-picker-range', 'start_date'),
     Input('stats-date-picker-range', 'end_date')]
)
def update_stats_and_prediction(currency1, currency2, start_date, end_date):
    if currency1 == currency2:
        return html.Div("Wybrane waluty muszą być różne"), {
            'data': [],
            'layout': {
                'title': 'Wybierz waluty i zakres dat',
                'xaxis': {'title': 'Data'},
                'yaxis': {'title': 'Kurs wymiany'},
            }
        }
    
    if currency1 and currency2 and start_date and end_date:
        url = f'https://api.frankfurter.app/{start_date}..{end_date}?from={currency1}&to={currency2}'
        response = requests.get(url)
        data = response.json()
        
        rates = data['rates']
        dates = list(rates.keys())
        exchange_rates = [rates[date][currency2] for date in dates]
        df = pd.DataFrame({'Data': dates, 'Kurs wymiany': exchange_rates})
        
        X = np.array(range(len(dates))).reshape(-1, 1)
        y = np.array(exchange_rates).reshape(-1, 1)
        model = LinearRegression().fit(X, y)
        pred = model.predict(X)
        
        df['Predykcja'] = pred.flatten()
        
        fig = {
            'data': [
                {'x': dates, 'y': exchange_rates, 'type': 'line', 'name': 'Kurs wymiany'},
                {'x': dates, 'y': pred.flatten(), 'type': 'line', 'name': 'Predykcja'}
            ],
            'layout': {
                'title': f'Predykcja kursu {currency1} do {currency2}',
                'xaxis': {'title': 'Data'},
                'yaxis': {'title': 'Kurs wymiany'},
            }
        }
        
        mean = df['Kurs wymiany'].mean()
        median = df['Kurs wymiany'].median()
        std = df['Kurs wymiany'].std()

        stats_output = html.Div([
            html.P(f"Średni kurs: {mean:.2f}"),
            html.P(f"Mediana kursu: {median:.2f}"),
            html.P(f"Odchylenie standardowe: {std:.2f}")
        ])
        
        return stats_output, fig
    
    return html.Div("Wybierz waluty i zakres dat"), {
        'data': [],
        'layout': {
            'title': 'Wybierz waluty i zakres dat',
            'xaxis': {'title': 'Data'},
            'yaxis': {'title': 'Kurs wymiany'},
        }
    }

if __name__ == '__main__':
    app.run_server(debug=False)
