import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from streamlit_lottie import st_lottie
import requests
import plotly.graph_objects as go
import re
import pydeck as pdk

st.set_page_config(layout="wide")


# change background of container
page_bg_img = """
   <style>
   [id="bedford-stuyvesant"]{
   border-radius: 8px;
   background-color:#cfe7fd;
   padding:20px
   }
   """

st.markdown(page_bg_img, unsafe_allow_html=True)





# pre-load animation
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()

#load assets
lottie_coding = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_DMgKk1.json")
lottie_exception = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_bhw1ul4g.json")
lottie_na = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_qszkkg7n.json")

schoolData = pd.read_csv('2019_DOE_High_School_Directory.csv')
data = schoolData[["school_name", "finalgrades", "academicopportunities1", "academicopportunities2", "academicopportunities3", "neighborhood", "zip", "school_sports", "total_students","college_career_rate", "attendance_rate", "graduation_rate", "extracurricular_activities"]]

st.sidebar.header("Please Filter Here:")

#st.write(data)
offergrades = st.sidebar.selectbox("Select grades:",
                              options= data["finalgrades"].unique())
neighborhood = st.sidebar.selectbox("Select neighborhood:",
                              options= data["neighborhood"].unique())

data.sort_values("neighborhood")




df_selection = data.query("finalgrades == @offergrades & neighborhood== @neighborhood")
#mask = data["school_name"].isin(neighborhood)
#data = data[mask]

#st.dataframe(df_selection)

try:
    st.title(df_selection["neighborhood"].values[0])
    #cols = st.columns(len(name_col))
    #Failed: what I want: 3 columns
    #for every school in school list, generate a column, put school name as the title


    #with st.container():
        #cols = st.columns(len(name_col))
        #for schoolname in name_col["school_name"]:
            #with cols:
                #st.header(schoolname)

    #overall page container

    #layout school name
    labels = df_selection["school_name"].tolist()
    opportunities = df_selection["academicopportunities1"]
    try:
        cols = st.columns(len(labels))
    except:
        st.write(" ")
    with st.container():

        for i in labels:

            with st.container():
                cols[labels.index(i)].subheader(f"""{i}""")
                dex = int(labels.index(i))


                class Error(Exception):
                    """Base class for exceptions"""
                    pass
                class Nan(Error):
                    """Raised when it's float that means it's na :)"""
                    pass

                with cols[labels.index(i)]:
                    #school size circle

                    student_number_string  = re.sub(',','', str(df_selection["total_students"].values[dex]))
                    height = int(student_number_string)/10
                    width = int(student_number_string)/10
                    fancy_color = "#FFCADF"
                    dots = """

                                            <div style="height:{}px; width:{}px; background-color:{};border-radius: 50%; display: inline-block">
                                            </div>

                                        """
                    st.markdown(dots.format(height, width, fancy_color), unsafe_allow_html=True)
                    st.subheader("   ")
                    st.write("Academic Opportunities: ")

                    #st.write(type(df_selection["academicopportunities2"].values[dex]))
                    try:


                        #st.write(o2)
                        if type(df_selection["academicopportunities1"].values[dex]) ==float or type(df_selection["academicopportunities2"].values[dex]) ==float or type(df_selection["academicopportunities3"].values[dex]) == float:
                            raise Nan
                        else:
                            st.markdown("   1, {0}".format(df_selection["academicopportunities1"].values[dex]))
                            st.markdown("   2, {0}".format(df_selection["academicopportunities2"].values[dex]))
                            st.markdown("   3, {0}".format(df_selection["academicopportunities3"].values[dex]))
                    except Nan:
                        #st.write("  ")
                        st_lottie(lottie_na, height=300)
        #st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """,
                                   # unsafe_allow_html=True)
                    #if "9" in df_selection["finalgrades"].values[dex]:
                        #st.write("yes")

                    #else:
                        #st.write("no")


    with st.container():
        #st.write("---")
        with st.expander("Athletic Opportunities"):
            labels = df_selection["school_name"].tolist()
            try:
                cols = st.columns(len(labels))
            except:
                st.write(" ")
            for i in labels:
                dex = int(labels.index(i))
                with st.container():

                    with cols[dex]:
                        # st.write(type(df_selection["academicopportunities2"].values[dex]))
                        try:

                            # st.write(o2)
                            if type(df_selection["school_sports"].values[dex]) == float:
                                raise Nan
                            else:
                                st.markdown("   Sports {0}".format(df_selection["school_sports"].values[dex]))
                        except Nan:
                            # st.write("  ")
                            st_lottie(lottie_na, height=100, key="second")

    with st.container():
        #st.write("---")
        with st.expander("Extracurricular Offering"):
            labels = df_selection["school_name"].tolist()
            try:
                cols = st.columns(len(labels))
            except:
                st.write(" ")
            for i in labels:
                dex = int(labels.index(i))
                with st.container():

                    with cols[dex]:
                        # st.write(type(df_selection["academicopportunities2"].values[dex]))
                        try:

                            # st.write(o2)
                            if type(df_selection["extracurricular_activities"].values[dex]) == float:
                                raise Nan
                            else:
                                st.markdown("   Activities: {0}".format(df_selection["extracurricular_activities"].values[dex]))
                        except Nan:
                            st.write("No data  ")



    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_selection["school_name"],
        y=df_selection["attendance_rate"],
        name='Attendance Rate',
        #marker_color='indianred'
        marker_color = '#FFAFA3'

    ))
    fig.add_trace(go.Bar(
        x=df_selection["school_name"],
        y=df_selection["graduation_rate"],
        name='graduation_rate',
        #marker_color='#8284f7'
        marker_color = '#FFC470'
    ))
    fig.add_trace(go.Bar(
        x=df_selection["school_name"],
        y=df_selection["college_career_rate"],
        name='college_career_rate',
        #marker_color='lightsalmon'
        marker_color = '#D9B8FF'

    ))


    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(barmode='group', xaxis_tickangle=-45)
    st.plotly_chart(fig)











    with st.container():
        #st.write("---")
        left_column, right_column = st.columns(2)


    with right_column:
        st_lottie(lottie_coding, height=300, key="coding2")




#if there is no school
except IndexError as error:
 # Output expected IndexErrors.
    st.title("Oops! There isn't {0} schools in {1} neighborhood~".format(offergrades, neighborhood))
    st_lottie(lottie_exception, height=300, key="exception1")




