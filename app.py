import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import sqlite3

# Load data from SQLite
conn = sqlite3.connect("fleet_data.db")
df = pd.read_sql_query("SELECT * FROM vehicle_data ORDER BY timestamp", conn)
conn.close()

# Add alert flags
df['Alert'] = df['fuel_level'].apply(lambda x: 'LOW FUEL' if x < 15 else '')

# Create Dash app
app = dash.Dash(__name__)

# Line graphs
fig_speed = px.line(df, x="timestamp", y="speed", color="vehicle_id", title="Vehicle Speed Over Time")
fig_fuel = px.line(df, x="timestamp", y="fuel_level", color="vehicle_id", title="Fuel Level Over Time")

# Layout
app.layout = html.Div([
    html.H1("Fleet Diagnostic Dashboard", style={"textAlign": "center"}),

    dcc.Graph(figure=fig_speed),
    dcc.Graph(figure=fig_fuel),

    html.Div([
        html.H3("Fuel Alerts (Below 15%)"),
        html.Ul([
            html.Li(f"{row.vehicle_id}: {row.fuel_level:.1f}% — {row.Alert}", style={"color": "red"})
            for _, row in df[df['Alert'] != ''].iterrows()
        ])
    ])
])

# Run app
if __name__ == "__main__":
    app.run(debug=True)
