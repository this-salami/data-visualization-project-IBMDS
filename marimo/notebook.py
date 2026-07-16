import marimo

__generated_with = "0.23.14"
app = marimo.App(
    width="full",
    app_title="Data Visualization - IBMDS",
)


@app.cell
async def _():
    import sys

    deps_ready = True
    if sys.platform == "emscripten":
        import micropip

        await micropip.install(["plotly"])

    return (deps_ready,)


@app.cell
def _(deps_ready):
    import marimo as mo
    import pandas as pd
    import plotly.express as px
    return mo, pd, px

@app.cell
def _(mo):
    mo.Html("""<style>
        html, body {
            margin: 0;
            padding: 0;
            height: 100%;
            width: fit-content;

            overflow-y: hidden;
            overflow-x: scroll;
        }

        #root {
            overflow: visible;
        }

        #root > .contents > div {
            min-width: 1200px;
        }
            
        #App {
            overflow: scroll;
            width: 100%;
        }
    </style>""")

@app.cell
def _(pd):
    data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/d51iMGfp_t0QpO30Lym-dw/automobile-sales.csv')
    year_list = sorted(data["Year"].unique().tolist())
    return data, year_list


@app.cell
def _(mo, year_list):
    title = mo.md("# Automobile Sales Statistics Dashboard")
    report_type = mo.ui.dropdown(
        options=["Yearly Statistics", "Recession Period Statistics"],
        value="Yearly Statistics",
        label="Select Statistics",
    )
    return report_type

@app.cell
def _(mo, year_list, report_type, title):
    year = mo.ui.dropdown(
        options=year_list,
        value=year_list[-1],
        label="Select Year",
        disabled=report_type.value == "Recession Period Statistics",
    )
    controls = mo.hstack([report_type, year], justify="start", gap=2)
    if report_type.value == "Recession Period Statistics":
        controls = mo.hstack([report_type], justify="start", gap=2)

    mo.vstack([title, controls], gap=1)
    return report_type, year


@app.cell
def _(data, px, report_type, year, pd):
    selected_statistics = report_type.value
    selected_year = year.value
    r_chart1 = r_chart2 = r_chart3 = r_chart4 = None
    y_chart1 = y_chart2 = y_chart3 = y_chart4 = None

    if selected_statistics == "Recession Period Statistics":
        recession_data = data[data["Recession"] == 1]

        yearly_rec = recession_data.groupby("Year")["Automobile_Sales"].mean().reset_index()
        r_chart1 = px.line(
            yearly_rec,
            x="Year",
            y="Automobile_Sales",
            title="Average Automobile Sales Fluctuation Over <br>Recession Period",
        )

        average_sales = (
            recession_data.groupby("Vehicle_Type")["Automobile_Sales"].mean().reset_index()
        )
        r_chart2 = px.bar(
            average_sales,
            x="Vehicle_Type",
            y="Automobile_Sales",
            title="Average Automobile Sales by Vehicle Type <br>During Recession Period",
        )

        exp_rec = (
            recession_data.groupby("Vehicle_Type")["Advertising_Expenditure"].sum().reset_index()
        )
        r_chart3 = px.pie(
            exp_rec,
            names="Vehicle_Type",
            values="Advertising_Expenditure",
            title="Total Advertising Expenditure by Vehicle Type <br>During Recession Period",
        )

        unemp_data = (
            recession_data.groupby(["unemployment_rate", "Vehicle_Type"])["Automobile_Sales"]
            .mean()
            .reset_index()
        )
        r_chart4 = px.bar(
            unemp_data,
            x="unemployment_rate",
            y="Automobile_Sales",
            color="Vehicle_Type",
            labels={
                "unemployment_rate": "Unemployment Rate",
                "Automobile_Sales": "Average Automobile Sales",
            },
            title="Effect of Unemployment Rate on Vehicle Type and Sales",
        )
    else:
        yearly_data = data[data["Year"] == selected_year]

        yas = data.groupby("Year")["Automobile_Sales"].mean().reset_index()
        y_chart1 = px.line(
            yas,
            x="Year",
            y="Automobile_Sales",
            title="Yearly Automobile Sales",
        )

        mas_total = data.groupby("Month")["Automobile_Sales"].sum().reset_index().rename(columns={"Automobile_Sales": "Total_Automobile_Sales"})
        mas_this = yearly_data.groupby("Month")["Automobile_Sales"].sum().reset_index().rename(columns={"Automobile_Sales": f"{selected_year}_Automobile_Sales"})
        mas = pd.merge(mas_total, mas_this, on="Month").set_index("Month").reindex(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]).reset_index()
        y_chart2 = px.line(
            mas,
            x="Month",
            y=["Total_Automobile_Sales", f"{selected_year}_Automobile_Sales"],
            title="Total Monthly Automobile Sales",
        )

        avr_vdata = yearly_data.groupby("Vehicle_Type")["Automobile_Sales"].mean().reset_index()
        y_chart3 = px.bar(
            avr_vdata,
            x="Vehicle_Type",
            y="Automobile_Sales",
            title=f"Avg. Vehicles Sold by Vehicle Type in {selected_year}",
        )

        exp_data = yearly_data.groupby("Vehicle_Type")["Advertising_Expenditure"].sum().reset_index()
        y_chart4 = px.pie(
            exp_data,
            names="Vehicle_Type",
            values="Advertising_Expenditure",
            title=f"Total Advertisement Expenditure by Vehicle Type in {selected_year}",
        )

    return selected_statistics, r_chart1, r_chart2, r_chart3, r_chart4, y_chart1, y_chart2, y_chart3, y_chart4


@app.cell
def _(mo, selected_statistics, r_chart1, r_chart2, r_chart3, r_chart4):
    recessionElems = []
    if selected_statistics == "Recession Period Statistics":
        recessionElems.append(
            mo.hstack([mo.ui.plotly(r_chart1), mo.ui.plotly(r_chart2)], widths="equal")
        )
        recessionElems.append(
            mo.hstack([mo.ui.plotly(r_chart3), mo.ui.plotly(r_chart4)], widths="equal")
        )
    else:
        pass
    mo.vstack(recessionElems, gap=2)


@app.cell
def _(mo, selected_statistics, y_chart1, y_chart2, y_chart3, y_chart4):
    yearlyElems = []
    if selected_statistics == "Yearly Statistics":
        yearlyElems.append(
            mo.hstack([mo.ui.plotly(y_chart1), mo.ui.plotly(y_chart2)], widths="equal")
        )
        yearlyElems.append(
            mo.hstack([mo.ui.plotly(y_chart3), mo.ui.plotly(y_chart4)], widths="equal")
        )
    else:
        pass
    mo.vstack(yearlyElems, gap=2)


if __name__ == "__main__":
    app.run()
