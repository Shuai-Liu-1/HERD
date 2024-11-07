import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import altair as alt
import re

#st.sidebar.divider()
st.header("Expenditure, Research Filed and Funding Sources ")
#st.subheader("Research expenditures for the Institution in "+year)
st.subheader("Expenditures for Institution from 2016 to 2022")

#t.divider() 

col1,col2,col3=st.columns(3,gap="small")
with col1:
     st.info("Select by Conditions Below")
state= {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "Virgin Islands": "VI",}
    #"United States Minor Outlying Islands": "UM",}
def load_data():
    RF= pd.read_csv("RF.csv")
    RF['year']=RF['year'].astype(str)#,encoding='windows-1252').drop(columns='Unnamed: 0')
    #RF_SN=RF[RF['year']==year]
    SF_SN= pd.read_csv("SF2022.csv").drop(columns='Unnamed: 0')
    return SF_SN,RF
#RF_SN=load_data()[0]
SF_SN=load_data()[0]
RF=load_data()[1]
#st.write(RF_SN)

s=RF[RF['Institution'] != 'All institutions'][["Institution","All R&D expenditures","State","system","HBC","HHE"]].drop_duplicates()
S=s.groupby(["Institution","State","system","HBC","HHE"])['All R&D expenditures'].sum().reset_index()
s1=RF[RF['Institution'] != 'All institutions'][["Institution","All R&D expenditures","State","system","HBC","HHE","year"]].drop_duplicates()
S1=s1.groupby(["Institution","State","system","HBC","HHE","year"])['All R&D expenditures'].sum().reset_index()

SF_SN['State']=SF_SN['State'].map(state)
S1['State']=S1['State'].map(state)
#st.write(S1)
custom_style = """
    <style>
        .stSelectboxLabel {
            margin-bottom: 15px;  /* Adjust the margin as needed */
        }
    </style>
"""
col1,col2,col3,col4=st.columns([2,2,1,1],gap="small")
with col2:
    #st.write("#")
    
    public = st.selectbox("Select Institution by **system**(All, Public or Private)",('Public|Private','Public', "Private"))
with col3:
    #st.write("#")
    #st.write("#")
    #st.markdown(custom_style, unsafe_allow_html=True)
    
    HHE = st.selectbox("High Hispanic Enrollment (HHE)",("No|Yes","No",'Yes'))
    
with col4:
    #st.write("#")
    #st.markdown(custom_style, unsafe_allow_html=True)
    HBC= st.selectbox("Historically Black Colleges and Universities (HBCUs)",("No|Yes","No",'Yes'))
with col1:
    #st.write("#")
    text_search = st.text_input("Search for institutions by **abbreviation of state** (e.g., AR). if you want to search more than one states please use | to seperate (e.g., AR|OK).", value="AR")       
SchoolName = st.text_input(
    "Search for institutions by **keyword**, eg: Arkansas, Fayetteville. if you want to search more than one institutions please use | to seperate keywords,**You can also leave it empty**." ,
      value="Arkansas for Medical Sciences|Arkansas, Fayetteville")  

m1=S['system'].str.contains(public).reset_index()
mHHE=S['HHE'].str.contains(HHE).reset_index()
mHBC=S['HBC'].str.contains(HBC).reset_index()
#M1=S[m1][mHBC][mHHE]
combined_condition=m1&mHHE&mHBC
M1=S[combined_condition]
#st.write(M1)


m2 = M1["State"].str.contains(text_search,na=False, case=False)
df=M1[m2]#.groupby("Institution")['All R&D expenditures'].sum().reset_index()
#st.write(df)

n1=S1['system'].str.contains(public,na=False, case=False) 
nHHE=S1['HHE'].str.contains(HHE,na=False, case=False)
nHBC=S1['HBC'].str.contains(HBC,na=False, case=False)
school=S1["Institution"].str.contains(SchoolName,na=False, case=False)
State=S1["State"].str.contains(text_search,na=False, case=False)
combined_condition=n1 & nHHE & nHBC & school & State
N1=S1[combined_condition]
#st.write(M1)

