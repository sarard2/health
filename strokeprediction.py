#Importing Needed Libraries
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import pickle
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu
import seaborn as sns
import plotly
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

#Setting page width to wide
st.set_page_config(layout="wide")

st.markdown("""
<style>
    #MainMenu, header, footer {visibility: hidden;}

    /* This code gets the first element on the sidebar,
    and overrides its default styling */
    section[data-testid="stSidebar"] div:first-child {
        top: 0;
        height: 100vh;
    }
</style>
""",unsafe_allow_html=True)

st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)
st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #808080;">
  <a class="navbar-brand" href="https://www.aub.edu.lb/osb/MSBA/Pages/default.aspx" target="_blank">Healthcare Analytics</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav">
      <li class="nav-item">
        <a class="nav-link" href="https://invis.io/VZ12GD1UDFTG" target="_blank">My Portfolio</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="https://www.linkedin.com/in/sara-ramadan/" target="_blank">Contact Me</a>
      </li>
    </ul>
  </div>
</nav>
""", unsafe_allow_html=True)

# generate country code  based on country name
import pycountry
def alpha3code(column):
    CODE=[]
    for country in column:
        try:
            code=pycountry.countries.get(name=country).alpha_3
           # .alpha_3 means 3-letter country code
           # .alpha_2 means 2-letter country code
            CODE.append(code)
        except:
            CODE.append('None')
    return CODE

#Reading data
data=pd.read_csv("healthdata.csv")
bmi_mean = data['bmi'].mean().round(1)
data = data.fillna(value=bmi_mean)



#Setting Default Theme for plotly graphs
#pio.templates.default = "simple_white"

#Sidebar Menu
selected = option_menu(None, ["Home", "Data", "Visuals","Exploration",'Prediction'],
    icons=['house', 'cloud-upload', "list-task", 'gear'],
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "darkturquoise", "font-size": "20px"},
        "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#808080"},
    }
)

yearly=pd.read_csv("yearlystrokes.csv")
# create a column for code
yearly['Country_Code']=alpha3code(yearly.location)

#Home Page
if selected =="Home":
    st.write("hi")

#Overview page
if selected=="Data":

    gd=GridOptionsBuilder.from_dataframe(data)
    gd.configure_pagination(enabled=True)
    gd.configure_default_column(editable=True,groupable=True)
    col1,col2=st.columns(2)
    with col1:
        st.header("Global Burder of Disease on Stroke")
        AgGrid(yearly)
    with col2:
        st.header("Sample Dataset on Stroke from Kaggle")
        AgGrid(data)

        #Visuals Page
if selected=="Visuals":
    col1,col2=st.columns(2)
    with col1:
         strokeages=pd.read_csv("allages.csv")
         country_options=strokeages["Location"].unique().tolist()
         metric_options=strokeages["Metric"].unique().tolist()
         my_expander1 = st.expander(label='Press to Edit the Metric!')
         with my_expander1:
                country_select=st.selectbox('In which country do you want to trace the number of deaths by stroke?',country_options)
                metric_select=st.selectbox("Which metric are you more intesrested in?")
                #number_stroke=strokeages[strokeages["Metric"]=="Number"]
         filter_dff=strokeages[strokeages["Location"]==country_select]&strokeages[strokeages["Metric"]==metric_select]

         figure8=px.area(filter_dff, x='Year', y="val",color="Sex",title="Deaths by Stroke Through Time According to Gender",
         width=400, height=400,
         color_discrete_map={1: "cadetblue", 0: "darkturquoise"},
         template="simple_white")
         figure8.update_layout(xaxis_title=None,yaxis_title=None)
         figure8.update_xaxes(showgrid=False,zeroline=False)
         figure8.update_yaxes(showgrid=False,showticklabels = True)
         figure8.update_layout( # customize font and legend orientation & position
         legend=dict(
         title="Stroke", orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center"))
         st.plotly_chart(figure8,use_container_width=True)


    with col2:
        thisyear=yearly[yearly["year"]==2019]
        #Map showing death across the globe in 2019
        fig = go.Figure(data=go.Choropleth(
        locations = thisyear['Country_Code'],
        z = thisyear['val'],
        text = thisyear['location'],
        colorscale = 'Gray',
        autocolorscale=False,
        reversescale=True,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title = 'Deaths',))
        fig.update_layout(height=600,width=400)
        fig.update_geos(projection_type="natural earth")
        st.plotly_chart(fig,use_container_width=True)



#Exploration Page
if selected=="Exploration":
    my_expander = st.expander(label='Filter the Graphs')
    with my_expander:
       
        col3,col4=st.columns(2)
        with col3:
            gender_options=data["gender"].unique().tolist()
            gender_select=st.multiselect('Which gender in the sample are you interested in studying?',gender_options,"Male")
        with col4:
            age_options=data["age"].unique().tolist()
            age_select=st.multiselect('Which age in the sample are you interested in studying?',age_options,64)
            filter_df=data[data["gender"].isin(gender_select)&data["age"].isin(age_select)]
    col1,col2=st.columns(2)
    with col1:
        figure1=px.histogram(filter_df, y='residence_type',color="stroke", barmode='group',title="Stroke according to Residence Type",
        width=400, height=400,
        color_discrete_map={1: "cadetblue", 0: "darkturquoise"},
        template="simple_white")
        figure1.update_layout(xaxis_title=None,yaxis_title=None)
        figure1.update_xaxes(showgrid=False,zeroline=False)
        figure1.update_yaxes(showgrid=False,showticklabels = True)
        figure1.update_layout( # customize font and legend orientation & position
        legend=dict(
        title="Stroke", orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center"))
        st.plotly_chart(figure1,use_container_width=True)
    with col1:
        figure2=px.histogram(filter_df, y='work_type', color="stroke", barmode='group',title="Stroke according to Work Type",
        width=400, height=400,
        color_discrete_map={1: "cadetblue", 0: "darkturquoise"},
        template="simple_white")
        figure2.update_layout(xaxis_title=None,yaxis_title=None)
        figure2.update_xaxes(showgrid=False,zeroline=False)
        figure2.update_yaxes(showgrid=False,showticklabels = True)
        figure2.update_layout( # customize font and legend orientation & position
        legend=dict(
        title="Stroke", orientation="h", y=1, yanchor="bottom", x=0.5, xanchor="center"))
        st.plotly_chart(figure2,use_container_width=True)

        figure10=px.box(data, x="stroke", y="bmi",title="Stroke according to BMI",
        width=400, height=400,
        color_discrete_map={1: "cadetblue", 0: "darkturquoise"},
        template="simple_white")
        figure10.update_layout(xaxis_title=None,yaxis_title=None)
        figure10.update_xaxes(showgrid=False,zeroline=False)
        figure10.update_yaxes(showgrid=False,showticklabels = True)
        st.plotly_chart(figure10,use_container_width=True)
    with col2:
        figure3=px.histogram(filter_df, y='ever_married', color="stroke", barmode='group',title="Stroke according to Marriage Status",
        width=400, height=400,
        color_discrete_map={1: "cadetblue", 0: "darkturquoise"},
        template="simple_white")
        figure3.update_layout(xaxis_title=None,yaxis_title=None)
        figure3.update_xaxes(showgrid=False,zeroline=False)
        figure3.update_yaxes(showgrid=False,showticklabels = True)
        st.plotly_chart(figure3,use_container_width=True)
    with col2:
        figure4=px.histogram(filter_df, y='smoking_status', color="stroke", barmode='group',title="Stroke according to Smoking Status",
        width=400, height=400,
        color_discrete_map={1: "cadetblue", 0: "darkturquoise"},
        template="simple_white")
        figure4.update_layout(xaxis_title=None,yaxis_title=None)
        figure4.update_xaxes(showgrid=False,zeroline=False)
        figure4.update_yaxes(showgrid=False,showticklabels = True)
        st.plotly_chart(figure4,use_container_width=True)
        colors = ['rgb(0, 0, 100)', 'rgb(0, 200, 200)']

        figure9=px.box(data, x="stroke", y="avg_glucose_level",title="Stroke according to Glucose Level",
        width=400, height=400,
        color_discrete_map={1: "cadetblue", 0: "darkturquoise"},
        template="simple_white")
        figure9.update_layout(xaxis_title=None,yaxis_title=None)
        figure9.update_xaxes(showgrid=False,zeroline=False)
        figure9.update_yaxes(showgrid=False,showticklabels = True)
        st.plotly_chart(figure9,use_container_width=True)

    #figure6=px.histogram(filter_df, x='heart_disease', color="stroke", barmode='group')
    #st.plotly_chart(figure6,use_container_width=True)

    #figure7=px.histogram(filter_df, x='hypertension', color="stroke", barmode='group')
    #st.plotly_chart(figure7,use_container_width=True)

#Prediction Page
if selected =="Prediction":
#Logistic Regression Model to predict approximate price of tickets based on variables that the user inputs
 col1,col2,col3=st.columns(3)
 with col1:
     #Gender
    gender = st.selectbox("What is your gender?", ['Female','Male','Other'])

    if gender == "Female":
              gender_inp = 0
    elif gender == "Male":
              gender_inp = 1
    elif gender == "Other":
              gender_inp = 2

       #Ever Married

    married = st.selectbox("Were you ever Married?" , ['Yes','No'])

    if married == "No":
              married_inp = 0
    elif married == "Yes":
              married_inp = 1
        #Work Type

    work = st.selectbox("What do you work?" , ['Government Job','Never Worked','Private Job', "Self Employed", "Children"])

    if work == "Government Job":
               work_inp = 0
    elif work == "Never Worked":
               work_inp = 1
    elif work == "Private Job":
               work_inp = 2
    elif work == "Self Employed":
               work_inp = 3
    elif work == "Children":
               work_inp = 4

        #Residence Type

    residence = st.selectbox("Where do you live?" , ['Rural','Urban'])

    if residence == "Rural":
               resi_inp = 0
    elif residence == "Urban":
               resi_inp = 1
    #Smoking Status

    smoke = st.selectbox("Do you smoke?" , ['Unknown','Formerly Smoke','Never Smoked','Smokes'])

    if smoke == "Unknown":
           smoke_inp = 0
    elif smoke == "Formerly Smoke":
           smoke_inp = 1
    elif smoke == "Never Smoked":
           smoke_inp = 2
    elif smoke == "Smokes":
           smoke_inp = 3

 with col3:
     #age
     age=st.number_input("How old are you?")
     hypertension=st.selectbox("Do you have hypertension?",["Yes","No"])
     if hypertension=="Yes":
         hype_inp=1
     elif hypertension=="No":
         hype_inp=0
     heart=st.selectbox("Do you have any heart problems?",["Yes","No"])
     if heart=="Yes":
         heart_inp=1
     elif heart=="No":
         heart_inp=0
     min_glucose = min(data["avg_glucose_level"])
     max_glucose = max(data["avg_glucose_level"])
     glucose=st.number_input("What is your average glucose level?",min_value = min_glucose,max_value = max_glucose)
     min_bmi = min(data["bmi"])
     max_bmi = max(data["bmi"])
     bmi=st.number_input("What is your most recent BMI?",min_value = min_bmi,max_value = max_bmi)
 with col2:
#Model of Logistic Regression From Pickle File
     lrmodel=pickle.load(open("logisticmodel.pkl",'rb'))
#Prediction given the following variables
     par = [gender_inp , married_inp , work_inp ,resi_inp, smoke_inp,age,hype_inp,heart_inp,glucose,bmi]

     if st.checkbox("Check Your Health Status"):
           pred = lrmodel.predict([par])
           if pred== 0:
               st.write('You will not have a stroke')
           else:
            st.write("You Might Have a stroke")

# Get input values - numeric variables
 #optional = st.slider('Please enter the living apartments:',min_value = 0,max_value = 5)
