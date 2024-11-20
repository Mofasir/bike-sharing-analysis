# 🚲 Bike Sharing Analysis Dashboard
This project provides an interactive dashboard for analyzing bike rental data. The dashboard explores patterns in bike rentals influenced by factors such as weather, seasons, user types, and more.

## Live Dashboard Access
To access the deployed dashboard, click on the following link:  
[Live Dashboard](https://bike-sharing-analysis-mofasir.streamlit.app/)

## Running the Dashboard Locally
Follow the steps below to run the dashboard on your local machine.

### 1. Setup Environment (Using Shell/Terminal)
**Create a project directory and set up Pipenv**
```
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
```
**Install dependencies**
```
pip install -r requirements.txt
```

### 2. Run the Streamlit App
```
cd dashboard
streamlit run dashboard.py
```
The app will open in your default browser. If it doesn't, navigate to the URL shown in your terminal (usually `http://localhost:8501`)

## Dashboard Features
- **Filters**: Select a spesific date range for analysis.
- **Visualizations**: Interactive bar charts, line plots, and more for exploring trends.  