#n2 = N1["State"].str.contains(text_search,na=False, case=False)
dfN1=N1[school]
#st.write(dfN1)

if not dfN1.empty:
#st.write(df)
     on = st.toggle('Show data')
     if on:
         st.dataframe(dfN1.style.highlight_max(color='orange',subset=pd.IndexSlice[:, ['All R&D expenditures']]),use_container_width=True)

     c = alt.Chart(df).mark_bar().encode (
              x='Institution', 
              y='All R&D expenditures',
              color=alt.condition(
                   alt.datum['All R&D expenditures']==df['All R&D expenditures'].max(),
                   alt.value('orange'),     
                   alt.value('steelblue')))
     #st.altair_chart(c, use_container_width=True)
else:
     st.markdown(" **:red[No data matching your selection]**")


def group():
    #data=dfN1[["Institution","year","All R&D expenditures"]].groupby(by='year')['All R&D expenditures'].reset_index()
    fig = px.line(dfN1.sort_values(by=["year","All R&D expenditures","Institution"],ascending=False), x="year", y="All R&D expenditures", color="Institution", markers=True,
              labels={
                     "All R&D expenditures": "Dollars",
},
              title="Research expenditures from 2016 to 2022 for searched institutions",)
    return fig

st.plotly_chart(group(),use_container_width=True)
st.divider() 
###############################################################



#st.divider() 
st.subheader("Research Filed")

source=["AllOther","Business", "FedGovFunds", "InstitutionalFunds", "StateLocalGov", "Nonprofit"]


#RF_SN=RF[RF['year']==year]
RF['State']=RF['State'].map(state)
S['State']=S['State'].map(state)
m4= RF["State"].str.contains(text_search,na=False, case=False)
m4_1=RF["Institution"].str.contains(SchoolName,na=False, case=False)
M44=RF[m4][m4_1]
#M43=M44.groupby(["year","Institution"])[["All R&D expenditures"]].sum().reset_index()
#M43=M43.sort_values(by=["year","All R&D expenditures"],ascending=False)
#st.write(M43)



M45=M44.groupby(["year","Institution"])[["Computer and information sciences","Geosciences, atmospheric sciences, and ocean sciences","Life sciences","Mathematics and statistics","Physical sciences","Psychology","Social sciences","Sciences nec","Engineering","All non-S&E fields"]].sum().reset_index()
col1,col2=st.columns(2,gap="small")
with col1:
     #st.write("#")
     st.info("Total Expenditures By Research Filed for Searched Institutions")

with col2:
     selected_source= st.selectbox(
"Please select one R&D fields to examine the trends from 2016 to 2022",
M45.columns.drop(["year","Institution"]),index=2)
col=["year","Institution",selected_source]
colu=[item for sublist in col for item in (sublist if isinstance(sublist,list) else[sublist])]

data=M45[colu]
data=data.sort_values(by=["year",selected_source],ascending=False)
on = st.toggle("Show " + selected_source+' data ')
if on:
        st.write(data.sort_values(by=selected_source))
#
#st.write(M44)
#st.subheader("Overview Funding Source on 2022 (Dollars in thousands)")

#
fig = px.line(data.sort_values(by=['year',selected_source,"Institution"],ascending=False), x="year", y=selected_source, color="Institution", markers=True,
        title=selected_source+ "Research Filedf or Searched Institutions")
        #labels={'pop':'population of Canada'})
fig.update_layout(yaxis_title="Dollars",legend={'traceorder':'normal'})
st.plotly_chart(fig,use_container_width=True)



####
col1,col2=st.columns(2,gap="small")
with col1:
     #st.write("#")
     st.info("Total Expenditures By Year ")
years=["2022","2021","2020","2019","2018","2017","2016"]
with col2:
     year = st.selectbox("Select a year",(years))
M4=M44[M44['year']==year]

df3=M4.drop(columns=['HBC','HHE',"year"]).melt(id_vars=["Institution", "All R&D expenditures",'FundsSource',"Rank","State","system"], 
        var_name="ResearchFiled", 
        value_name="Value")
