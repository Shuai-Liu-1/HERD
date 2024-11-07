import pandas as pd
import plotly.express as px
import streamlit as st
import plotly
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from plotly.colors import find_intermediate_color
#import matplotlib.pyplot as plt
#import mercury as mr
import warnings
from pandas.errors import SettingWithCopyWarning
warnings.simplefilter(action='ignore', category=(SettingWithCopyWarning))

plot_data=pd.read_csv("ExpendituresFrom1953.csv")
plot_data=plot_data[plot_data['Year']>=2016]
plot_data=plot_data[plot_data['source']!='All R&D expenditures']
#st.write(plot_data)
@st.cache_data
def type_data():
    df=pd.read_csv("nsf24308-tab009.csv",header=4).rename(columns={"Unnamed: 0":"Year"})
    pie_data=pd.melt(df,id_vars=['Year'],value_vars=df.columns[2:5]).rename(columns={"value": "Expenditures","variable":"source"})
    pie_data['Year']=pie_data['Year'].astype("object")
    return pie_data
pie_data=type_data()
#st.write(pie_data)
#sunAgency=pd.read_csv("C:/Users/shuail/VScode/HERD-app/SunAgency.csv")
#st.write(sunAgency)

##plot 1
st.header("Funding Source ")
st.markdown("""Research and development (R&D) spending by academic institutions totaled $97.8 billion in FY 2022""")
st.markdown(
    """R&D expenditures at higher education institutions originate from five main sources:
    **the Federal government, State and local government, institutional funds, business , and all other sources**.
    Federal government funded R&D at universities totaled almost $54 billion in FY 2022, which accounted for 55% of total expenditure. (Overview Funding Source on 2022)""" )

st.write("""There are three main type of R&D:**basic research, allplied research, and expenrimental development**,  
         basic research at universities totaled almost $62 billion in FY 2022, which accounted for 63% of total expenditure. (Overview R&D Type on 2022)""")

col1,col2=st.columns([1,1],gap="medium")
with col1:
    #st.subheader("Overview Funding Source on 2022 (Dollars in thousands)")
    fig3 = px.pie(plot_data[plot_data["Year"]==2022], values='Expenditures', names='source', 
                  title='Funding Source on 2022 (Dollars in Billions)',color_discrete_sequence=px.colors.qualitative.Set1)
    fig3.update_traces(textposition='inside', textinfo="label+percent",hovertemplate = "%{label}: %{percent:.1%} <br>$:%{value} B")
    #fig3.update(layout_showlegend=False)
    #fig3.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    #fig3.update_layout(legend=dict(orientation="v", y=1.5, x=0.5, xanchor="center"))
    fig3.update_layout(showlegend=False)
    st.plotly_chart(fig3,use_container_width=True)
with col2:
    fig1 = px.pie(pie_data[pie_data["Year"]==2022], values='Expenditures', names='source',
                   title='R&D Type on 2022 (Dollars in Billions)',color_discrete_sequence=px.colors.qualitative.Set3)
    fig1.update_traces(textposition='inside', textinfo="label+percent",hovertemplate = "%{label}: %{percent:.1%} <br>$:%{value} B")
    #fig1.update_layout(legend=dict(orientation="h", y=1.5, x=0.5, xanchor="center"))
    fig1.update_layout(showlegend=False)
    st.plotly_chart(fig1,use_container_width=True)
#with st.sidebar:
       # st.markdown("Overview Funding Source on 2022 (Dollars in thousands)")
        #sidebarlogo = st.plotly_chart(fig3,use_container_width=True)
        #st.image(sidebarlogo, use_column_width='auto')

#----------------------------------------
#plot2
st.subheader("Funding Source from 2016 to 2022")
reordered_colors = [
    px.colors.qualitative.Set1[0],  # Green
    px.colors.qualitative.Set1[4],  # Red
    px.colors.qualitative.Set1[1],  # Blue
    px.colors.qualitative.Set1[3],  # Purple
    px.colors.qualitative.Set1[2]
]
fig = px.line(plot_data, x="Year", y="Expenditures", color="source", markers=True,
            #title="Funding Source from differnt Federal Agency",
            labels={'"Expenditures": "Expenditures (Dollars)"'},
            color_discrete_sequence=reordered_colors)
fig.update_layout(yaxis_title="Billion of Dollars",legend={'traceorder':'normal'})
st.plotly_chart(fig,use_container_width=True)
#------------------------------------------------------------------------
#selected_source = st.multiselect(
 #   'Please choose one or more sources to observe the trend from 2016 to 2022',
 #   ['Federal government','State and local government',"Institution funds","Business","All other sources"],default=['Federal government','State and local government'])
