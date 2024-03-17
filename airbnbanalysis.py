import streamlit as st
from streamlit_option_menu import option_menu  # Assuming this is a custom function you've defined
import plotly.express as px
import pandas as pd
import plotly.figure_factory as ff
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title="AirBnb-Analysis", page_icon=":bar_chart:", layout="wide")

st.title(":bar_chart:   AirBnb-Analysis")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

SELECT = option_menu(
    menu_title=None,
    options=["Explore Data"],
    icons=["bar-chart"],
    default_index=0,  # Since there's only one option, the default index should be 0
    orientation="horizontal",
    styles={"container": {"padding": "0!important", "background-color": "white", "size": "cover", "width": "100"},
            "icon": {"color": "black", "font-size": "20px"},
            "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
            "nav-link-selected": {"background-color": "#6F36AD"}})




def explore_data():
    fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
    if fl is not None:
        try:
            filename = fl.name
            st.write(filename)
            df = pd.read_csv(fl, encoding="ISO-8859-1")

            st.sidebar.header("Choose your filter: ")

            # Create for neighbourhood_group
            neighbourhood_group = st.sidebar.multiselect("Pick your neighbourhood_group", df["neighbourhood_group"].unique())
            if not neighbourhood_group:
                df2 = df.copy()
            else:
                df2 = df[df["neighbourhood_group"].isin(neighbourhood_group)]

            # Create for neighbourhood
            neighbourhood = st.sidebar.multiselect("Pick the neighbourhood", df2["neighbourhood"].unique())
            if not neighbourhood:
                df3 = df2.copy()
            else:
                df3 = df2[df2["neighbourhood"].isin(neighbourhood)]

            # Filter the data based on neighbourhood_group, neighbourhood
            filtered_df = filter_data(df, df2, df3, neighbourhood_group, neighbourhood)

            visualize_data(filtered_df, df)
        except Exception as e:
            st.error(f"Error reading the file: {e}")


def filter_data(df, df2, df3, neighbourhood_group, neighbourhood):
    if not neighbourhood_group and not neighbourhood:
        filtered_df = df
    elif not neighbourhood:
        filtered_df = df[df["neighbourhood_group"].isin(neighbourhood_group)]
    elif not neighbourhood_group:
        filtered_df = df[df["neighbourhood"].isin(neighbourhood)]
    elif neighbourhood:
        filtered_df = df3[df["neighbourhood"].isin(neighbourhood)]
    elif neighbourhood_group:
        filtered_df = df3[df["neighbourhood_group"].isin(neighbourhood_group)]
    elif neighbourhood_group and neighbourhood:
        filtered_df = df3[df["neighbourhood_group"].isin(neighbourhood_group) & df3["neighbourhood"].isin(neighbourhood)]
    else:
        filtered_df = df3[df3["neighbourhood_group"].isin(neighbourhood_group) & df3["neighbourhood"].isin(neighbourhood)]

    return filtered_df

def visualize_data(filtered_df, df):
    room_type_df = filtered_df.groupby(by=["room_type"], as_index=False)["price"].sum()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("room_type_ViewData")
        fig = px.bar(room_type_df, x="room_type", y="price", text=['${:,.2f}'.format(x) for x in room_type_df["price"]],
                     template="seaborn")
        st.plotly_chart(fig, use_container_width=True, height=200)

    with col2:
        st.subheader("neighbourhood_group_ViewData")
        fig = px.pie(filtered_df, values="price", names="neighbourhood_group", hole=0.5)
        fig.update_traces(text=filtered_df["neighbourhood_group"], textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    cl1, cl2 = st.columns((2))
    with cl1:
        with st.expander("room_type wise price"):
            st.write(room_type_df.style.background_gradient(cmap="Blues"))
            csv = room_type_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Data", data=csv, file_name="room_type.csv", mime="text/csv",
                               help='Click here to download the data as a CSV file')

    with cl2:
        with st.expander("neighbourhood_group wise price"):
            neighbourhood_group = filtered_df.groupby(by="neighbourhood_group", as_index=False)["price"].sum()
            st.write(neighbourhood_group.style.background_gradient(cmap="Oranges"))
            csv = neighbourhood_group.to_csv(index=False).encode('utf-8')
            st.download_button("Download Data", data=csv, file_name="neighbourhood_group.csv", mime="text/csv",
                               help='Click here to download the data as a CSV file')

    # Create a scatter plot
    data1 = px.scatter(filtered_df, x="neighbourhood_group", y="neighbourhood", color="room_type")
    data1['layout'].update(title="Room_type in the Neighbourhood and Neighbourhood_Group wise data using Scatter Plot.",
                           titlefont=dict(size=20), xaxis=dict(title="Neighbourhood_Group", titlefont=dict(size=20)),
                           yaxis=dict(title="Neighbourhood", titlefont=dict(size=20)))
    st.plotly_chart(data1, use_container_width=True)

    with st.expander("Detailed Room Availability and Price View Data in the Neighbourhood"):
        st.write(filtered_df.iloc[:500, 1:20:2].style.background_gradient(cmap="Oranges"))

    # Download original DataSet
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button('Download Data', data=csv, file_name="Data.csv", mime="text/csv")

    st.subheader(":point_right: Neighbourhood_group wise Room_type and Minimum stay nights")
    with st.expander("Summary_Table"):
        df_sample = df[0:5][["neighbourhood_group", "neighbourhood", "reviews_per_month", "room_type", "price", "minimum_nights", "host_name"]]
        fig = ff.create_table(df_sample, colorscale="Cividis")
        st.plotly_chart(fig, use_container_width=True)

    # map function for room_type
    st.subheader("Airbnb Analysis in Map view")
    df = df.rename(columns={"Latitude": "lat", "Longitude": "lon"})

    st.map(df)

# Main function
if SELECT == "Explore Data":
    explore_data()
