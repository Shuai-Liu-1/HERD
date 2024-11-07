import pandas as pd
import plotly.express as px
#import plotly
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
#import mercury as mr
import warnings
from pandas.errors import SettingWithCopyWarning
warnings.simplefilter(action='ignore', category=(SettingWithCopyWarning))
import streamlit as st


st.header("R&D Field ")
st.write("""There are three primary R&D fields: **Science, Engineering, and Non-Science & Engineering**. Within each R&D field, there are also subfields. 
         For example, under the Science R&D field, there are subfields such as Life Science and Physical Science etc. """)
st.write("""R&D expenditures in all **Science** fields was reaching 76.2 billion (78%) in FY 2022. 
         while **Engineering** R&D expenditures was reaching 15.6 billion(16%) total and **Non-Science & Engineering R&D** was reaching 5.9 billion total(6%).
         R&D expenditures in two life sciences subfields, health sciences (31.9 billion total) and biological and biomedical sciences (18.2 billion total), in FY 2022.(pie chart below)""")
@st.cache_data
def load_data():
    df=pd.read_csv("Sunburs.csv")
    return df
Sunburs=load_data()
#st.write(Sunburs)

#st.write(pie_data.dtypes)
#st.write(pie_data[pie_data["Year"]==2010])
st.subheader("Expenditures by R&D Field by the Years")


years= ["2022","2021","2020","2019","2018","2017","2016","2015","2014","2013","2012","2011","2010"]
selected_year=st.selectbox(
"Please choose a **year** from the options below to view the pie chart depicting expenditures in the R&D field for the selected year. You can also **click or hover over** the pie chart for additional details ",
(years),placeholder="") 

rows=1
cols=1
specs = [[{'type':'domain'}] * cols] * rows
fig = make_subplots(rows=rows,cols=cols,specs=specs)#,subplot_titles=selected_year)
figaux = px.sunburst(Sunburs, path=['Field1', "Field2","Field3"], values=selected_year)
fig.add_trace(figaux.data[0], row=1, col=1)
fig.update_traces(textinfo="label+percent parent",hovertemplate = "%{label}: %{percentParent:.1%} <br>$:%{value:,}")
st.plotly_chart(fig,use_container_width=True)
############################################
st.subheader("Expenditures by R&D Field from 2010 to 2022")
field=pd.melt(Sunburs,id_vars=['Field','Field1',"Field2","Field3"],value_vars=years).rename(columns={"variable":"Year","value":"Expenditures"})
#st.write(field)
#fig.update_layout(width=450,height=450)  

selected_source = st.multiselect(
    "Please select one or more R&D fields to examine the trends from 2010 to 2022",
    field["Field1"].unique(),default=["Science"])
selected_source_data=field[field["Field1"].isin(selected_source)].drop(columns=['Field3'])
#st.write(selected_source_data,"df1")
def group(name):
    data=selected_source_data[[name,"Year","Expenditures"]].groupby(by=[name,'Year'])['Expenditures'].sum().reset_index()
    fig = px.line(data.sort_values(by=["Year","Expenditures"],ascending=False), x="Year", y="Expenditures", color=name, markers=True,
              labels={
                     "Expenditures": "Dollars ",
},
              title="Higher education R&D expenditures, by R&D field from 2010 to 2022",)
    return data,fig

#data=selected_source_data[["Field1",'Year','Expenditures']].groupby(by=["Field1",'Year'])['Expenditures'].sum().reset_index()
#st.write(data)




st.plotly_chart(group("Field1")[1],use_container_width=True)
#st.write(group("Field1")[0])
#st.write(field)
#st.plotly_chart(group("Field")[1],use_container_width=True)
on = st.toggle('Show data')
if on:
    st.write(group("Field1")[0][['Field1','Year','Expenditures']])

for i in range(len(selected_source)):
    data=selected_source_data[selected_source_data['Field1']==selected_source[i]].groupby(by=["Field","Year"]).sum().reset_index()
    data=data.sort_values(by=["Year","Expenditures"],ascending=False)
    #data=data.replace(0, np.nan, inplace=True)
    fig = px.line(data, x="Year", y="Expenditures", color="Field", markers=True,
             title="Research Filed for " +selected_source [i],)
             #labels={'pop':'population of Canada'})
    fig.update_layout(yaxis_title="Dollars",legend={'traceorder':'normal'})
    
    #st.write(data,"df2")
    st.plotly_chart(fig,use_container_width=True)

    on = st.toggle("Show " + selected_source[i]+' data ')
    if on:
         st.write(data.sort_values(by=["Expenditures"],ascending=True))
st.write("""**Notes**: Prior to FY 2016, expenditures for Natural Resources and Conservation, Materials Science, Anthropology, and Industrial and Manufacturing Engineering were not collected separately""")







