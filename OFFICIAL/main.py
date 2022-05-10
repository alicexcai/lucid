import streamlit as st

from multipage import MultiPage
from pages import dream, about

app = MultiPage()
apptitle = 'LUCID'
st.set_page_config(page_title=apptitle, page_icon=":moon:")
st.sidebar.markdown("## Select a page")

app.add_page("DREAM", dream.app)
app.add_page("ABOUT", about.app)

app.run()