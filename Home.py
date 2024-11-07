import streamlit as st
from streamlit.logger import get_logger
from PIL import Image
LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="HERD",
        page_icon="👋",
    )

    st.write("# HERD Dashboard 👨‍🎓👩‍🎓")

    #st.sidebar.success("Select a page above.")
    
    st.markdown(
        """
        
        Higher Education Research and Development (HERD) Survey is an annual census of U.S. colleges and universities that expended at least $150,000 in separately accounted-for R&D in the fiscal year. 
        The survey collects information on R&D expenditures by field of research and source of funds and also gathers information on types of research, expenses, 
        and headcounts of R&D personnel.
        
        ### Want to learn more?
        
        - [Survey-Info](https://ncses.nsf.gov/surveys/higher-education-research-development/2021#survey-info)
        - [Methodology](https://ncses.nsf.gov/surveys/higher-education-research-development/2021#methodology)
        - [Data](https://ncses.nsf.gov/surveys/higher-education-research-development/2021#data)
        - [Analysis](https://ncses.nsf.gov/surveys/higher-education-research-development/2021#analysis)
    
        
        
    """ )
    
    author_dtl = "<strong>Happy Learning: 😎 Shuai Liu: shuail@uark.com</strong>"    
    st.markdown(author_dtl, unsafe_allow_html=True)
if __name__ == "__main__":
    run()


#streamlit run c:/Users/shuail/VScode/HERD-app/Home.py
#python -m streamlit run c:/Users/shuail/VScode/HERD-app/Home.py