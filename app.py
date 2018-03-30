# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
from scipy.stats import binom
import plotly.graph_objs as go

app = dash.Dash()

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

description = '''
### Background
The statistical analysis associated with the triangle test compares the proportion of test participants whom have correctly identified an odd beer out, to the proportion of tasters that would be expected to correctly identify the odd beer purely due to random chance. The greater the proportion of correct participants, the more evidence there is against the “random chance” null hypothesis. As we are only interested if the different beers can be correctly distinguished, this will be an “upper tailed” test. That is to say, the potential result of the odd beer out being correctly identified less than we’d expect under random chance isn’t of particular interest to us.

In plain terms, our null hypothesis is that the true proportion of population that can correctly identify the odd beer out is 1/3. Our alternative hypothesis is that the true proportion of the population that can correctly identify the odd beer out is greater than 1/3.

### Exact p-value
The exact p-value can be calculated using the binomial distribution. Specifically, the p-value is found as the probability of having observed at least as many correct tasters, if the population proportion is infact equal to 1/3. This calculation is implemented in the right pane of this web app.

### Approximate p-value
An approximate p-value can also be calculated assuming that under the null hypothesis, the estimated proportion will follow a normal distribution with mean equal to 1/3, and variance equal to (2/(9 * n)), where n is the sample size. This approximate method may be used when the sample size is large (at least 25), thanks to Central Limit Theorem.
'''


attribution = '''
Built by [Justin Angevaare](http://onuncertainty.com) with [Plot.ly Dash](https://dash.plot.ly)
'''


app.layout = html.Div(className = 'twelve columns', children=[
    html.Div(className='row', children=[
        html.Center(
            html.H1('Triangle Test Calculator')
            )
        ]),
    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            dcc.Markdown(children=description)
            ]), # end of left side
        html.Div(className='six columns', children=[
            html.Div(className='row', children=[
                dcc.Graph(id='plot')
                ]), # end of row
            html.Div(className='row', children=[
                html.Div(className='four columns', children=[
                    html.Label('Number of participants'),
                    dcc.Input(id='size', type='number', value=20)
                    ]),
                html.Div(className='four columns', children=[
                    html.Label('Number of correct participants'),
                    dcc.Input(id='correct', type='number', value=10)
                    ]),
                html.Div(className='four columns', children=[
                    html.Br(),
                    html.Button('Submit', id='button')
                    ])
                ]), # end of row
            html.Div(className='row', children=[
                html.H3(id='exact')
                ]) # end of row
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
            title='',
            barmode='stack',
            showlegend=False,
            bargap = 0.0,
            yaxis = dict(fixedrange = True),
            xaxis = dict(fixedrange = True)
            )
        )


@app.callback(
    Output(component_id='exact', component_property='children'),
    [Input(component_id='button', component_property='n_clicks')],
    [State(component_id='size', component_property='value'),
    State(component_id='correct', component_property='value')]
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