#selected_source_data=plot_data[plot_data["source"].isin(selected_source)]


#fig = make_subplots(rows=1, cols=2)
#source=['All R&D expenditures', 'Federal government',
#       'State and local government', 'Institution funds', 'Business',
#       'All other sources']
#color=["darkgrey",'#636EFA', '#EF553B', '#00CC96', '#FFA15A','#AB63FA' ]

#for i in range(len(source)):
#    fig.add_trace(go.Scatter(x=selected_source_data.Year, y=selected_source_data[selected_source_data['source']==source[i]]['Expenditures'],
#                         name=source[i], legendgroup=source[i],mode='markers+lines',
#                         line=dict(color=color[i]),
#                            showlegend=True),
#              row=1, col=1)
    
#for i in range(len(source)):
#     fig.add_trace(go.Scatter(x=selected_source_data.Year, y=selected_source_data[selected_source_data['source']==source[i]]['Percentage'],
#                         name=source[i], legendgroup=source[i],mode='markers+lines',
 #                        line=dict(color=color[i]),
 #                            showlegend=False),
 #             row=1, col=2)
 
#fig.update_layout(yaxis=dict(title=dict(text="Expenditures (Dollars in Billions)"),side="left"),
#                  yaxis2=dict(title=dict(text="Percentage %"), side="right"),yaxis2_range=[0,100],)
#                  #title="Expenditures by source of funds from 1953 to 2022")
#fig.update_layout(legend=dict(orientation="h",y=1.02,xanchor="right", x=1))

#st.plotly_chart(fig,use_container_width=True)
#----------------------------------------------------------------
#Animation Plot
#with st.expander("Animation Plot"):
#   fig2=px.scatter(selected_source_data, x="Year", y="Percentage", animation_frame="Year", animation_group="source",
 #           size="Percentage", size_max=55,color="source", hover_name="source", range_y=[0,75],range_x=[2016,2022],color_discrete_map=dict(map(lambda i,j : (i,j) , source,color)))
  #  fig2.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 50
   # st.plotly_chart(fig2,use_container_width=False)

st.divider()


#--------------------------------------------------------------------
#plot3
st.subheader("Funding Source from different Federal Government Agency from 2016 to 2022")

st.markdown("""
- The Department of Health and Human Services (HHS), which includes the National Institutes of Health, supported the largest federal share of R&D at $30.3 billion.
This amounted to 31% of total R&D at higher education institutions in FY 2022 and 56% of total federal R&D support. """)
st.markdown("""
- The Department of Defense (DOD) (8.0 billion) and the National Science Foundation (NSF)(6.0 billion) accounted for most of the remaining federally funded expenditures, 
while three other agencies supported between 1.5 billion and 2.5 billion of university R&D in FY 2022: 
the Department of Energy (DOE) (2.5 billion), the National Aeronautics and Space Administration (NASA) (2.0 billion), and the Department of Agriculture (USDA) (1.5 billion). 
All other federal agencies combined supported 3.6 billion of higher education R&D in FY 2022.""")
@st.cache_data
def load_data():
    df=pd.read_csv("FederalAgency.csv")
    return df
FederalAgency=load_data()

def load_data1():
    df1=pd.read_csv("SunAgency.csv")
    return df1
SunAgency=load_data1()
columns={"Computer and information sciences":"CI","Geosciences, atmospheric sciences, and ocean sciences":"GAO","Mathematics and statistics":"MS",
         "Sociology, demography, and population studies":"SDP","Natural resources and conservation":"NRC","Aerospace, aeronautical, and astronautical engineering":"AAA","Communication and communications technologies":"CCT",
         "Atmospheric science and meteorology":"ASM","Ocean sciences and marine sciences":"OSMS","Biological and biomedical sciences":"BBS","Geological and earth sciences":"GES","Geosciences, atmospheric sciences, and ocean sciences nec":"GAON",
         "Political science and government":"PSG","Astronomy and astrophysics":"AA","Electrical, electronic, and communications engineering":"EECE","Metallurgical and materials engineering":"MME",
         "Industrial and manufacturing engineering":"IME", "Bioengineering and biomedical engineering":"BBE","Mechanical engineering":"ME","Business management and business administration":"BBA",
         "Visual and performing arts":"VPA"}
