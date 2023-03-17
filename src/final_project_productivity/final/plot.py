"""Functions plotting results."""
import plotly.graph_objs as go
import plotly.io as pio
import pandas as pd
from PIL import Image
import os


def plot_prod(plot_df, sector_df, prod_measure = "TFP", amount_of_sectors=10, from_year=1993):
    """
    Plots the level of a given production measure over time for the specified number of largest sectors in the economy.
    
    Args:
    - plot_df: A pandas DataFrame in wide format with columns 'year' and columns for each sector's level of the production measure.
    - sector_df: A pandas DataFrame with one column of sector names in the same format as the sector names used in plot_df.
    - prod_measure: The production measure to plot, defaults to "TFP". "LP" also available.
    - amount_of_sectors: The number of largest sectors to include in the plot, defaults to 10.
    - from_year: The first year to include in the plot, defaults to 1993.
    
    Returns:
    - fig: A plotly Figure object containing the line plot of the specified production measure over time.
    """
    plot_df = plot_df[plot_df['year'] >= from_year]
    starts_with = f'level_{prod_measure}'

    sectors = sector_df.values.tolist()
    sectors = [item[0] for item in sectors]
    sectors = sectors[:amount_of_sectors]

    cols = [col for col in plot_df.columns if col.startswith(starts_with) and any(sector in col for sector in sectors)] 
    

    fig = go.Figure()
    for col in cols:
        col_name = col.replace(f'{starts_with}_', "")
        fig.add_trace(go.Scatter(x=plot_df['year'], y=plot_df[col], name=col_name, mode='lines',line=dict(width=2)))

    fig.update_layout(title={'font': {'family': 'HelveticaNeue-CondensedBold, Helvetica, Sans-serif',
                        'size':20,
                        'color': '#333'},
                        'text' : f'Level {prod_measure} for Each Year',
                        'x' : 0.5,
                        'y' : 0.95,
                        'xanchor': 'center',
                        'yanchor': 'top'},
                    xaxis_title='Years',
                    yaxis_title=f'Level {prod_measure}',
                    legend_orientation='h',
                    legend=dict(
                        y=-0.2,
                        borderwidth=0.5),
                    hovermode='x unified',
                    height=800,
                    width=800,
                    xaxis=dict(
                        showline=True,
                        showgrid=False,
                        showticklabels=True,
                        linecolor='black',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='black')
                    ),
                    yaxis=dict(
                        showline=True,
                        showgrid=False,
                        showticklabels=True,
                        linecolor='black',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                                family='Arial',
                                size=12,
                                color='black')
                        ),
                    plot_bgcolor='rgba(191, 186, 142, 0.2)',
                    paper_bgcolor='rgba(191, 186, 142, 0.2)',
                    shapes=[{
                            'type': 'line',
                            'x0': 0,
                            'y0': 100,
                            'x1': 1,
                            'y1': 100,
                            'xref': 'paper',
                            'yref': 'y',
                            'line': {
                                'color': 'black',
                                'width': 1,
                                'dash': 'dot',
                            }
                    }]
                )

    return fig


def plot_sector_data(data, sector, country_names, layout, productivity="level_TFP"):
    """
    Create a line plot of a given sector's data over time for different countries using Plotly.

    Args:
        data (pd.DataFrame): A DataFrame containing the sector's data over time
        sector (str): The name of the sector to plot
        country_names (list): A list of country names to include in the plot
        layout (str): File path to an image file to use as the plot background
        productivity (str, optional): The type of productivity data to plot. Defaults to "level_TFP".

    Returns:
        plotly.graph_objs._figure.Figure: A Plotly figure object representing the line plot.
    """

    data = pd.read_csv(data)
    data.set_index('year', inplace=True)
    sector = f'{productivity}_{sector}'

    # Extract the columns we want to plot
    columns = [f'{sector} {country}' for country in country_names]
    data = data[columns]

    colors = ['#1616A7', '#F6222E', '#FBE426']

    image_file = layout
    pil_image = Image.open(image_file)
    image = go.layout.Image(
    source=pil_image,
    xref="paper", yref="paper",
    x=0, y=1,
    sizex=1, sizey=1,
    sizing = "fill",
    opacity=0.5,
    layer="below",
                )

    # Create a list of traces for each country's data
    traces = []
    for i, country in enumerate(country_names):
        trace = go.Scatter(
            x=data.index,
            y=data[f'{sector} {country}'],
            name=country,
            line=dict(color=colors[i])
        )
        traces.append(trace)

    # Create the plot layout
    layout = go.Layout(
        images=[image],
        title=sector,
        xaxis=dict(title='Year', 
                   color="black", 
                   showgrid=False, 
                   showline=True, 
                   linecolor='black'),
        yaxis=dict(title='Index (base year 2000 = 100)', 
                   color="black", 
                   showgrid=False, 
                   showline=True, 
                   linecolor='black'),
        plot_bgcolor='rgba(191, 186, 142, 0.8)',
        paper_bgcolor='rgba(191, 186, 142, 0.8)',
        shapes=[{
                            'type': 'line',
                            'x0': 0,
                            'y0': 100,
                            'x1': 1,
                            'y1': 100,
                            'xref': 'paper',
                            'yref': 'y',
                            'line': {
                                'color': 'black',
                                'width': 1,
                                'dash': 'dot',
                            }
                    }]
    )

    # Create the plot figure and display it
    fig = go.Figure(data=traces, layout=layout)
    return fig

