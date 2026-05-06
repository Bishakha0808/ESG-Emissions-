# ESG Emissions Dashboard

This repository contains an interactive ESG (Environmental, Social, Governance) emissions dashboard built with Streamlit, along with data cleaning, analysis, and reporting tools.

## Features
- Cleaned ESG emissions dataset
- Streamlit dashboard with KPI cards, charts, and filters
- PDF report generation
- Power BI/Excel dashboard instructions

## Getting Started

### 1. Clone the Repository
```
git clone <repo-url>
cd <repo-folder>
```

### 2. Install Dependencies
It is recommended to use a virtual environment:
```
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

If you do not have a requirements.txt, install manually:
```
pip install streamlit pandas plotly
```

### 3. Prepare the Data
Ensure the cleaned data file exists as:
```
ESG Data Analytics Task.cleaned.csv
```
If not, run the notebook or scripts to generate it from the raw CSV.

### 4. Run the Streamlit Dashboard
```
streamlit run task.py
```

The dashboard will open in your browser. Use the sidebar filters to interact with the data.

### 5. Generate the PDF Report (Optional)
Open `esg_report_pdf.ipynb` in Jupyter/VS Code and run all cells. This will create `ESG_Emissions_Final_Report.pdf`.

## Project Structure
- `task.py` — Main Streamlit dashboard app
- `ESG Data Analytics Task.cleaned.csv` — Cleaned dataset
- `esg_report_pdf.ipynb` — Notebook for PDF report export
- `report_for_pdf.md` — Markdown version of the final report
- `data.ipynb` — Data cleaning and analysis notebook

## Power BI/Excel Dashboard
Instructions for building a Power BI or Excel dashboard are provided in the notebook and report.

## License
Specify your license here.
