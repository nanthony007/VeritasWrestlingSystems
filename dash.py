import dash
import dash_core_components as dcc 
import dash_html_components as html
import pandas as pd 
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import dash_daq as daq
from django_plotly_dash import DjangoDash

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
from django.contrib.auth.models import User
from vws_main.models import FS_Match, FS_Wrestler


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = DjangoDash('Dash101', external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1('Dash 101!'), 

    html.Label('Graph1'),
    dcc.Dropdown(
        id='dropdown1',  
        options=[],
        value=[],
        multi=True,
        placeholder="Select a wrestler",
    ),
    dcc.Graph(
        id='graph1',
    ),
])

@app.expanded_callback(
    Output('graph1', 'figure'), 
    [Input('dropdown1', 'value')]
)
def update_graph1(*args, **kwargs): 
    user_qs = kwargs['user']
    u = User.objects.get(username=user_qs)
    r = u.profile.roster.all()
    match_qs = []
    for wrestler in r:
        match_qs.append(wrestler.focus_wrestler2.values())
    matches = pd.concat([pd.DataFrame(match_qs[i].values()) for i in range(len(match_qs))], ignore_index=True)
    traces = []
    for w in matches.weight.unique():
        traces.append(go.Scatter(
            x=matches[matches['weight']==w]['result'],
            y=matches[matches['weight']==w]['npf'],
            text=matches[matches['weight']==w]['focus_id'].iloc[0],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 10,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=str(w)+'kgs',
        )
    )

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'Result'},
            yaxis={'title': 'Neutral Pace Factor'},
            margin={'l': 50, 'b': 25, 't': 25, 'r': 50},
            legend={'x': 1.1, 'y': 0.5},
            hovermode='closest'
        ),
    }

# @app.expanded_callback(
#     dash.dependencies.Output("dropdown1", "options"),
#     [dash.dependencies.Input("dropdown1", "value")],
# )
# def update_options(*args, **kwargs):
#     user_qs = kwargs['user']
#     u = User.objects.get(username=user_qs)
#     r = u.profile.roster.all()
#     wnames = []
#     for w in r:
#         wnames.append(w.name) 
#     return sorted([{'label': w, 'value':w} for w in wnames], key=lambda x: x['label'])

