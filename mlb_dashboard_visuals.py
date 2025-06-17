import sqlite3
import pandas as pd
import ast
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# Load data from SQLite
conn = sqlite3.connect('mlb_history.db')
df_raw = pd.read_sql_query("SELECT * FROM mlb_history_1902", conn)
conn.close()

# Parse RowData into structured records
records = []
for index, row in df_raw.iterrows():
    try:
        data_list = ast.literal_eval(row['RowData'])  # Safely convert string to list
        if len(data_list) >= 4 and data_list[0] != 'Statistic':
            records.append({
                "Year": row['Year'],
                "Event": row['Event'],
                "Table": row['Table'],
                "Statistic": data_list[0],
                "Player": data_list[1],
                "Team": data_list[2],
                "Value": data_list[3]
            })
    except Exception:
        continue

df = pd.DataFrame(records)

# Convert 'Value' to numeric (NaN if not a number)
df['Value'] = pd.to_numeric(df['Value'], errors='coerce')

# Filter out non-numeric statistics
valid_stats = df.groupby('Statistic')['Value'].apply(lambda x: x.notna().all())
filtered_stats = valid_stats[valid_stats].index.tolist()

# Build Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("MLB History 1902 Dashboard"),

    html.Label("Select Statistic:"),
    dcc.Dropdown(
        id='stat-dropdown',
        options=[{'label': stat, 'value': stat} for stat in filtered_stats],
        value=filtered_stats[0] if filtered_stats else None
    ),

    dcc.Graph(id='stat-graph'),
])

@app.callback(
    Output('stat-graph', 'figure'),
    Input('stat-dropdown', 'value')
)
def update_graph(selected_stat):
    filtered_df = df[df['Statistic'] == selected_stat].sort_values(by='Value', ascending=False)

    if filtered_df.empty:
        return {
            'data': [],
            'layout': {
                'title': f"{selected_stat} (1902)",
                'xaxis': {'title': 'Player'},
                'yaxis': {'title': 'Value'},
                'annotations': [{
                    'text': 'No data available',
                    'xref': 'paper',
                    'yref': 'paper',
                    'showarrow': False,
                    'font': {'size': 18}
                }]
            }
        }

    # Create separate bar traces per team to show legend
    traces = []
    for team in filtered_df['Team'].unique():
        team_data = filtered_df[filtered_df['Team'] == team]
        traces.append(go.Bar(
            x=team_data['Player'],
            y=team_data['Value'],
            name=team,
            showlegend=True
        ))

    fig = go.Figure(data=traces)
    fig.update_layout(
        title=f"{selected_stat} (1902)",
        xaxis_title='Player',
        yaxis_title='Value',
        legend_title='Team'
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True)
