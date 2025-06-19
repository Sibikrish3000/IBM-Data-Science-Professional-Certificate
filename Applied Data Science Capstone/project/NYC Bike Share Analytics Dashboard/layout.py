from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from data import load_and_prepare_data

# Load data once to populate dropdowns
df = load_and_prepare_data()
days_ordered = df['day_of_week'].cat.categories

# Define the app layout
layout = dbc.Container([
    # Header
    dbc.Row(
        dbc.Col(html.H1("NYC Bike Share Analytics Dashboard", className="header"), width=12),
        className="mb-4 mt-4"
    ),
    
    # Control Panel
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Filters"),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Label("Day of Week"),
                        dcc.Dropdown(
                            id='day-dropdown',
                            options=[{'label': day, 'value': day} for day in days_ordered],
                            value=list(days_ordered), # Default to all days
                            multi=True
                        )
                    ], md=4),
                    dbc.Col([
                        html.Label("Time of Day (Hour Window)"),
                        dcc.RangeSlider(id='hour-slider', min=0, max=23, step=1,
                                        marks={i: str(i) for i in range(0, 24, 2)},
                                        value=[0, 23])
                    ], md=8),
                ])
            ])
        ], className="content-card"), width=12)
    ], className="mb-4"),

    # KPIs Row
    dbc.Row(id='kpi-row', className="mb-4"),

    # Main Visuals Row
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader([
                "Trip Activity Map",
                dbc.RadioItems(
                    id='map-type-toggle',
                    options=[
                        {'label': 'Heatmap', 'value': 'heatmap'},
                        {'label': 'Routes', 'value': 'routes'},
                    ],
                    value='heatmap', inline=True, className="float-end"
                )
            ]),
            dbc.CardBody(dcc.Graph(id='activity-map', style={'height': '60vh'}))
        ], className="content-card"), lg=7),

        dbc.Col([
            dbc.Card(dcc.Graph(id='user-type-pie', style={'height': '30vh'}), className="content-card mb-4"),
            dbc.Card([
                dbc.CardHeader([
                    "Busiest Stations",
                     dbc.RadioItems(
                        id='station-type-toggle',
                        options=[{'label': 'Start', 'value': 'start'}, {'label': 'End', 'value': 'end'}],
                        value='start', inline=True, className="float-end"
                    )
                ]),
                dbc.CardBody(dash_table.DataTable(
                    id='top-stations-table',
                    style_cell={'textAlign': 'left', 'fontFamily': 'sans-serif'},
                    style_header={'backgroundColor': '#f8f9fa', 'fontWeight': 'bold'},
                    style_table={'overflowY': 'auto', 'height': '21vh'}
                ))
            ], className="content-card")
        ], lg=5)
    ], className="mb-4"),
    
    # Hourly Trend Row
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Hourly Trip Trends vs. Daily Average"),
            dbc.CardBody(dcc.Graph(id='hourly-trend-bar'))
        ], className="content-card"), width=12)
    ])
], fluid=True)