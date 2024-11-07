import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import altair as alt
import re

col1,col2=st.columns([1,2],gap="small")
with col1:
    st.info("Search institution by keyword")
with col2:
    SchoolName = st.text_input(
        'Search for institutions by **keyword**, eg: Arkansas, Fayetteville.' ,
        value="U. Arkansas, Fayetteville")  


def load_data():
    RF= pd.read_csv("C:/Users/shuail/VScode/HERD-app/RF.csv")
    #RF['year']=RF['year'].astype(str)#,encoding='windows-1252').drop(columns='Unnamed: 0')
    #RF_SN=RF[RF['year']==year]
    FederalAgencyANDSchool= pd.read_csv("C:/Users/shuail/VScode/HERD-app/FederalAgencyANDSchool.csv")
    return FederalAgencyANDSchool,RF
#RF_SN=load_data()[0]
FederalAgencyANDSchool=load_data()[0]
RF=load_data()[1]



ALL=RF[RF["Institution"].str.contains(SchoolName,na=False, case=True)]
#.rename(columns={"Computer and information sciences":"CI","Geosciences, atmospheric sciences, and ocean sciences":"GAO","Mathematics and statistics":"MS"}).sort_values(by=["year","All R&D expenditures"],ascending=False)
Federal=FederalAgencyANDSchool[FederalAgencyANDSchool["Institution"].str.contains(SchoolName,na=False, case=True)].sort_values(
        by=["year","All R&D expenditures"],ascending=False)
#.rename( columns={"Computer and information sciences":"CI","Geosciences, atmospheric sciences, and ocean sciences":"GAO","Mathematics and statistics":"MS"})
#st.write(ALL)
#st.write(Federal)
field=["Computer and information sciences","Geosciences, atmospheric sciences, and ocean sciences","Life sciences","Mathematics and statistics","Physical sciences","Psychology","Social sciences","Sciences nec","Engineering","All non-S&E fields"]
combine=pd.concat([Federal,ALL.drop(['State',"system","HBC","HHE"], axis=1)])
combine=combine[combine['FundsSource']!="FedGovFunds"]
combine=pd.melt(combine,id_vars=["year","Institution","FundsSource"],value_vars=field).rename(columns={"variable":"R&D Field","value":"Expenditures"}).sort_values(by=["Expenditures"],ascending=False)
#st.write(combine)
###
on = st.toggle('Show Data')
if on:
    st.write(combine)
    
st.header("Funding Source for "+SchoolName)

col1,col2=st.columns([2,1],gap="small")
with col2:
    pie = px.pie(ALL[ALL["year"]==2022], values='All R&D expenditures', names='FundsSource', title='Founding Source on 2022',
                 color_discrete_sequence=px.colors.qualitative.Set1)
    pie.update_traces(textposition='inside', textinfo="label+percent",hovertemplate = "%{label}: %{percent:.1%} <br>$:%{value}")
    pie.update_layout(showlegend=False)
    st.plotly_chart(pie,use_container_width=True)
with col1:
    fig = px.line(ALL, x="year", y="All R&D expenditures", color="FundsSource", markers=True,
            title="Funding Source from 2016 to 2022",
            labels={'"Expenditures": "Expenditures "'},
            color_discrete_sequence=px.colors.qualitative.Set1)
    fig.update_layout(yaxis_title="Dollars ",legend={'traceorder':'normal'})
    st.plotly_chart(fig,use_container_width=True)
st.divider()
###
st.subheader("Funding Source from different Federal Government Agency for "+SchoolName)
col1,col2=st.columns([2,1],gap="small")
with col2:
    pie = px.pie(Federal[Federal["year"]==2022], values='All R&D expenditures', names='FundsSource', title='Founding Source on 2022',
                 color_discrete_sequence=px.colors.qualitative.Set1)
    pie.update_traces(textposition='inside', textinfo="label+percent",hovertemplate = "%{label}: %{percent:.1%} <br>$:%{value}")
    pie.update_layout(showlegend=False)
    st.plotly_chart(pie,use_container_width=True)
with col1:
    fig = px.line(Federal, x="year", y="All R&D expenditures", color="FundsSource", markers=True,
            title="Funding Source from 2016 to 2022",
            labels={'"Expenditures": "Expenditures "'},
            color_discrete_sequence=px.colors.qualitative.Set1)
    fig.update_layout(yaxis_title="Dollars ",legend={'traceorder':'normal'})
    st.plotly_chart(fig,use_container_width=True)