#FederalAgency['SubField']=FederalAgency['SubField'].replace(columns)
#FederalAgency['SubSubField']=FederalAgency['SubSubField'].replace(columns)




AgencySum=FederalAgency.groupby(["Federal Agency","Year"])[["Expenditures"]].sum().reset_index()
AgencySum=AgencySum.sort_values(by=["Year","Expenditures"],ascending=False)

#st.write(AgencySum)





col1,col2=st.columns([3,1],gap="small")
with col2:
    pie3 = px.pie(AgencySum[AgencySum["Year"]==2022], values='Expenditures', names='Federal Agency', title='Year 2022',
                  )
    pie3.update_traces(textposition='inside', textinfo="label+percent",hovertemplate = "%{label}: %{percent:.1%} <br>$:%{value}")
    pie3.update_layout(showlegend=False)
    st.plotly_chart(pie3,use_container_width=True)
with col1:
    fig = px.line(AgencySum, x="Year", y="Expenditures", color="Federal Agency", markers=True,
            title="Funding Source from differnt Federal Agency",
            labels={'"Expenditures": "Expenditures (Dollars)"'},
           )
    fig.update_layout(yaxis_title="Dollars",legend={'traceorder':'normal'})
    st.plotly_chart(fig,use_container_width=True)


st.divider()
#----------------------------------------------------------------------------------
#select one Federal Agency Plot

col1,col2=st.columns([1,2],gap="small")
with col1:
     #st.write("#")
     st.info("Funding Source By Federal Agency")
with col2:
     selected_source= st.selectbox(
"Please select one Federal Agency below",
FederalAgency['Federal Agency'].unique(),index=1)
     


FASelected=FederalAgency[FederalAgency['Federal Agency']==selected_source]
SumField1=FASelected.groupby(["Field","Year"])[["Expenditures"]].sum().reset_index()
#st.write(SumField1)

col1,col2=st.columns([3,1],gap="small")
with col2:
    pie4=px.pie(SumField1[SumField1["Year"]==2022], values='Expenditures', names='Field', title='Year 2022',
                  color_discrete_sequence=px.colors.qualitative.Dark2)
    pie4.update_traces(textposition='inside', textinfo="label+percent",hovertemplate = "%{label}: %{percent:.1%} <br>$:%{value}")
    pie4.update_layout(showlegend=False)
    st.plotly_chart(pie4,use_container_width=True)
    #data=dfN1[["Institution","year","All R&D expenditures"]].groupby(by='year')['All R&D expenditures'].reset_index()
with col1:
    fig = px.line(SumField1.sort_values(by=["Year","Expenditures"],ascending=False), x="Year", y="Expenditures", color="Field", markers=True,
                  color_discrete_sequence=px.colors.qualitative.Dark2,
              labels={
                     "Expenditures": "Dollars",
},
              title="Funding Source from "+selected_source+" By Three Main Research field")
    st.plotly_chart(fig,use_container_width=True)
st.markdown(""" nec = not elsewhere classfified; S&E = Science and Engineering""")


###
col1,col2=st.columns([1,2],gap="small")
with col1:
     #st.write("#")
     st.info("Funding Source from "+  selected_source+ " By Research Field")
with col2:
     selected_field= st.selectbox(
"Please select one Main Research Field",
FederalAgency['Field'].unique())
FASelected=FederalAgency[FederalAgency['Federal Agency']==selected_source]     
FieldSelected=FASelected[FASelected['Field']==selected_field]     
#SubField
subfield=FieldSelected.groupby(["SubField","Field","Federal Agency","Year"])['Expenditures'].sum().reset_index()
color_Science=["rgb(27, 158, 119)","rgb(54, 172, 134)","rgb(81, 186, 149)","rgb(108, 200, 164)","rgb(135, 214, 179)","rgb(162, 227, 194)","rgb(189, 241, 209)","rgb(216, 255, 224)","rgb(230, 255, 234)"]
color_Engineering=["rgb(217, 95, 2)","rgb(225, 115, 38)","rgb(232, 135, 74)","rgb(240, 155, 110)","rgb(247, 175, 146)","rgb(249, 189, 168)","rgb(252, 202, 189)","rgb(255, 215, 211)","rgb(255, 215, 211)"]
color_Non=["rgb(117, 112, 179)","rgb(133, 128, 189)","rgb(149, 144, 199)","rgb(165, 160, 209)","rgb(181, 176, 219)","rgb(197, 192, 229)","rgb(213, 208, 239)","rgb(229, 224, 249)","rgb(229, 224, 249)"]
color_dict = {
    "Engineering": color_Engineering,
    "Science": color_Science,
    "Non-S&E": color_Non
}