df4=df3.groupby(["Institution","ResearchFiled"]).sum("Value").reset_index()
#st.write(df3)
#st.write(df4)
on1 = st.toggle('Show data',key="show2")
if on1:
    st.dataframe(df4,use_container_width=True)
    #st.write("Rank All R&D expenditures based on FundsSource")
fig = px.bar(df4.sort_values(by=["ResearchFiled",'Institution'],ascending=False), x="Institution", y="Value", color="ResearchFiled",   
            title="Research Filed for the Institution in "+year ,color_discrete_sequence=px.colors.qualitative.Set2)
            #labels={'pop':'population of Canada'})
fig.update_layout(yaxis_title="Dollars ")
###
st.plotly_chart(fig,use_container_width=True)
col1,col2=st.columns(2,gap="small")
with col1:
     #st.write("#")
     st.info("Total Expenditures By Founding Sources in "+year)
with col2:
    text_search_3 = st.selectbox("Based on expenditures, there are six sources: AllOther, Business, FedGovFunds, InstitutionalFunds, StateLocalGov, and Nonprofit. Please choose one sources"
,source,index=2)
df2=M4[M4['FundsSource']==text_search_3]
df2=df2.drop(columns=['HBC','HHE',"year"]).melt(id_vars=["Institution", "All R&D expenditures",'FundsSource',"Rank","State","system"], 
        var_name="ResearchFiled", 
        value_name="Value")
@st.cache_data
def load_data():
    return df2
on2 = st.toggle('Show data in Year ' +year,key="show3")
if on2:
    st.dataframe(df2,use_container_width=True)
fig = px.bar(df2[df2['FundsSource']==text_search_3].sort_values(by=["ResearchFiled",'Institution'],ascending=False), x="Institution", y="Value", color="ResearchFiled",   
            title="Research Filed for the Institution in "+year+" Source from " +text_search_3,color_discrete_sequence=px.colors.qualitative.Set2)
            #labels={'pop':'population of Canada'})
fig.update_layout(yaxis_title="Dollars ")

st.plotly_chart(fig,use_container_width=True)


st.divider() 
########################################################################
st.subheader("Funding Sources for the Institution" )
#st.divider() 


col1,col2=st.columns(2,gap="small")
with col1:
     #st.write("#")
     st.info("Expenditures By Founding Sources")

M46_1=RF["State"].str.contains(text_search,na=False, case=False)
M46_2=RF["Institution"].str.contains(SchoolName,na=False, case=False)
M46=RF[M46_1][M46_2]


with col2:
     selected_source= st.selectbox(
"Please select one funding source to examine the trends from 2016 to 2022",
M46['FundsSource'].unique(),index=2)
M47=M46[M46['FundsSource']==selected_source]
#st.write(M47)
if not M47.empty:
#st.write(df)
    on1 = st.toggle('Show data ')
    if on1:
        st.dataframe(M47,use_container_width=True)

fig47 = px.line(M47.sort_values(by=['year',"All R&D expenditures","Institution"],ascending=False), x="year", y="All R&D expenditures", color="Institution", markers=True,
                labels={
                     "All R&D expenditures": "Dollars",
},
        title="Funding Sources from " +selected_source)
        #labels={'pop':'population of Canada'})
fig.update_layout(yaxis_title="Dollars",legend={'traceorder':'normal'})
st.plotly_chart(fig47,use_container_width=True)

col1,col2=st.columns(2,gap="small")
with col1:
     #st.write("#")
     st.info("Founding Sources by Year")
with col2:
     year2 = st.selectbox("Please select a year",(years))

M48=M46[M46['year']==year2]


if not M48.empty:
#st.write(df)
    on48 = st.toggle(' Show data ')
    if on48:
        st.dataframe(M48,use_container_width=True)
        
fig = px.bar(M48.sort_values(by=["All R&D expenditures","Institution"],ascending=False), x="Institution", y="All R&D expenditures", color="FundsSource", 
             color_discrete_sequence=px.colors.qualitative.Set2,
             title="Funding Sources for the Institution in " +year2)
             #labels={'pop':'population of Canada'})
fig.update_layout(yaxis_title="Dollars ")
st.plotly_chart(fig)
st.divider()








