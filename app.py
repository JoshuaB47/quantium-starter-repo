# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd

# lol, using the .read_csv builtin of pandas could be cool
data =pd.read_csv("munged.csv")
data = data.sort_values(by="date")
print(data.columns.values)
app = Dash(__name__)



# create the header
header = html.H1(
    "Pink Morsel Sales Data",
    id="header"
)

# our 5 radio options for regions. We want all to be the default
radioOptions =\
    dcc.RadioItems(["north", "south", "east", "west", "all"],
                   "all",
                   id='region')

checkBoxRounding = dcc.Checklist(["Want a Moving Average?"], id="rounding")
sliderForWindow = dcc.Slider(0, 31, 1,
               value=7,
               id='rollingLength'
                )
# want the header then visualization
app.layout = html.Div(children=[
    header,
    radioOptions,
    checkBoxRounding,
    sliderForWindow,
    dcc.Graph(id="visualization")
])

@callback(
    Output('visualization', 'figure'),
    Input('region', 'value'),
    Input('rounding', 'value'),
    Input('rollingLength', 'value'))
def makeVisualization(regionToDisplay, roundBool, rollingLength):
    xDay = int(rollingLength)
    # if we're looking at all, take sum of all regions
    if regionToDisplay == "all":
        # sum all data from same date
        newData = data.groupby("date", as_index=False)["sales"].sum()
        # if we want a xDay day moving average
        if roundBool:
            newData["sales"] = newData["sales"].rolling(window=xDay, min_periods=0).mean()
        line_chart = px.line(newData, x="date", y="sales", title="Pink Morsel sale for all regions")

        line_chart.update_layout()

        return line_chart
    else:
        # only look at data that corresponds to the proper region
        newData = data[data["region"] == regionToDisplay]
        # if we want a xDay day moving average
        if roundBool:
            # take the xDay day average for sales
            newData["sales"] = newData["sales"].rolling(window=xDay, min_periods=0).mean()
        line_chart = px.line(newData, x="date", y="sales", title="Pink Morsel sale for the " + regionToDisplay + " region")

        line_chart.update_layout()
        return line_chart


if __name__ == '__main__':
    app.run_server()