color_df = pd.DataFrame(color_dict)
#if selected_source=="Engineering":
    #color=color_engineering
color=color_df[selected_field]    
#st.write(color)
##st.write(subfield)


col1,col2=st.columns([3,1],gap="small")
with col2:
    pie4=px.pie(subfield[subfield["Year"]==2022], values='Expenditures', names='SubField',
                    color_discrete_sequence=color)
    pie4.update_traces(textposition='inside', textinfo="label+percent",hovertemplate = "%{label}: %{percent:.1%} <br>$:%{value}")
    pie4.update_layout(showlegend=False)
    st.plotly_chart(pie4,use_container_width=True)
        #data=dfN1[["Institution","year","All R&D expenditures"]].groupby(by='year')['All R&D expenditures'].reset_index()
with col1:
    fig = px.bar(subfield[subfield["Year"]==2022].sort_values(by=["Expenditures"],ascending=False), x="SubField", y="Expenditures", color="SubField", 
                color_discrete_sequence=color,
                title="Funding Source from "+selected_source+" Federal Agency on "+selected_field+" in 2022",
                labels={
                    "Expenditures": "Dollars","SubField":""
})
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig,use_container_width=True)

fig = px.line(subfield.sort_values(by=["Year","Expenditures"],ascending=False), x="Year", y="Expenditures", color="SubField", 
                markers=True,color_discrete_sequence=color,
            labels={
                    "Expenditures": "Dollars",
},
            title="Funding Source from "+selected_source+" Federal Agency on "+selected_field+ " From 2016 to 2022")
st.plotly_chart(fig,use_container_width=True)


# expander plot
if selected_field=="Science":
    with st.expander("Funding Source from "+selected_source+" on "+selected_field+" Subfield"):

#SubSubFIeld
    #FieldSelected['SubSubField']=FieldSelected['SubSubField'].replace(columns)

        col1,col2=st.columns([3,1],gap="small")
        with col2:

            pie4=px.pie(FieldSelected[FieldSelected["Year"]==2022], values='Expenditures', names='SubSubField', title="", 
                            color_discrete_sequence=px.colors.qualitative.Set3_r)
            pie4.update_traces(textposition='inside', textinfo="label+percent",hovertemplate = "%{label}: %{percent:.1%} <br>$:%{value}")
            pie4.update_layout(showlegend=False)
            st.plotly_chart(pie4,use_container_width=True)
                #data=dfN1[["Institution","year","All R&D expenditures"]].groupby(by='year')['All R&D expenditures'].reset_index()
        with col1:
            fig = px.bar(FieldSelected[FieldSelected["Year"]==2022].sort_values(by=["Expenditures"],ascending=False), x="SubSubField", y="Expenditures", color="SubSubField", 
                   color_discrete_sequence=px.colors.qualitative.Set3_r,
                title="Funding Source from "+selected_source+" Federal Agency on "+selected_field+" in 2022",
                labels={
                    "Expenditures": "Dollars","SubSubField":""})
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig,use_container_width=True)

        fig = px.line(FieldSelected.sort_values(by=["Year","Expenditures"],ascending=False), x="Year", y="Expenditures", color="SubSubField", 
                            markers=True,color_discrete_sequence=px.colors.qualitative.Set3_r,
                        labels={
                                "Expenditures": "Dollars",
            },
                        title="Funding Source from "+selected_source+" on "+selected_field+" Subfield From 2016 to 2022")
        st.plotly_chart(fig,use_container_width=True)


