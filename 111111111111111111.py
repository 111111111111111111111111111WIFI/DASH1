import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_table

# Загрузка данных из файла
file_path = 'C:/Users/xttna/PycharmProjects/pythonProject2/12.csv'  # Замените на путь к вашему файлу
df = pd.read_csv(file_path)

# Преобразование столбцов с датами
df['Transaction Date'] = pd.to_datetime(df['Transaction Date'])
df['Delivery Date'] = pd.to_datetime(df['Delivery Date'], errors='coerce')
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')

# Создание экземпляра приложения
app = dash.Dash(__name__)

# Определение структуры дашборда
app.layout = html.Div([
    html.H1('Данные транзакции', style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='time-period-dropdown',
        options=[
            {'label': 'Месяц', 'value': 'M'},
            {'label': 'Квартал', 'value': 'Q'},
            {'label': 'Год', 'value': 'Y'}
        ],
        value='M',
        clearable=False,
        style={'width': '50%', 'margin': '0 auto'}
    ),
    dcc.Graph(id='time-series-chart'),
    dcc.Graph(id='pie-chart'),
    dcc.Graph(id='histogram'),
    dcc.Graph(id='scatter-plot'),
    html.Div(id='data-table')
], style={'padding': '20px'})

# Определение логики дашборда
@app.callback(
    Output('time-series-chart', 'figure'),
    Output('pie-chart', 'figure'),
    Output('histogram', 'figure'),
    Output('scatter-plot', 'figure'),
    Output('data-table', 'children'),
    [Input('time-period-dropdown', 'value')]
)
def update_charts(selected_time_period):
    # Фильтрация и агрегация данных в соответствии с выбранным периодом
    filtered_df = df.resample(selected_time_period, on='Transaction Date')['Quantity'].sum().reset_index()

    # Проверка наличия данных после агрегации
    if filtered_df.empty:
        return dash.no_update  # Возвращает текущее состояние, если данные отсутствуют

    # Линейный график
    time_series_chart = px.line(filtered_df, x='Transaction Date', y='Quantity', title='Временной ряд')

    # Круговая диаграмма
    pie_chart = px.pie(df, names='Transaction Type', title='Распределение типов сделок')

    # Гистограмма
    histogram = px.histogram(df, x='Unit Price', title='Распределение цен за единицу')

    # Точечный график
    scatter_plot = px.scatter(df, x='Quantity', y='Unit Price', title='Корреляция между Количеством и Ценой за Единицу')