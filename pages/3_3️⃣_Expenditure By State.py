import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from PIL import Image
import altair as alt
from plotly.subplots import make_subplots

#from plotly.subplots import make_subplots
st.header("Expenditure Trend by State")

@st.cache_data
def load_data():
    data=pd.read_csv("C:/Users/shuail/VScode/HERD-app/ByState.csv")
    return data
df=load_data()

#st.write(df)


#st.title("Higher education R&D expenditures, by state: FYs 2010–22(Dollars in thousands)")

#st.write("This chart shows the number of air passenger traveled in each month from 1949 to 1960")


df.astype({'year': 'object'})

fig = px.choropleth(df,locations='state', animation_frame='year',locationmode="USA-states",scope='usa',
                    color="expenditure",
                    color_continuous_scale=px.colors.sequential.Rainbow,#px.colors.cyclical.IceFire,#px.colors.sequential.Rainbow,#"reds"
                    hover_name="state",range_color=[0,13000000000])
fig.update_layout(title="Higher education R&D expenditures, by state: FYs 2010–22")
fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000
#fig.show()
st.plotly_chart(fig)



on = st.toggle('Compare with EPSCoR map')
ESPCoR = Image.open(r"C:/Users/shuail/VScode/HERD-app/EPSCoR.JPG")
if on:
     st.image(ESPCoR)    #st.write("Rank by All R&D expenditures ")
     st.markdown("""
                 ESPCoR map comes from 
                 [NSF](https://new.nsf.gov/funding/initiatives/epscor/epscor-criteria-eligibility)
                 """)
st.divider()
####################################################
col1,col2,=st.columns([1,2],gap="small")
with col1:
    #st.write("#")
    st.info("State expenditure line chart by year")  
with col2:
    text_search = st.text_input("Please enter abbreviation of a state (e.g., AR).  if you want to search more than one states please use | to seperate (e.g., AR|OK)", 

#st.info("Search state abbreviations to view annual Higher Education R&D expenditures ")
#text_search = st.text_input("Please enter abbreviation of a state (e.g., AR).  if you want to search more than one states please use | to seperate (e.g., AR|OK)", 
                            value="AR|TN")       

state = df["state"].str.contains(text_search,na=False, case=False)
df2=df[state]
df2=df2.sort_values(by=["year",'expenditure'],ascending=False)
df2.astype({'year': 'object'})

fig1=px.line(df2,x='year',y='expenditure',color='state',markers=True, labels={"expenditure": "Dollars "})
fig1.update_layout(title="Higher education R&D expenditures for state "+text_search+ " : FYs 2010–22")
st.plotly_chart(fig1,use_container_width=True)
on = st.toggle('Show Data')
if on:
    st.write(df2)
    #st.write("Rank by All R&D expenditures ")
