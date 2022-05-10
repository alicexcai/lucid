import streamlit as st
import pandas as pd
import pygsheets
from datetime import datetime
import openai
import requests

def app():
    
    # SET APP PROPERTIES

    st.title("ABOUT LUCID")
    
    st.write("Lucid is an incubation tool for lucid dreaming...")