import os
from dotenv import load_dotenv
from supabase import create_client, Client
import streamlit as st

# Load local .env if it exists
load_dotenv()

# Prefer Streamlit Cloud secrets if available
SUPABASE_URL = os.getenv("SUPABASE_URL") or st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "Missing Supabase credentials. Please set SUPABASE_URL and SUPABASE_KEY "
        "in your .env file (for local) or Streamlit Cloud Secrets (for deployment)."
    )

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
