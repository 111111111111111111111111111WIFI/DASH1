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
