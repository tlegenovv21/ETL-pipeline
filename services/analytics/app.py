# services/analytics/app.py

import streamlit as st
import pandas as pd
from pymongo import MongoClient
from minio import Minio
import os
from collections import Counter
import plotly.express as px

# --- Configuration & Connections ---
st.set_page_config(page_title="ETL Analytics Dashboard", layout="wide")
st.title("📊 Data Engineering Analytics Dashboard")

# Connect to MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:supersecretkey@mongo:27017/")
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client["metadata_db"]
    collection = db["metadata"]
    # Fetch all documents, excluding the internal MongoDB '_id' field
    data = list(collection.find({}, {"_id": 0}))
except Exception as e:
    st.error(f"Failed to connect to MongoDB: {e}")
    data = []

if not data:
    st.warning("No data found in MongoDB. Please run the ETL pipeline first!")
    st.stop()

# Convert data to a Pandas DataFrame for easy manipulation
df = pd.DataFrame(data)

# --- Layout: 2 Columns ---
col1, col2 = st.columns(2)

# ==========================================
# REQUIREMENT 1: Statistics by Data Type
# ==========================================
with col1:
    st.subheader("📈 Data Types Distribution")
    if 'data_type' in df.columns:
        type_counts = df['data_type'].value_counts().reset_index()
        type_counts.columns = ['Data Type', 'Count']
        
        # Create a pie chart using Plotly
        fig_pie = px.pie(type_counts, names='Data Type', values='Count', hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

# ==========================================
# REQUIREMENT 4: Top 10 Most Frequent Words
# ==========================================
with col2:
    st.subheader("🔠 Top 10 Words (Text Data)")
    text_data = df[df['data_type'] == 'text']
    
    if not text_data.empty and 'metadata' in text_data.columns:
        all_tokens = []
        # Extract tokens from the metadata of text documents
        for meta in text_data['metadata']:
            if isinstance(meta, dict) and 'tokens' in meta:
                all_tokens.extend(meta['tokens'])
                
        if all_tokens:
            # Count the most common words
            word_counts = Counter(all_tokens).most_common(10)
            words_df = pd.DataFrame(word_counts, columns=['Word', 'Frequency'])
            
            # Create a bar chart
            fig_bar = px.bar(words_df, x='Word', y='Frequency', color='Frequency')
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No tokens found in text metadata.")
    else:
        st.info("No text data available to analyze.")

st.divider()

# ==========================================
# REQUIREMENT 2: Search by Tags/Keywords
# ==========================================
st.subheader("🔍 Search Metadata")
search_query = st.text_input("Enter a keyword to search in the database:")

if search_query:
    # Filter the DataFrame based on the search query (case-insensitive)
    mask = df.astype(str).apply(lambda x: x.str.contains(search_query, case=False, na=False)).any(axis=1)
    filtered_df = df[mask]
    st.dataframe(filtered_df, use_container_width=True)
else:
    st.dataframe(df, use_container_width=True)

st.divider()

# ==========================================
# REQUIREMENT 3: Image Previews (and MinIO connection)
# ==========================================
st.subheader("🖼️ Image Previews")
image_data = df[df['data_type'] == 'image']

if not image_data.empty:
    # Create columns to display images in a grid
    image_cols = st.columns(3)
    
    for index, row in image_data.iterrows():
        # The image URL is stored in the 'content' field
        img_url = row.get('content')
        meta = row.get('metadata', {})
        description = meta.get('description', 'No description')
        
        with image_cols[index % 3]:
            # Streamlit can render the image directly from the URL
            st.image(img_url, caption=description, use_column_width=True)
else:
    st.info("No images found in the database.")

# Optional: Prove MinIO connection works
with st.expander("View Files Stored in MinIO (Raw & Processed Buckets)"):
    try:
        minio_client = Minio(
            os.getenv("MINIO_ENDPOINT", "minio:9000"),
            access_key=os.getenv("MINIO_ACCESS_KEY", "admin"),
            secret_key=os.getenv("MINIO_SECRET_KEY", "supersecretkey"),
            secure=False
        )
        objects = minio_client.list_objects("processed-data", recursive=True)
        st.write("Files in `processed-data` bucket:")
        st.write([obj.object_name for obj in objects])
    except Exception as e:
        st.error(f"Could not connect to MinIO: {e}")