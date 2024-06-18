import streamlit as st
import pandas as pd
from numerize.numerize import numerize
import plotly.express as px
import plotly.graph_objects as go
from bokeh.palettes import Spectral6

# Page behaviour
st.set_page_config(page_title="Vulcanic Analytics", layout="wide")

# Load excel file
df = pd.read_excel('volcano-events.xlsx', sheet_name='volcano-events')

# Display DataFrame for inspection
# st.dataframe(df, use_container_width=True)

# Sidebar filters

st.sidebar.header("Please Filter Here: ")

name = st.sidebar.multiselect(
    "Select the Name of Vulcano",
    options=df["Name"].unique(),
)
type = st.sidebar.multiselect(
    "Select the Type",
    options=df["Type"].unique(),
)
country = st.sidebar.multiselect(
    "Select the Country",
    options=df["Country"].unique(),
)

# Apply filters to DataFrame with default values
filtered_df = df

if name:
    filtered_df = filtered_df[filtered_df["Name"].isin(name)]
if type:
    filtered_df = filtered_df[filtered_df["Type"].isin(type)]
if country:
    filtered_df = filtered_df[filtered_df["Country"].isin(country)]

# Fill NaN values with 0
filtered_df = filtered_df.fillna(0)

def plot_map():
    if not filtered_df.empty:
        st.title("Map of Locations of Erupting Volcanoes")
        fig = px.scatter_mapbox(
            filtered_df,
            lat="Latitude",
            lon="Longitude",
            hover_name="Name",
            hover_data=["Country", "Type", "Deaths", "Missing", "Total Deaths"],
            color_discrete_sequence=["fuchsia"],
            zoom=3,
            height=500,
        )
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

def plot_bottom_left():
    if not filtered_df.empty:
        fig = px.histogram(filtered_df, x='Deaths', nbins=50, title="Death Statistics")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

def plot_type_pie():
    if not filtered_df.empty:
        type_counts = filtered_df['Type'].value_counts()
        fig = px.pie(values=type_counts.values, names=type_counts.index, title="Eruption Type Statistics")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

def plot_year_distribution():
    if not filtered_df.empty:
        year_distribution = filtered_df['Year'].value_counts().sort_index()
        fig = go.Figure(data=go.Scatter(x=year_distribution.index, y=year_distribution.values, mode='lines+markers'))
        fig.update_layout(title='Event Year Statistics', xaxis_title='Year', yaxis_title='Count')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

def plot_country_distribution():
    if not filtered_df.empty:
        country_distribution = filtered_df['Country'].value_counts().reset_index()
        country_distribution.columns = ['Country', 'Count']
        fig = px.bar(country_distribution, x='Country', y='Count', title='Eruption Statistics by Country')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

def plot_injuries_pie():
    if not filtered_df.empty:
        fig = px.pie(filtered_df, values='Injuries', names='Country', title='Injury Statistics by Country')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

def plot_deaths_by_vei_magnitude():
    if not filtered_df.empty:
        deaths_by_vei = filtered_df.groupby('VEI')['Deaths'].sum().reset_index()
        fig = px.area(deaths_by_vei, x='VEI', y='Deaths', title='Number of Deaths by VEI Magnitude')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

def HomePage():
    if not filtered_df.empty:
        with st.expander("Detailed Volcanic Eruption Data"):
            shwData = st.multiselect('Filter :', filtered_df.columns, default=["Name", "Type", "Country", "Location", "Latitude", "Longitude", "Deaths", "Missing", "Total Deaths"])
            st.dataframe(filtered_df[shwData], use_container_width=True)
        
        # Compute top analytics
        total_type = float(filtered_df['Total Houses Destroyed'].sum())
        total_injuries = float(filtered_df['Injuries'].sum())
        total_missing = float(filtered_df['Missing'].sum())
        deaths = float(filtered_df['Deaths'].sum())

        # Columns
        total1, total2, total3, total4 = st.columns(4, gap='large')
        with total1:
            st.info('Total Houses Destroyed')
            st.metric(label='Total: ', value=f"{total_type:,.0f}")

        with total2:
            st.info('Total Injuries')
            st.metric(label='Total: ', value=f"{total_injuries:,.0f}")

        with total3:
            st.info('Total Missing')
            st.metric(label='Total: ', value=f"{total_missing:,.0f}")

        with total4:
            st.info('Total Death')
            st.metric(label='Total: ', value=numerize(deaths), help=f"""Total Death: {deaths}""")

        st.markdown("""---""")

        col1, col2 = st.columns(2)
        with col1:
            plot_bottom_left()
        with col2:
            plot_year_distribution()

        col3, col4 = st.columns(2)
        with col3:
            plot_type_pie()
        with col4:
            plot_injuries_pie()

        col5, col6 = st.columns(2)
        with col5:
            plot_country_distribution()
        with col6:
            plot_deaths_by_vei_magnitude()
    else:
        st.warning("No data available for the selected filters.")

plot_map()
HomePage()