st.divider()
###

####
st.subheader("Expenditures by R&D field for "+SchoolName)
#st.write("R&D Field abbreviation: CI: Computer and information sciences, GAO: Geosciences, atmospheric sciences, and ocean sciences, MS: Mathematics and statistics")

RD=ALL.groupby(["year","Institution"])[field].sum().reset_index()
RD=pd.melt(RD,id_vars=["year","Institution"],value_vars=field).rename(columns={"variable":"R&D Field","value":"Expenditures"}).sort_values(by=["year","Expenditures"],ascending=False)
col1,col2=st.columns([3,1],gap="small")

with col1:
    fig = px.bar(RD[RD["year"]==2022].sort_values(by=["Expenditures"],ascending=False), x="R&D Field", y="Expenditures", color="R&D Field",
            color_discrete_sequence=px.colors.qualitative.Set2,
        labels={
                "Expenditures": "Dollars ","SubSubField":""
},
        title="All Expenditures by R&D field on 2022")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig,use_container_width=True)
    
with col2:
    pie = px.pie(RD[RD["year"]==2022], values='Expenditures', names="R&D Field", 
                    color_discrete_sequence=px.colors.qualitative.Set2)
    pie.update_traces(textposition='inside', textinfo="label+percent",hovertemplate = "%{label}: %{percent:.1%} <br>$:%{value}")
    pie.update_layout(showlegend=False)
    st.plotly_chart(pie,use_container_width=True)

fig = px.line(RD, x="year", y="Expenditures", color="R&D Field", markers=True,
                title="Expenditures by R&D field from 2016 to 2022",
                labels={'"Expenditures": "Expenditures (Dollars )"'},
                color_discrete_sequence=px.colors.qualitative.Set2)
fig.update_layout(yaxis_title="Dollars ",legend={'traceorder':'normal'})
st.plotly_chart(fig,use_container_width=True)




st.subheader("Federal Expenditures by R&D field for "+SchoolName)
RDF=Federal.groupby(["year","Institution"])[field].sum().reset_index()
RDF=pd.melt(RDF,id_vars=["year","Institution"],value_vars=field).rename(columns={"variable":"R&D Field","value":"Expenditures"}).sort_values(by=["year","Expenditures"],ascending=False)
#st.write(RD)
col1,col2=st.columns([3,1],gap="small")
with col1:
    fig = px.bar(RDF[RDF["year"]==2022].sort_values(by=["Expenditures"],ascending=False), x="R&D Field", y="Expenditures", color="R&D Field",
            color_discrete_sequence=px.colors.qualitative.Set2,
        labels={
                "Expenditures": "Dollars ","SubSubField":""
},
        title="Federal Expenditures by R&D field on 2022")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig,use_container_width=True)
with col2:
    pie = px.pie(RDF[RDF["year"]==2022], values='Expenditures', names="R&D Field", 
                    color_discrete_sequence=px.colors.qualitative.Set2)
    pie.update_traces(textposition='inside', textinfo="label+percent",hovertemplate = "%{label}: %{percent:.1%} <br>$:%{value}")
    pie.update_layout(showlegend=False)
    st.plotly_chart(pie,use_container_width=True)

fig = px.line(RDF, x="year", y="Expenditures", color="R&D Field", markers=True,
        title="Federal Expenditures by R&D field from 2016 to 2022",
        labels={'"Expenditures": "Expenditures "'},
        color_discrete_sequence=px.colors.qualitative.Set2)
fig.update_layout(yaxis_title="Dollars",legend={'traceorder':'normal'})
st.plotly_chart(fig,use_container_width=True)
st.subheader("Each Funding Source for "+SchoolName)
st.write("These Funds Source are part of Federal Agency Funds: NSF, USDA, HHS, DOD, DOE, NASA and Other")
st.write("R&D Field abbreviation: CI: Computer and information sciences, GAO: Geosciences, atmospheric sciences, and ocean sciences, MS: Mathematics and statistics")

#st.write(combine)
#st.write(Federal)
#st.write(ALL)
col1,col2=st.columns([1,1],gap="small")
with col1:
     #st.write("#")
     st.info("Funding Source")
