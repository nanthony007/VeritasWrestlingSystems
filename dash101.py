import dash
import dash_core_components as dcc 
import dash_html_components as html
import pandas as pd 
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import dash_daq as daq

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
from django.contrib.auth.models import User
from vws_main.models import FS_Match, FS_Wrestler

df = pd.read_csv('collection/stats/matchdata.csv')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash('Dash101 App', external_stylesheets=external_stylesheets)

user = User.objects.first()
roster1 = user.profile.roster.all()
match_qs = []
for wrestler in roster1:
    match_qs.append(wrestler.focus_wrestler2.values())
matches = pd.concat([pd.DataFrame(match_qs[i].values()) for i in range(len(match_qs))], ignore_index=True)


app._layout = html.Div([
    html.H1('Dash 101!'), 

    html.Label('Multi-Select Dropdown'),
    dcc.Dropdown(
        id='dropdown1',
        options=[ 
            ({'label': w, 'value':w}) for w in matches.focus_id.unique()
        ] ,
        value=[],
        multi=True,
    ),
    dcc.Graph(
        id='graph1',
    ),
])

@app.callback(
    Output('graph1', 'figure'), [Input('dropdown1', 'value')]
)
def update_graph1(input_names): 
    filtered_df = matches[matches.focus_id.isin(input_names)]
    traces = []
    for w in filtered_df.weight.unique():
        traces.append(go.Scatter(
            x=filtered_df[filtered_df['weight']==w]['result'],
            y=filtered_df[filtered_df['weight']==w]['npf'],
            text=filtered_df[filtered_df['weight']==w]['focus_id'].iloc[0],
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
            xaxis={'title': 'Neutral Pace Factor'},
            yaxis={'title': 'Action per Minute'},
            margin={'l': 50, 'b': 25, 't': 25, 'r': 50},
            legend={'x': 1.1, 'y': 0.5},
            hovermode='closest'
        ),
    }


if __name__ == '__main__':
    app.run_server(debug=True)