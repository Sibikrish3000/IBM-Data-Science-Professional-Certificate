from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import html

# Import our figure-generating functions
from figures import (
    create_activity_map,
    create_user_pie_chart,
    create_hourly_trend_chart,
    create_station_table_data
)

def register_callbacks(app, df, mapbox_token):
    @app.callback(
        [
            Output('kpi-row', 'children'),
            Output('activity-map', 'figure'),
            Output('user-type-pie', 'figure'),
            Output('top-stations-table', 'data'),
            Output('top-stations-table', 'columns'),
            Output('hourly-trend-bar', 'figure')
        ],
        [
            Input('day-dropdown', 'value'),
            Input('hour-slider', 'value'),
            Input('map-type-toggle', 'value'),
            Input('station-type-toggle', 'value')
        ]
    )
    def update_dashboard(selected_days, hour_range, map_type, station_type):
        # Ensure selected_days is a list
        if not selected_days: # Handle empty selection
            selected_days = []
        elif not isinstance(selected_days, list):
            selected_days = [selected_days]

        # Filter data based on controls
        dff = df[
            df['day_of_week'].isin(selected_days) &
            (df['hour'] >= hour_range[0]) &
            (df['hour'] <= hour_range[1])
        ].copy()

        # --- Generate KPIs ---
        if dff.empty:
            kpi_cards = [dbc.Col(dbc.Alert("No data for this selection.", color="warning"), width=12)]
        else:
            total_trips = len(dff)
            avg_duration = dff['trip_duration_min'].mean()
            total_dist = dff['distance_km'].sum()
            kpi_cards = [
                dbc.Col(dbc.Card(dbc.CardBody([html.H4(f"{total_trips:,}", className="card-title"), html.P("Total Trips")])), className="kpi-card", md=4),
                dbc.Col(dbc.Card(dbc.CardBody([html.H4(f"{avg_duration:.1f} min", className="card-title"), html.P("Avg. Duration")])), className="kpi-card", md=4),
                dbc.Col(dbc.Card(dbc.CardBody([html.H4(f"{total_dist:,.0f} km", className="card-title"), html.P("Total Distance")])), className="kpi-card", md=4),
            ]
        
        # --- Generate Figures by calling functions from figures.py ---
        fig_map = create_activity_map(dff, map_type, mapbox_token)
        fig_pie = create_user_pie_chart(dff)
        table_data, table_cols = create_station_table_data(dff, station_type)
        fig_bar = create_hourly_trend_chart(dff, df) # Pass original df for overall average

        return kpi_cards, fig_map, fig_pie, table_data, table_cols, fig_bar