import os
import re

import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px



app = dash.Dash(__name__)


## ------ Get files list ------
pattern = '^solution_([a-zA-Z0-9]*).csv$'
list_dates = []

for filename in os.listdir('output'):
    ans = re.findall(pattern=pattern, string=filename)
    if len(ans) == 1:
        list_dates.append(ans[0])

assert len(list_dates) != 0, "Pas de données correctes trouvées dans le dossier data !"

## ------ Widgets ------

date_dropdown = dcc.Dropdown(
        id='date-dropdown',
        options=[
            {'label': date, 'value': date} for date in list_dates
        ],
        value=list_dates[0]
    )





## ------ Layout ------

app.layout = html.Div([
    dcc.Graph(id="scatter-plot"),
    date_dropdown
])

@app.callback(
    Output("scatter-plot", "figure"), 
    [Input("date-dropdown", "value")])
def update_bar_chart(value):
    date = value
    filename = f'solution_{date}.csv'

    df_ans = pd.read_csv(os.path.join('output', filename))

    fig = px.scatter(df_ans, x='x', y='y', color='Catégorie',
            hover_name='Siège',
            size='Poids',
            hover_data=df_ans.columns,
            title="Visualisation de la solution optimale",
            template="plotly_white")

    fig.update_traces(marker=dict(line=dict(width=2,
                                            color='DarkSlateGrey')),
                    selector=dict(mode='markers'))
    return fig

app.run_server(debug=True)