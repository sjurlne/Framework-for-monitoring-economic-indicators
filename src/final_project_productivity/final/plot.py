"""Functions plotting results."""
import plotly.graph_objs as go
import pandas as pd

def plot_prod(plot_df, sector_df, prod_measure = "TFP", amount_of_sectors=10):
    """Takes a data frame in wide format, and creates plot over the given amount of largest sectors in the economy.
    """
    
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