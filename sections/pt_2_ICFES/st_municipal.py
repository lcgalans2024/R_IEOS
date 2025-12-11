import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import altair as alt
from streamlit_extras.metric_cards import style_metric_cards

def ranking(df=None, variable=None):
    st.header("Análisis ET 📈")