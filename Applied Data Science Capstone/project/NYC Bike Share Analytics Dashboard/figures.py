import plotly.express as px
import plotly.graph_objects as go
import holoviews as hv
from holoviews.operation.datashader import datashade

# Set HoloViews to use the Plotly backend
hv.extension('plotly')

def create_activity_map(dff, map_type, mapbox_token):
    """
    Creates the main activity map.
    This version uses a robust "guard clause" structure to prevent errors.
    """
    px.set_mapbox_access_token(mapbox_token)
    # THE FIX: Handle the empty dataframe case first and exit immediately.
    # This is the cleanest way to prevent errors on empty selections.
    if dff.empty:
        fig = go.Figure(go.Scattermapbox()) # Create a blank map
        fig.update_layout(
            title_text="No data selected. Please broaden your filters.",
            mapbox_style="dark",
            mapbox_accesstoken=mapbox_token,
            mapbox_center_lon=-74,
            mapbox_center_lat=40.7,
            mapbox_zoom=9.5,
            margin={"r":0,"t":40,"l":0,"b":0}
        )
        return fig # Return the valid, empty figure

    # THE REASON: If we reach this point, we are guaranteed to have data.
    # Now we can safely proceed with the complex rendering logic.

    # Handle the 'datashader_heatmap' view
    if map_type == 'heatmap':
        
        fig = px.density_mapbox(
            dff, lat='start_lat', lon='start_lng',
            radius=10,
            center=dict(lat=40.7, lon=-74),
            color_continuous_scale= px.colors.sequential.Viridis, 
            opacity = 0.5,
            zoom=10,
            mapbox_style="dark",
            title="Heatmap of Trip Start Locations",
        )
    
    # Handle the 'routes' view
    else: # 'routes'
        route_counts = dff.groupby(['start_lat', 'start_lng', 'end_lat', 'end_lng']).size().reset_index(name='count')
        route_counts = route_counts.sort_values('count', ascending=False).head(100)
        
        fig = go.Figure() # Start with a fresh figure for the routes
        for _, row in route_counts.iterrows():
            fig.add_trace(go.Scattermapbox(
                mode="lines",
                lon=[row['start_lng'], row['end_lng']],
                lat=[row['start_lat'], row['end_lat']],
                line=dict(width=1 + row['count'] / route_counts['count'].max() * 4, color='#00aaff'),
                opacity=0.6,
                hoverinfo='none'
            ))
        
        fig.update_layout(
            title_text="Top 100 Popular Routes",
            mapbox_style="dark",
            mapbox_accesstoken=mapbox_token,
            mapbox_center_lon=-74,
            mapbox_center_lat=40.7,
            mapbox_zoom=9.5,
            showlegend=False,
            margin={"r":0,"t":40,"l":0,"b":0}
        )
        
    return fig


# --- No changes needed for the functions below ---

def create_user_pie_chart(dff):
    if dff.empty: return go.Figure()
    user_counts = dff['member_casual'].value_counts()
    fig = px.pie(values=user_counts.values, names=user_counts.index, title="User Type Breakdown", hole=0.4, color_discrete_sequence=['#007bff', '#17a2b8'])
    fig.update_layout(margin={"r":10,"t":40,"l":10,"b":10}, legend_x=0.5, legend_xanchor="center")
    return fig

def create_hourly_trend_chart(dff, overall_df):
    if dff.empty: return go.Figure()
    overall_avg_hourly = (overall_df['hour'].value_counts().sort_index() / len(overall_df['day_of_week'].unique())).round()
    selected_hourly = dff['hour'].value_counts().sort_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=selected_hourly.index, y=selected_hourly.values, name='Selected Period', marker_color='#007bff'))
    fig.add_trace(go.Scatter(x=overall_avg_hourly.index, y=overall_avg_hourly.values, name='Overall Daily Average', mode='lines+markers', line=dict(color='#dc3545', dash='dash')))
    fig.update_layout(xaxis_title="Hour of Day", yaxis_title="Number of Trips", legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01), xaxis=dict(tickmode='linear', dtick=2))
    return fig

def create_station_table_data(dff, station_type):
    if dff.empty: return [], []
    station_col = 'start_station_name' if station_type == 'start' else 'end_station_name'
    top_stations = dff[station_col].value_counts().reset_index().head(10)
    top_stations.columns = ['Station Name', 'Number of Trips']
    columns = [{"name": i, "id": i} for i in top_stations.columns]
    data = top_stations.to_dict('records')
    return data, columns