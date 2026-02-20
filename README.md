# Data Engineering ETL Pipeline & Analytics Dashboard

A fully containerized Data Engineering pipeline that extracts unstructured data (text, images, logs), transforms it using Python, and loads it into MinIO (Object Storage) and MongoDB (NoSQL). The project includes a Streamlit web application for data analytics and visualization.

---

## 1. Architecture Schema

```mermaid
graph TD
    %% Extract Phase
    subgraph Extract Phase
        A[Wikipedia API] -->|JSON| E[Python Extractors]
        B[Unsplash API] -->|JSON| E
        C[Synthetic Logs] -->|Text| E
    end

    %% Transform Phase
    subgraph Transform Phase
        E -->|Raw Data| T[Python Transformers]
        T -->|Clean Text & langdetect| U[Unified Metadata Schema]
        T -->|Image Hash & PIL| U
        T -->|Regex Parsed Logs| U
    end

    %% Load Phase
    subgraph Load Phase
        E -.->|Save Raw Output| M1[(MinIO: raw-data)]
        U -->|Save Metadata JSON| DB[(MongoDB: metadata)]
        U -->|Save Processed Files| M2[(MinIO: processed-data)]
    end

    %% Analytics Phase
    subgraph Analytics Phase
        DB -->|Query Metadata| S[Streamlit Dashboard]
        M2 -->|Fetch Images| S
    end
---

## 2. Access the Web Interfaces
Once the containers are running, you can access the three main UI components. Below are the default local credentials (configurable via `.env`).

📊 **1. Analytics Dashboard (Streamlit)**
* **URL:** [http://localhost:8501]
* **Authentication:** None required.
* **What to look for:** View the distribution pie chart, explore the top 10 words, and search the unified metadata.

🍃 **2. MongoDB Database UI (Mongo Express)**
* **URL:** [http://localhost:8081]
* **Username:** `admin`
* **Password:** `pass`  
* **What to look for:** Click on the `metadata_db` database, then click on the `metadata` collection to view all the processed JSON documents.

🪣 **3. MinIO Object Storage Console**
* **URL:** [http://localhost:9001]
* **Username:** `admin`
* **Password:** `supersecretkey`
* **What to look for:** Click on "Object Browser" in the left menu to explore the files saved inside the `raw-data` and `processed-data` buckets.


![Analytics Dashboard]
(dashboard.jpg)