import dash
import dash_bootstrap_components as dbc

# Import our modularized components
from data import load_and_prepare_data
from layout import layout
from callbacks import register_callbacks

# --- Configuration ---
# You need a Mapbox token for the map visualizations.
# Get a free one from https://www.mapbox.com/
MAPBOX_TOKEN = 'pk.eyJ1Ijoic2liaWtyaXNoIiwiYSI6ImNtYzNtdzdxajA2eWQyanF0bHhieDYxbmIifQ.2f7wyNwdiPE2ifnFlZAXsw'

# --- App Initialization ---
# The 'assets_folder' is automatically set to 'assets'
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# --- Data Loading ---
df = load_and_prepare_data("bike_trips_data.parquet")

# --- App Layout ---
app.layout = layout

# --- Register Callbacks ---
# We pass the app instance and the dataframe to the callback registration function
register_callbacks(app, df, MAPBOX_TOKEN)

# --- Run the App ---
if __name__ == '__main__':
    app.run(debug=True)