with col2:
     selected_source= st.selectbox(
"Please select one Funding Source below",
combine['FundsSource'].unique())
FundsSource=combine[combine["FundsSource"]==selected_source]
#st.write(FundsSource)
col1,col2=st.columns([3,1],gap="small")
with col1:
    fig = px.bar(FundsSource[FundsSource["year"]==2022].sort_values(by=["Expenditures"],ascending=False), x="R&D Field", y="Expenditures", color="R&D Field",
            color_discrete_sequence=px.colors.qualitative.Set2,
        labels={
                "Expenditures": "Dollars ","SubSubField":""
},
        title=selected_source +" Expenditures by R&D field on 2022")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig,use_container_width=True)
with col2:
    pie = px.pie(FundsSource[FundsSource["year"]==2022], values='Expenditures', names="R&D Field",
                    color_discrete_sequence=px.colors.qualitative.Set2)
    pie.update_traces(textposition='inside', textinfo="label+percent",hovertemplate = "%{label}: %{percent:.1%} <br>$:%{value}")
    pie.update_layout(showlegend=False)
    st.plotly_chart(pie,use_container_width=True)
fig = px.bar(FundsSource, x="year", y="Expenditures", color="R&D Field",
                title=selected_source+" on Research Field by year",color_discrete_sequence=px.colors.qualitative.Set2)
fig.update_layout(yaxis_title="Dollars")
st.plotly_chart(fig,use_container_width=True)
st.divider()

st.subheader("Expenditures by Research Field and Agency for "+SchoolName)
#st.write(ALL)

col1,col2=st.columns([1,1],gap="small")
with col1:
     #st.write("#")
     st.info("Select by Year")
with col2:
     year= st.selectbox(
"Please select a year",
ALL['year'].unique())

RDA=ALL.groupby(["year","Institution","FundsSource"])[field].sum().reset_index()
RDA=pd.melt(RDA,id_vars=["year","Institution","FundsSource"],value_vars=field).rename(columns={"variable":"R&D Field","value":"Expenditures"}).sort_values(by=["year","Expenditures"],ascending=False)
#st.write(RDA)

fig = px.bar(RDA[RDA['year']==year], y="R&D Field", x="Expenditures", color="FundsSource",orientation='h',
            title="Expenditure by Research Field and Agency in " +str(year),color_discrete_sequence=px.colors.qualitative.Set1)
st.plotly_chart(fig,use_container_width=True)
fig = px.bar(RDA[RDA['year']==year], y="FundsSource", x="Expenditures", color="R&D Field",orientation='h',
            color_discrete_sequence=px.colors.qualitative.Set2,)
st.plotly_chart(fig,use_container_width=True)


#st.write(Federal)
FA=Federal.groupby(["year","Institution","FundsSource"])[field].sum().reset_index()
FA=pd.melt(FA,id_vars=["year","Institution","FundsSource"],value_vars=field).rename(columns={"variable":"R&D Field","value":"Expenditures"}).sort_values(by=["year","Expenditures"],ascending=False)
fig = px.bar(FA[FA['year']==year].sort_values(by=["Expenditures"],ascending=False), y="R&D Field", x="Expenditures", color="FundsSource",orientation='h',
            title="Federally finanaced academic R&D expenditure by Research Field and Agency in "+str(year),color_discrete_sequence=px.colors.qualitative.Set1)
st.plotly_chart(fig,use_container_width=True)
fig = px.bar(FA[FA['year']==year].sort_values(by=["Expenditures"],ascending=False), y="FundsSource", x="Expenditures", color="R&D Field",orientation='h',
            color_discrete_sequence=px.colors.qualitative.Set2)
st.plotly_chart(fig,use_container_width=True)


fig = px.bar(combine[combine['year']==year].sort_values(by=["Expenditures"],ascending=False), y="R&D Field", x="Expenditures", color="FundsSource",orientation='h',
            title="Expenditure by Research Field and Agency in "+str(year),color_discrete_sequence=px.colors.qualitative.Set1)
st.plotly_chart(fig,use_container_width=True)
fig = px.bar(combine[combine['year']==year].sort_values(by=["Expenditures"],ascending=False), y="FundsSource", x="Expenditures", color="R&D Field",orientation='h',
            color_discrete_sequence=px.colors.qualitative.Set2)
#fig.update_layout(legend=dict(orientation="h",yanchor="top",y=1.02,xanchor="right",x=1))
st.plotly_chart(fig,use_container_width=True)
st.write("These Funds Source are part of Federal Agency Funds: NSF, USDA, HHS, DOD, DOE, NASA and Other")