import streamlit as st
import pymongo


class AppDatabase:
    # Initialize connection.
    # Uses st.experimental_singleton to only run once.
    @st.experimental_singleton
    def init_connection():
        return pymongo.MongoClient(**st.secrets["mongo"])



