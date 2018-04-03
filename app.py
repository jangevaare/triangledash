# -*- coding: utf-8 -*-
import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
from scipy.stats import binom
import plotly.graph_objs as go
import os
from random import randint

server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
app = dash.Dash(__name__, server=server)

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

description = '''
### Background
The statistical analysis associated with the triangle test compares the proportion of test participants that have correctly identified an odd sample out, to the proportion of tasters that would be expected to correctly identify the odd sample purely due to random chance. The greater the proportion of correct participants, the more evidence there is against the “random chance” null hypothesis. As we are only interested if the different beers can be correctly distinguished, this will be an “upper tailed” test. That is to say, the potential result of the odd sample out being correctly identified less than we’d expect under random chance isn’t of relevance.

In plain terms, our null hypothesis, Η₀, is that the true proportion of population that can correctly identify the odd sample out is 1/3. Our alternative hypothesis, H₁, is that the true proportion of the population that can correctly identify the odd sample out is greater than 1/3.

### Exact p-value
The exact p-value can be calculated using the binomial distribution. Specifically, the p-value is found as the probability of having observed at least as many correct tasters, if the population proportion is infact equal to 1/3. This calculation is implemented in the right pane of this web app.

### Approximate p-value
An approximate p-value can also be calculated assuming that under the null hypothesis, the sample proportion will follow a normal distribution with mean equal to 1/3 and variance equal to 2/(9*n), where n is the sample size. This approximate method may be used when the sample size is large (at least 25), thanks to Central Limit Theorem.
'''


attribution = '''
Built by [Justin Angevaare](http://onuncertainty.com) with [Plot.ly Dash](https://dash.plot.ly)
'''

app.title = 'TriangleDash'
app.layout = html.Div(className = 'twelve columns', children=[
html.Script(type="text/javascript", src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"),
    html.Div(className='row', children=[
        html.Center(
            html.H1('TriangleDash: Triangle Test Calculator and Utilities')
            )
        ]),
    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            dcc.Markdown(children=description)
            ]), # end of left side
        html.Div(className='six columns', children=[
            html.H3('Calculator'),
            html.Div(className='row', children=[
                html.Div(className='five columns', children=[
                    html.Label('Number of participants:', style={'verticalAlign':'middle'})
                    ]),
                html.Div(className='seven columns', style={'textAlign': 'left'}, children=[
                    dcc.Input(id='size', type='number', value=20)
                    ])
                ]),
                html.Br(),
                html.Div(className='row', children=[
                    html.Div(className='five columns', children=[
                        html.Label('Number of correct participants:', style={'verticalAlign':'middle'})
                        ]),
                    html.Div(className='seven columns', style={'textAlign': 'left'}, children=[
                        dcc.Input(id='correct', type='number', value=10)
                        ])
                    ]),
            html.Div(className='row', style={'text-align': 'left'}, children=[
                html.Br(),
                html.Button('Submit', id='button')
                ]),
            html.Div(className='row', children=[
                html.H3('Result'),
                dcc.Graph(id='plot')
                ])
            ]) # end of right side
        ]),
    html.Div(className='row', children=[
        html.Br(),
        html.Br(),
        html.Center(
            html.Small(
                dcc.Markdown(children=attribution)
                )
            )
        ]) # end of row
    ]) # end of app layout


@app.callback(
    Output(component_id='plot', component_property='figure'),
    [Input(component_id='button', component_property='n_clicks')],
    [State(component_id='size', component_property='value'),
    State(component_id='correct', component_property='value')]
    )
def makeplot(clicks, n, correct):
    if n > 0:
        n += 1
    return go.Figure(
        data = [
            go.Bar(
                y = binom.pmf(range(0, correct, 1), n, 1/3),
                x = list(range(0, correct, 1)),
                hoverinfo='none'
                ),
            go.Bar(
                y = binom.pmf(range(correct, n+1, 1), n, 1/3),
                x = list(range(correct, n+1, 1)),
                hoverinfo='none'
                )],
        layout = go.Layout(
            title=exactp(clicks, n, correct),
            barmode='stack',
            showlegend=False,
            bargap = 0.0,
            yaxis = dict(fixedrange = True,
                         title='Event probability under H₀'),
            xaxis = dict(fixedrange = True,
                         title='Number of correct participants'),
            )
        )

def exactp(clicks, n, correct):
    if n == 0:
        return "Must have at least one participant"
    elif correct > n:
        return "The number of correct participants can not exceed the total number of participants"
    else:
        return "Exact p-value: {:.4f}".format(1-binom.cdf(correct-1, n, 1/3))


if __name__ == '__main__':
    app.run_server(debug=True)
