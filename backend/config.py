# import os
# from dotenv import load_dotenv
import supabase
import streamlit as st

# for local .env variables
# load_dotenv()

SUPABASE_URL: str = st.secrets["SUPABASE_URL"]
SUPABASE_ANON_KEY: str = st.secrets["SUPABASE_ANON_KEY"]
SUPABASE_BUCKET: str = st.secrets["SUPABASE_BUCKET"]
SUPABASE_TABLE: str = st.secrets["SUPABASE_TABLE"]

if SUPABASE_URL == "" or SUPABASE_ANON_KEY == "":
    raise ValueError("Empty keys while initialization")

client = supabase.create_client(SUPABASE_URL, SUPABASE_ANON_KEY)