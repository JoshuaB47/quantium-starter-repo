## outline for this code courtesy of https://dash.plotly.com/layout

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import csv
import time

# returns list of [preChangeSalesRate, postChangeSalesRate]
def getSalesData():
    totalPreSales = 0
    totalPostSales = 0
    preDates = set()
    postDates = set()
    cutOffDate = time.strptime("2021-01-15", "%Y-%m-%d")
    with open("munged.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # if it's after or the day of the change
            if time.strptime(row["date"], "%Y-%m-%d") >= cutOffDate:
                totalPostSales += float(row["sales"])
                postDates.add(row["date"])
            else:
                totalPreSales += float(row["sales"])
                preDates.add(row["date"])
    return [round(totalPreSales / len(preDates), 2), round(totalPostSales / len(postDates), 2)]

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Time Period": ["Before", "After"],
    "Sales of Pink Morsels Per Day": getSalesData(),
    "Time": ["Before January 15th, 2021", "After January 15th, 2021"]
})

fig = px.bar(df, x="Time Period", y="Sales of Pink Morsels Per Day", color="Time", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Pink Morsel Sales Per Day: Comparing Pre- and Post- Jan 15, 2021'),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run(debug=True)
