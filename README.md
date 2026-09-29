<div align="center">

# QDFS — BPC Electricity Demand Forecasting

**A Streamlit application comparing Moving Average and Exponential Smoothing for quarterly electricity demand forecasting at Botswana Power Corporation.**

[![Open Live App](https://img.shields.io/badge/Live%20App-Open%20QDFS-FF4B4B?logo=streamlit&logoColor=white)](https://qdfs-bpc-demand-forecasting-wdfhxttgccnfsrkrtiawaa.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Built with Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)

</div>

---

## Overview

The **Quantitative Demand Forecasting System (QDFS)** is a web-based forecasting application developed for an academic project focused on quarterly electricity demand forecasting at Botswana Power Corporation (BPC).

The application compares two quantitative forecasting techniques:

- **Moving Average (MA)** — uses a selected number of previous observations to calculate a forecast.
- **Exponential Smoothing (ES)** — combines the most recent actual observation with the previous forecast using a smoothing constant.

The project uses quarterly electricity distribution figures as a **proxy for demand**. Electricity distributed may not equal unconstrained demand when supply is restricted.

## Live application

**[Launch QDFS on Streamlit Community Cloud](https://qdfs-bpc-demand-forecasting-wdfhxttgccnfsrkrtiawaa.streamlit.app/)**

## Application screenshots

Add screenshots of the running app to the repository's `screenshots/` folder with the filenames below. Once uploaded, the images will appear here.

| Dashboard | Forecast results |
|---|---|
| `screenshots/dashboard.png` | `screenshots/forecast-results.png` |

| Accuracy analysis | Parameter testing |
|---|---|
| `screenshots/accuracy-analysis.png` | `screenshots/parameter-testing.png` |

## Project objectives

1. Generate quarterly forecasts using Moving Average and Exponential Smoothing.
2. Compare historical forecasting performance using Mean Absolute Deviation (MAD) and Mean Absolute Percentage Error (MAPE).
3. Present data, forecasts, and accuracy measures through an interactive dashboard.
4. Allow users to test model parameters.
5. Support export of forecast results and analysis.

## Forecasting methods

### 1. Moving Average

For a moving-average window of `n` observations:

\[
MA_t = \frac{A_{t-1} + A_{t-2} + \cdots + A_{t-n}}{n}
\]

The default window is **4 quarters**.

### 2. Exponential Smoothing

\[
F_t = \alpha A_{t-1} + (1-\alpha)F_{t-1}
\]

The default smoothing constant is **α = 0.4**. The initial forecast is set to the first actual observation.

### Accuracy measures

- **MAD (Mean Absolute Deviation):** the mean of the absolute differences between actual and forecast values.
- **MAPE (Mean Absolute Percentage Error):** the mean absolute error expressed as a percentage of actual values.

Lower MAD and MAPE values indicate smaller errors over the evaluation period. Comparisons should use the same evaluation period.

## Features

- Built-in quarterly BPC dataset.
- CSV and Excel file upload.
- Input validation for data quality.
- Adjustable Moving Average window and Exponential Smoothing alpha.
- Historical forecasts and next-quarter forecasts.
- MAD and MAPE accuracy analysis.
- Parameter testing for both forecasting methods.
- Forecast visualizations.
- CSV and Excel exports.

## Dataset

The built-in dataset covers **2020 Q1 to 2024 Q1** and contains quarterly electricity distribution values in MWh.

Uploaded files should contain these columns:

| Column | Description | Example |
|---|---|---|
| `Quarter` | Quarter label in chronological order | `2020 Q1` |
| `Actual_MWh` | Actual electricity distribution, in MWh | `1011335` |

Keep observations in chronological order. Avoid blank or duplicate quarter labels, missing values, and non-numeric actual values.

## Technology stack

- Python
- Streamlit
- pandas
- NumPy
- Matplotlib
- openpyxl

## Run locally

### Prerequisites

- Python installed on your computer
- Git (optional, for cloning the repository)

### 1. Clone the repository

```bash
git clone https://github.com/gomolemoclifford52-tech/QDFS-BPC-Demand-Forecasting.git
cd QDFS-BPC-Demand-Forecasting
```

Alternatively, download the repository ZIP from GitHub and extract it.

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Start the application

```bash
streamlit run app.py
```

Streamlit will print a local address, typically `http://localhost:8501`.

## Repository structure

```text
QDFS-BPC-Demand-Forecasting/
├── app.py
├── forecasting.py
├── requirements.txt
├── README.md
├── .gitignore
└── screenshots/
    ├── dashboard.png
    ├── forecast-results.png
    ├── accuracy-analysis.png
    └── parameter-testing.png
```

The `screenshots/` images are presentation assets. Add them to the repository to display the screenshots in this README.

## Interpreting forecast ranges

Where displayed, the application may show a simple range calculated as:

\[
\text{Forecast} \pm MAD
\]

This is an **error-based range**, not a statistical confidence interval or prediction interval.

## Limitations

- Electricity distribution is used as a proxy for demand and may not represent unconstrained demand when supply is restricted.
- The available dataset is relatively short and quarterly.
- Moving Average and single-parameter Exponential Smoothing are comparatively simple models.
- Historical accuracy measures do not guarantee future forecasting performance.
- Results depend on the selected parameters and evaluation period.
- Minor differences from figures in the written report may arise from rounding or implementation details.

## Future improvements

- Extend the dataset as more observations become available.
- Evaluate seasonal forecasting methods.
- Compare additional forecasting models.
- Use a defined validation procedure for parameter selection.
- Incorporate explanatory variables where reliable data is available.

## Academic context

This application supports the project:

**“Quantitative Demand Forecasting for Operational Efficiency: A Comparative Study of Moving Average and Exponential Smoothing at Botswana Power Corporation.”**

Refer to the project report for the study's full background, data sources, assumptions, methodology, and reported findings.

---

<div align="center">

Developed as an academic forecasting project using Python and Streamlit.

</div>
