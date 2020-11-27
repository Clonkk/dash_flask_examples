import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_bootstrap_components as dbc
# Read more about DBC
# https://dash-bootstrap-components.opensource.faculty.ai/examples/
# https://dash-bootstrap-components.opensource.faculty.ai/docs/
# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/
import dash_html_components as html

from flask import Flask
from flask import render_template

import requests
import random

random.seed()

# You can use html directly here from python for layout
# Or you can use DBC Layout -> https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/
layout = html.Div(
    [
        dcc.Store(id="store-id", data=""),
        # Create div between components
        html.Div(
            [
                html.H1("Hello world !"),
                html.Hr(),
                html.P("This is some text using html layout through Dash"),
                html.Hr(),
                html.Hr(),
            ],
            style={"width": "90%", "float": "left"}
        ),
        html.Div([
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            children="I can write things here !",
                            id="card-id",
                            className="card-text",
                            color="primary",
                            inverse=True
                        ),
                        md=8
                        ),
                    dbc.Col(
                        dbc.Button("Click me !", id="button-id", className="mr-1"),
                        md=4
                        ),
                ],
            ),
            # Add a ling to the route 'catfacts'
            dbc.Row(
                [
                    dbc.NavbarSimple(
                        brand="Want some cat facts ? Click here !",
                        brand_href="/catfacts",
                        brand_external_link=True,
                        color="lightgreen",
                    ),
                ],
            ),
        ],
            # This is a Python dictionnary that contains CSS properties
            style={"width": "100%", "margin-left": "3rem", "float": "left"}
        )
    ],
    style={"width": "100%", "margin-left": "2rem"}
)

# Can download stylesheet from internet
#  external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# Can use predefined dbc themes
external_stylesheets = [dbc.themes.BOOTSTRAP]

# Create Flask server
server = Flask(__name__)  # necessary for video stream, which uses flask stream
# Create Dash application and pass Flask server as argument
app = dash.Dash(
    server=server,
    # Download a CSS style
    external_stylesheets=external_stylesheets,
)


# Example of routing a function
@app.server.route('/catfacts', methods=['GET', 'POST'])
def serve_template():
    text = cat_facts()
    # Fill a template with values
    # HTML template must be in templates/ folder at root level
    # Search for Jinja2 Template for more information
    return render_template("catfacts.html", text=text, catfact=cat_facts(), template="Flask")


# Example of using request library
def cat_facts():
    response = requests.get("http://cat-fact.herokuapp.com/facts")
    # This gives a JSON of a list of JSON
    # {
    #   "all": [{...}, {...}]
    # }
    dict_facts = response.json()["all"]
    rand_catfacts_idx = random.randrange(0, len(dict_facts)-1)
    text = dict_facts[rand_catfacts_idx]["text"]
    return text


@app.callback(
    [
        Output("card-id", "children")
    ],
    [
        Input("store-id", "data")
    ]
)
def updt_card(store_data):
    # Update card content every time store change
    print("store was updated")
    return [dbc.CardBody(children=store_data)]


@app.callback(
    [
        Output("store-id", "data")
    ],
    [
        Input("button-id", "n_clicks")
    ]
)
def button_cb(n_clicks):
    # Update data you store every 2 clicks
    if n_clicks is None:
        return dash.no_update

    result = dash.no_update
    if n_clicks % 2 == 0:
        result = "You clicked {0}".format(n_clicks)

    return [result]


app.layout = layout

app.run_server(port=36050, debug=True)
