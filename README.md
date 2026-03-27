# Clinical Trial Performance & Analytics Dashboard 🔬

**Live Demo:** [Insert your Live Streamlit URL here]

## 📌 Project Overview
This project is an interactive, end-to-end data analytics dashboard designed to monitor and analyze global clinical trial performance. Built with **Python, Pandas, Plotly, and Streamlit**, it transforms raw clinical registry data into actionable healthcare insights, mirroring the daily workflows of Global Data Science & Analytics (GDSA) teams in the life sciences sector.

The dashboard focuses on real-world evidence (RWE), tracking patient enrollment funnels, geographic trial distribution, and pipeline maturity across different therapeutic areas.

## 🚀 Key Features & Analytics
* **Patient Conversion Funnel:** Models the attrition rate across the clinical trial lifecycle (Screening → Enrollment → Treatment → Retention → Outcome).
* **Dynamic KPI Tracking:** Real-time calculation of total trials, global enrollment volume, average trial duration, and active recruiting status.
* **Therapeutic Area Segmentation:** Highlights top clinical conditions (e.g., Oncology, Cardiovascular) to identify research concentration.
* **Geographic & Sponsor Distribution:** Identifies top-performing trial locations and major industry vs. institutional sponsors.
* **Pipeline Maturity:** Visualizes the distribution of trials across clinical phases (Phase 1–4).
* **Time-Series Analysis:** Tracks monthly trial registration trends over a rolling 12-month period.

## 🛠️ Technical Stack
* **Language:** Python 3.x
* **Data Processing & Cleaning:** Pandas, NumPy
* **Data Visualization:** Plotly Express, Plotly Graph Objects
* **Web Framework & Deployment:** Streamlit, Streamlit Community Cloud

## 📂 Project Structure
```text
clinical-analytics-dashboard/
├── data/
│   ├── processed/
│   │   └── clean_clinical_data.csv    # Cleaned and engineered dataset
│   └── raw/                           # Raw dataset (ignored in version control)
├── notebooks/
│   ├── 01_data_prep.ipynb             # Data cleaning, handling nulls, and feature engineering
│   └── 02_dashboard_visuals.ipynb     # Exploratory Data Analysis (EDA) and Plotly prototyping
├── app.py                             # Main Streamlit web application script
├── requirements.txt                   # Project dependencies
└── README.md                          # Project documentation
```

## ⚙️ How to Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/YOUR-USERNAME/clinical-trial-analytics-dashboard.git
cd clinical-trial-analytics-dashboard
```

**2. Create and activate a virtual environment**

*For Windows:*
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

*For macOS/Linux:*
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the Streamlit app**
```bash
streamlit run app.py
```

## 💡 Business Value (Alignment with GDSA Workflows)
This project demonstrates core competencies required for life sciences data analytics, including:

* **Real-World Data Processing:** Handling missing values, standardizing dates, and engineering clinical metrics from raw datasets.
* **Interactive Decision Support:** Building tools that allow stakeholders to slice data by phase, condition, and status for strategic trial planning.
* **Data Storytelling:** Utilizing clean, heavily structured visual hierarchies to communicate complex medical data simply and effectively.

---
*Developed by Anmol Santwani | [LinkedIn](https://www.linkedin.com/in/anmol-santwani-90b676215/)*