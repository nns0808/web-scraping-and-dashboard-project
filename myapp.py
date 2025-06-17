import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# Load cleaned data
df = pd.read_csv("mlb_history_1902_cleaned.csv")

# Create the Dash app
app = dash.Dash(__name__)
server = app.server 

# Bar chart of top 10 players by Value
fig = px.bar(
    df.sort_values(by="Value", ascending=False).head(10),
    x="Name",
    y="Value",
    color="Team",
    title="Top 10 MLB Players by Statistic Value (1902)"
)

# Layout
app.layout = html.Div([
    html.H1("1902 MLB Season Stats"),
    dcc.Graph(figure=fig),
    html.H2("Raw Data Table"),
    html.Div([
        dash.dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in df.columns],
            page_size=10,
            style_table={'overflowX': 'auto'},
        )
    ])
])

if __name__ == "__main__":
    app.run(debug=True)