with st.expander("More Spending Details from "+ selected_source+ " on Research Field"):
    ## TOP 10 ##
    Science=FederalAgency[FederalAgency['Field']=="Science"].groupby(["Field","Federal Agency","Year","SubField"])[["Expenditures"]].sum().reset_index().drop(columns=["Field"]).rename(columns={'SubField': 'Field'})
    EngNon=FederalAgency[FederalAgency['Field']!="Science"].groupby(["Field","Federal Agency","Year"])[["Expenditures"]].sum().reset_index()
    Top10=combined_df = pd.concat([Science, EngNon])
    Top10=Top10[Top10['Federal Agency']==selected_source]
    #st.write(Science)
    #st.write(EngNon)
    #st.write(Top10)

    col1,col2=st.columns([3,1],gap="small")
    with col2:
        pie = px.pie(Top10[Top10["Year"]==2022], values='Expenditures', names='Field', title='',
                    color_discrete_sequence=px.colors.qualitative.Set2)
        pie.update_traces(textposition='inside', textinfo="label+percent",hovertemplate = "%{label}: %{percent:.1%} <br>$:%{value}")
        pie.update_layout(showlegend=False)
        st.plotly_chart(pie,use_container_width=True)
    with col1:
        fig = px.bar(Top10[Top10["Year"]==2022].sort_values(by=['Expenditures'],ascending=False), x="Field", y="Expenditures", color="Field",
                title="Funding Source from "+selected_source+" by Top 10 research field in 2022",
                labels={"Expenditures": "Dollars ","Field":""},
                color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig,use_container_width=True)
    
    fig = px.line(Top10.sort_values(by=["Year",'Expenditures'],ascending=False), x="Year", y="Expenditures", color="Field", markers=True,
                title="Funding Source from "+selected_source+" by Top 10 research field From 2016 to 2022",
                labels={'"Expenditures": "Dollars "'},
                color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(yaxis_title="Dollars",legend={'traceorder':'normal'})
    st.plotly_chart(fig,use_container_width=True)
    st.divider()

    # subfield #
    #st.write(FASelected)
    subfieldALL=FASelected.groupby(["SubField","Field","Federal Agency","Year"])['Expenditures'].sum().reset_index()

    col1,col2=st.columns([3,1],gap="small")
    #st.write(subfieldALL)
    with col1:
        fig = px.bar(subfieldALL[subfieldALL["Year"]==2022].sort_values(by=["Expenditures"],ascending=False), x="SubField", y="Expenditures", color="SubField",
                    color_discrete_sequence=px.colors.qualitative.Set2,
                labels={
                        "Expenditures": "Dollars","SubField":""
    },
                title="Funding Source from "+selected_source+" By Sub Research field in 2022")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig,use_container_width=True)
    with col2:
        pie4=px.pie(subfieldALL[subfieldALL["Year"]==2022].sort_values(by=["Expenditures"],ascending=False), values='Expenditures', names='SubField', 
                    title='',
                    color_discrete_sequence=px.colors.qualitative.Set2)
        pie4.update_traces(textposition='inside', textinfo="label+percent",hovertemplate = "%{label}: %{percent:.1%} <br>$:%{value}")
        pie4.update_layout(showlegend=False)
        st.plotly_chart(pie4,use_container_width=True)

    fig = px.line(subfieldALL.sort_values(by=["Year","Expenditures"],ascending=False), x="Year", y="Expenditures", color="SubField", markers=True,
                    color_discrete_sequence=px.colors.qualitative.Set2,
                labels={
                        "Expenditures": "Dollars",
    },
                title="Funding Source from "+selected_source+" By Sub Research field from 2016 to 2022")
    st.plotly_chart(fig,use_container_width=True)
    st.divider()

        #data=dfN1[["Institution","year","All R&D expenditures"]].groupby(by='year')['All R&D expenditures'].reset_index()
    #subsubfield#
 
    col1,col2=st.columns([3,1],gap="small")
    with col1:
        fig = px.bar(FASelected[FASelected["Year"]==2022].sort_values(by=["Expenditures"],ascending=False), x="SubSubField", y="Expenditures", color="SubSubField",
                    color_discrete_sequence=px.colors.qualitative.Set2,
                labels={
                        "Expenditures": "Dollars ","SubSubField":""
    },
                title="Funding Source from "+selected_source+" By Sub Sub Research field in 2022")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig,use_container_width=True)
    with col2:
        pie4=px.pie(FASelected[FASelected["Year"]==2022].sort_values(by=["Expenditures"],ascending=False), values='Expenditures', names='SubSubField',
                    title='',
                    color_discrete_sequence=px.colors.qualitative.Set2)
        pie4.update_traces(textposition='inside', textinfo="label+percent",hovertemplate = "%{label}: %{percent:.1%} <br>$:%{value}")
        pie4.update_layout(showlegend=False)
        st.plotly_chart(pie4,use_container_width=True)
    fig = px.line(FASelected.sort_values(by=["Year","Expenditures"],ascending=False), x="Year", y="Expenditures", color="SubSubField", markers=True,
                    color_discrete_sequence=px.colors.qualitative.Set2,
                labels={
                        "Expenditures": "Dollars ","SubSubField":""
    },
                title="Funding Source from "+selected_source+" By Sub Sub Research field from 2016 to 2022")
    st.plotly_chart(fig,use_container_width=True)

       
