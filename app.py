#import libraries for visualization
import pandas as pd
import plotly.express as px 
import streamlit as st
from traitlets.traitlets import default



#As a first step, we setup basic configuration of web app (default layout = centered)
st.set_page_config(page_title="Video Games Sales Dashboard",page_icon=":video_game:",layout="wide")

df = pd.read_csv('VideoGames_Sales.csv',header=0, encoding='unicode_escape')



#---SIDEBAR---
st.sidebar.header("Made by Kunal Yadav :smile:")
st.sidebar.header("Please Filter Here:")

#Platform selection
plat = st.sidebar.multiselect(
    "Select/Remove Platforms:",
    options=df["Platform"].unique(),
    default=df["Platform"].unique(),
)

#Genre selection
genre = st.sidebar.multiselect(
    "Select/Remove Genres:",
    options=df["Genre"].unique(),
    default=df["Genre"].unique(),
)

#Select the filtered dataset
df_selection = df.query(
    "Platform == @plat & Genre == @genre"
)



#---MAINPAGE---#
st.title(":chart_with_upwards_trend: Video Games Sales Dashboard")
st.markdown("##")

#Details of data
total_games = int(df_selection.shape[0])
total_genres=int(df["Genre"].unique().shape[0])
total_platforms=int(df["Platform"].unique().shape[0])
total_sales=df["Global_Sales"].sum()

#Display data as a table (vertically parallel) 
left_column, middle_column, right_column, rightmost_column = st.columns(4)
with left_column:
    st.subheader("Total Video Games:")
    st.subheader(f"{total_games:,}")
with middle_column:
    st.subheader("Number of Genres:")
    st.subheader(f"{total_genres}")
with right_column:
    st.subheader("Number of Platforms:")
    st.subheader(f"{total_platforms}")
with rightmost_column:
    st.subheader("Total Sales in Millions:")
    st.subheader(f"{total_sales}")

st.markdown("""---""")


#DISPLAY DATA IF CHECKBOX IS TICKED
check = st.checkbox("Select to show data!")
if check:
    st.dataframe(df_selection)



#---HISTOGRAMS---
#HISTOGRAM - GENRE WISE DISTRIBUTION
fig_genre_dist = px.histogram(df_selection["Genre"], 
    title="<b>Genre Wise Sales Distribution</b>", 
    color_discrete_sequence=["#0067B7"],
    template="plotly_dark",
)

fig_genre_dist.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

#HISTOGRAM - PLATFORM WISE DISTRIBUTION
fig_plat_dist = px.histogram(df_selection["Platform"],
    title="<b>Platform Wise Sales Distribution</b>",
    color_discrete_sequence=["#0067B7"],
    template="plotly_dark",)

fig_plat_dist.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

#DISPLAY HISTOGRAMS
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_genre_dist, use_container_width=True)
right_column.plotly_chart(fig_plat_dist, use_container_width=True)



#---BAR GRAPH---
#BAR GRAPH - GENRE WISE AVERAGE SALES FOR EVERY REGION
st.header("Genre-wise average sales based on region")
region_names = ["Global_Sales", "NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]
chosen_region = st.radio("Select the region of which you want to see average sales:", region_names)

#Select average sales genre wise for chosen region
df_region_selection=df_selection.groupby(by=["Genre"]).mean()[chosen_region]

#Bargraph for the same 
fig_avg_sales=px.bar(
    df_region_selection,
    x=chosen_region,
    y=df_region_selection.index,
    labels={chosen_region : f"Average {chosen_region} in Millions"},
    orientation="h",
    title=f"<b>Genre-Wise Average {chosen_region}",
    color_discrete_sequence=["#0067B7"]*len(df_region_selection),
    template="plotly_dark",
)
fig_avg_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

#Display graph alongside data
left_column, middle_column, right_column = st.columns(3)
left_column.plotly_chart(fig_avg_sales)
with right_column:
    st.dataframe(df_region_selection)




#---PIE CHARTS---
#PIE CHART - Sales by Region
total_regions=["NA_Sales","EU_Sales","JP_Sales","Other_Sales"]
total_values=[]
for i in total_regions:
    total_values.append(df_selection[i].sum())

pie_region_dist = px.pie(df_selection,
    values=total_values,
    names= total_regions,
    title="<b>Sales Distribution by Region</b>",
    template="plotly_dark",
)

#PIE CHART - Sales by Genre
genre_values=[]
genre_names=sorted(df_selection["Genre"].unique())
for i in genre_names:
    df_temp=df_selection[df_selection["Genre"]==i]
    genre_values.append(df_temp["Global_Sales"].sum())
pie_genre_dist = px.pie(df_selection,
    values=genre_values,
    names=genre_names,
    title="<b>Global Sales Distribution by Genre</b>",
    template="plotly_dark",)

#DISPLAY HISTOGRAMS
left_column, right_column = st.columns(2)
left_column.plotly_chart(pie_region_dist, use_container_width=True)
right_column.plotly_chart(pie_genre_dist, use_container_width=True)



#---LINE CHART---
df_yearwise=df_selection.groupby(by=["Year"]).sum()
line_year_dist=px.line(df_yearwise, 
    x = df_yearwise.index, 
    y=total_regions,
    title="<b>Year-wise Regional Sales in Millions</b>",
    template="plotly_dark",
    )
st.plotly_chart(line_year_dist)

#---TOP 10---
st.header("Top 10 Highest Grossing Games based on Genre")
chosen_genre = st.selectbox("Select a Genre:",genre_names)
df_genre=df_selection[df_selection["Genre"]==chosen_genre]
df_genre_gamewise=df_genre.groupby(by=["Name"]).sum()
df_genre_sorted=df_genre_gamewise.sort_values('Global_Sales',ascending=False)
st.dataframe(df_genre_sorted[["Global_Sales"]].head(10))
