import dash
from dash import dcc, html, Input, Output
import sqlite3
import pandas as pd
import plotly.express as px

# Load data from SQLite
def load_data():
    conn = sqlite3.connect("mlb_history.db")
    df = pd.read_sql_query("SELECT * FROM mlb_history_1902", conn)

    conn.close()
    return df

df = load_data()

# Create list of years for dropdown
year_options = [{'label': str(year), 'value': year} for year in sorted(df['Year'].unique())]

# Initialize Dash app
app = dash.Dash(__name__)


app.layout = html.Div([
    html.H1("MLB History Dashboard"),

    html.Label("Select Year:"),
    dcc.Dropdown(
        id='year-dropdown',
        options=year_options,
        value=year_options[0]['value']
    ),

    html.Label("Table Slider (number of records):"),
    dcc.Slider(
        id='table-slider',
        min=1,
        max=100,
        step=1,
        value=20
    ),

    html.Div(id='table-container'),

    dcc.Graph(id='event-pie-chart'),
    dcc.Graph(id='year-bar-chart')
])


@app.callback(
    Output('table-container', 'children'),
    Output('event-pie-chart', 'figure'),
    Output('year-bar-chart', 'figure'),
    Input('year-dropdown', 'value'),
    Input('table-slider', 'value')
)
def update_dashboard(selected_year, num_records):
    filtered_df = df[df['Year'] == selected_year]

    
    table = html.Table([
        html.Tr([html.Th(col) for col in filtered_df.columns])
    ] + [
        html.Tr([html.Td(filtered_df.iloc[i][col]) for col in filtered_df.columns])
        for i in range(min(len(filtered_df), num_records))
    ])

   
    pie_fig = px.pie(filtered_df, names='Table', title='Event Types')

    
    bar_fig = px.histogram(df, x='Year', title='Records per Year')

    return table, pie_fig, bar_fig

# Run app
if __name__ == '__main__':
    app.run(debug=True)
