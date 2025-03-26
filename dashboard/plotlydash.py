from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import requests
import os
from io import StringIO
import plotly.express as px
from datetime import datetime

app = Dash(__name__)

# Используем имя сервиса из docker-compose
API_URL = os.getenv('DJANGO_API_URL', 'http://127.0.0.1:8000/api/hardware/')

def fetch_hardware_data():
    try:
        print(f"Попытка подключения к: {API_URL}")
        response = requests.get(API_URL, params={'format': 'csv'}, timeout=10)
        response.raise_for_status()
        
        df = pd.read_csv(StringIO(response.text))
        # Преобразуем дату в datetime для лучшей сортировки
        df['release_date'] = pd.to_datetime(df['release_date'])
        print(f"Успешно загружено {len(df)} записей")
        return df
        
    except Exception as e:
        print(f"Ошибка подключения: {str(e)}")
        return pd.DataFrame()

app.layout = html.Div([
    html.H1("Анализ аппаратных компонентов", style={'textAlign': 'center'}),
    html.Button("Обновить данные", id="refresh-btn", style={'margin': '10px'}),
    
    dcc.Dropdown(
        id='graph-type',
        options=[
            {'label': 'Распределение по категориям', 'value': 'category'},
            {'label': 'Топ самых дорогих товаров', 'value': 'top_price'},
            {'label': 'Зависимость цены от мощности', 'value': 'price_power'},
            {'label': 'Новинки по дате выхода', 'value': 'newest'},
            {'label': 'Сравнение цен по производителям', 'value': 'manufacturer_price'}
        ],
        value='category',
        style={'width': '80%', 'margin': '10px auto'}
    ),
    
    dcc.Graph(id='hardware-graph', style={'height': '600px'}),
    
    html.H3("Данные продуктов", style={'marginTop': '30px'}),
    dash_table.DataTable(
        id='table',
        page_size=10,
        style_table={'overflowX': 'auto', 'margin': '10px'},
        style_cell={'textAlign': 'left', 'padding': '10px'},
        style_header={
            'backgroundColor': 'lightgrey',
            'fontWeight': 'bold'
        }
    )
])

@callback(
    [Output('table', 'data'),
     Output('hardware-graph', 'figure')],
    [Input('refresh-btn', 'n_clicks'),
     Input('graph-type', 'value')]
)
def update_content(n, graph_type):
    df = fetch_hardware_data()
    
    if df.empty:
        return [], {}
    
    # Создаем график в зависимости от выбранного типа
    if graph_type == 'category':
        fig = px.sunburst(
            df, 
            path=['category', 'manufacturer'], 
            values='price',
            title='Распределение продуктов по категориям и производителям',
            color='price',
            color_continuous_scale='Blues'
        )
    elif graph_type == 'top_price':
        top_products = df.sort_values('price', ascending=False).head(10)
        fig = px.bar(
            top_products,
            x='name',
            y='price',
            color='category',
            title='Топ 10 самых дорогих продуктов',
            labels={'price': 'Цена ($)', 'name': 'Название продукта'}
        )
    elif graph_type == 'price_power':
        fig = px.scatter(
            df,
            x='power_consumption',
            y='price',
            color='category',
            size='price',
            hover_name='name',
            title='Зависимость цены от потребляемой мощности',
            labels={'price': 'Цена ($)', 'power_consumption': 'Потребляемая мощность (Вт)'}
        )
    elif graph_type == 'newest':
        newest = df.sort_values('release_date', ascending=False).head(10)
        fig = px.bar(
            newest,
            x='name',
            y='release_date',
            color='manufacturer',
            title='Последние выпущенные продукты',
            labels={'release_date': 'Дата выпуска', 'name': 'Название продукта'}
        )
    elif graph_type == 'manufacturer_price':
        fig = px.box(
            df,
            x='manufacturer',
            y='price',
            color='manufacturer',
            title='Распределение цен по производителям',
            labels={'price': 'Цена ($)', 'manufacturer': 'Производитель'}
        )
    else:
        fig = {}
    
    return df.to_dict('records'), fig

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)