import streamlit as st
import pandas as pd
import altair as alt

st.title("Exploring Illinois License Records")

st.write(
    "This app explores license records from the Fall 2022 dataset."
)

url = "https://raw.githubusercontent.com/UIUC-iSchool-DataViz/is445_data/main/licenses_fall2022.csv"

df = pd.read_csv(url)

df = df[["License Type", "License Status", "State", "County"]]

df = df[df["State"] == "IL"]

df = df.dropna(subset=["License Type", "License Status"])

st.write("Number of records:", len(df))

status_counts = df.groupby(
    ["License Type", "License Status"]
).size().reset_index(name="Count")



#License Status by Category
st.header("License Status by Category")

categories = df.groupby("License Type").size()

categories_selected = st.multiselect(
    "Which license categories do you want to view?",
    categories.index.values
)

if len(categories_selected) > 0:
    plot_data = status_counts[
        status_counts["License Type"].isin(categories_selected)
    ]
    chart_height = len(categories_selected) * 40 + 400
else:
    plot_data = status_counts
    chart_height = len(categories) * 40 + 400

status_order = df.groupby("License Status").size().index.values.tolist()

status_colors = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728",
    "#9467bd", "#8c564b", "#e377c2", "#7f7f7f",
    "#bcbd22", "#17becf", "#393b79", "#637939",
    "#a55194"
]

chart1 = alt.Chart(plot_data).mark_bar().encode(
    x=alt.X(
        "Count:Q",
        title="Number of records"
    ),
    y=alt.Y(
        "License Type:N",
        title="License category",
        sort="-x",
        axis=alt.Axis(labelLimit=300)
    ),
    color=alt.Color(
        "License Status:N",
        title="License status",
        scale=alt.Scale(
            domain=status_order,
            range=status_colors
        ),
        legend=alt.Legend(
            orient="bottom",
            columns=1,
            labelLimit=350
        )
    )
).properties(
    height=chart_height
)

st.altair_chart(chart1, use_container_width=True)

st.subheader("About the License Status Chart")
st.write("""
The first chart compares license record counts and status across categories.
I use horizontal stacked bars so viewers can compare both the total count
and the status breakdown. The count axis uses a linear scale starting at
zero, and the categories are sorted by total count. Colors separate the
license statuses rather than represent a numeric scale. The multiselect
lets users focus on smaller categories that are difficult to see beside
the largest ones. The chart height also changes with the number of selected
categories. These counts represent records in this dataset, not unique
people. With more time, I would add a percentage view to compare status
proportions across categories with different totals.
""")



#License Records by County
st.header("License Records by County")

county_df = df.dropna(subset=["County"])

counties = county_df.groupby("County").size()

counties_selected = st.multiselect(
    "Which counties do you want to view?",
    counties.index.values
)

if len(counties_selected) > 0:
    county_df = county_df[
        county_df["County"].isin(counties_selected)
    ]
else:
    county_df = county_df[
        county_df["County"].isin(
            ["COOK", "DUPAGE", "LAKE", "WILL"]
        )
    ]

st.write(
    "If no county is selected, the chart shows Cook, DuPage, "
    "Lake, and Will counties."
)

county_counts = county_df.groupby(
    ["County", "License Type"]
).size().reset_index(name="Count")

chart2 = alt.Chart(county_counts).mark_rect().encode(
    x=alt.X(
        "County:N",
        title="County",
        axis=alt.Axis(
            labelAngle=-45,
            labelLimit=200
        )
    ),
    y=alt.Y(
        "License Type:N",
        title="License category",
        axis=alt.Axis(labelLimit=300)
    ),
    color=alt.Color(
        "Count:Q",
        title="Number of records",
        scale=alt.Scale(scheme="blues", type="log")
    )
).properties(
    height=650
)

st.altair_chart(chart2, use_container_width=True)

st.write(
    "Darker cells show more records. The color scale is logarithmic "
    "to make differences between smaller counts easier to see. "
    "Blank cells mean there are no matching records in this dataset. "
    "Records with missing county names are excluded from this chart."
)

st.subheader("About the County Heatmap")
st.write("""
The second chart compares license record counts across counties and
license categories. I use a heatmap because it shows many combinations
in a compact space. Both axes show categories, and darker blue cells
represent larger counts. The sequential blue color scheme fits the
ordered numeric values. I use a logarithmic color scale because the
counts vary widely, making smaller differences easier to see. Users can
select counties to compare, while blank cells indicate no matching
records in this dataset. Records without county names are excluded.
The color scale adjusts to the selected data, so colors should be read
with the legend. With more time, I would add county population data to
compare records per resident instead of only raw counts.
""")

#Comparison with Homework 5
st.header("Comparison with Homework 5")

st.write("""
Homework 5 used UFO reports to show counts by shape and changes over time.
This assignment uses a different dataset about license records.
The first chart still uses horizontal bars, but it plots different
variables and stacks the counts by license status. The second chart
uses a heatmap to compare counties and license categories.
No write-up text or completed plots were copied from Homework 5.
""")

st.write(
    "Source: https://raw.githubusercontent.com/UIUC-iSchool-DataViz/"
    "is445_data/main/licenses_fall2022.csv"
)

st.write(
    "License statuses reflect the Fall 2022 dataset, not current status."
)