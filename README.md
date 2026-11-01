# Stock Market Analysis Dashboard

## Overview

The " Stock Market Analysis Dashboard " is a Python-based data analysis project that processes stock market data, evaluates stock performance,
compares sector performance, and visualises market trends through an interactive dashboard.

The project follows a data processing pipeline that extracts stock information from YAML files, converts it into CSV datasets,
performs stock and sector analysis, and presents the results through a Streamlit dashboard.

## Key Features

### 1. Stock Analysis
- Select individual stocks using their ticker symbols.
- View starting and ending stock prices.
- Calculate overall stock returns.
- Visualise historical closing prices.
- Display recent stock records.

### 2. Sector Analysis
- Group stocks based on their sectors.
- Calculate average daily returns for each sector.
- Compare sector performance using tables and bar charts.
- Analyse sector volatility.

### 3. Market Summary
- Display average stock prices.
- Calculate average trading volume.
- Compare stocks with positive and negative period returns.
- Identify the top 10 gainers.

### 4. Correlation Analysis
- Calculate correlations between stock closing prices.
- Generate a correlation matrix.
- Visualise relationships between different stocks using a heatmap.

### 5. Raw Data
- Display the processed stock dataset.
- Explore the available stock records.
- Download the dataset as a CSV file.

### 6. Additional Analysis
- Identify the top 10 gainers and losers.
- Calculate stock volatility using standard deviation.
- Generate cumulative return charts.
- Perform monthly stock performance comparisons.
- Export individual stock datasets.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Pandas | Data cleaning, manipulation, and analysis |
| Streamlit | Interactive dashboard development |
| Matplotlib | Data visualisation |
| PyYAML | Extracting data from YAML files |
| Glob | Searching and retrieving YAML files |
| OS | File and directory management |
| CSV | Storing extracted and processed datasets |

## Project Architecture

The project follows an ETL (Extract, Transform, Load) workflow.


              YAML SOURCE FILES
                     |
                     v
                 extract.py
                     |
                     v
                all_stocks.csv
                     |
                     v
              analysis.py
                     |
          +----------+-----------+
          |          |           |
          v          v           v
      Stock       Sector      Volatility
     Returns     Analysis      Analysis
          |          |           |
          +----------+-----------+
                     |
                     v
                final_data.csv
                     |
                     v
                  app.py
                     |
                     v


## Project Structure

The following structure is based on the files shared:


Stock-Market-Analysis/
│
├── app.py
│
├── scripts/
│   ├── extract.py
│   ├── analysis.py
│   └── chart.py
│
├── CSV/
│   ├── charts/
│   ├── tickers/
│   ├── .gitignore
│   ├── Sector_data.csv
│   ├── all_stocks.csv
│   ├── final_data.csv
│   └── sector_summary.csv
│
└── README.md


Additional chart images are also present in the CSV directory.

## Data Processing Workflow

### Step 1: Data Extraction

The `extract.py` script:
- Searches for YAML files in the source data directory.
- Reads the YAML records using PyYAML.
- Combines the extracted records into a Pandas DataFrame.
- Exports the consolidated dataset as `all_stocks.csv`.

### Step 2: Data Cleaning and Analysis

The `analysis.py` script:
- Loads stock price and sector datasets.
- Cleans column names.
- Extracts ticker symbols and merges sector information.
- Converts dates into datetime format.
- Sorts stock records by ticker and date.
- Calculates daily returns and period returns.
- Calculates stock and sector volatility.
- Identifies top gainers and losers.
- Generates charts and exports processed datasets.

### Step 3: Additional Analysis

The `chart.py` script performs stock-level and sector-level analysis, including:
- Daily stock returns.
- Period returns.
- Stock volatility.
- Sector average returns.
- Sector volatility.

It also exports the combined dataset, sector summary, and individual ticker datasets.

### Step 4: Interactive Dashboard

The `app.py` script loads `final_data.csv` and provides an interactive interface for exploring stock performance, sector analysis, market summaries, 
correlations, and raw datasets.

## Financial Calculations

### Daily Return

Measures the percentage change in a stock's closing price compared with its previous recorded closing price.

```text
Daily Return = (Current Close - Previous Close) / Previous Close
```

Python implementation:

```python
df.groupby('Ticker')['close'].pct_change()
```

### Period Return

Measures the percentage change between the first and last recorded closing prices in the selected dataset period.

```text
Period Return (%) = ((Last Price - First Price) / First Price) × 100
```

### Volatility

Measures fluctuations in stock returns using standard deviation.

```python
df.groupby('Ticker')['daily_return'].std()
```

### Correlation

Measures how the closing prices of two stocks move in relation to each other.

The correlation coefficient ranges from -1 to +1:

- +1: Perfect positive correlation.
- 0: No linear correlation.
- -1: Perfect negative correlation.

## Installation and Setup

### Prerequisites

- Python 3.9 or later
- pip
- Git

### 1. Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
```

### 2. Navigate to the Project Directory

```bash
cd Stock-Market-Analysis
```

### 3. Install Dependencies

```bash
pip install pandas matplotlib streamlit pyyaml
```

### 4. Run the Data Extraction Script

Run this from the project root directory:

```bash
python scripts/extract.py
```

Ensure the YAML source files are available in the directory expected by the extraction script.

### 5. Run the Analysis Pipeline

```bash
python scripts/analysis.py
```

This generates the processed dataset and analysis outputs.

### 6. Launch the Dashboard

```bash
streamlit run app.py
```

The dashboard will open in your browser.

## Potential Future Enhancements

- Integrate live stock market data through a financial market API.
- Add date-range filters for historical stock analysis.
- Include moving averages such as SMA and EMA.
- Add RSI and MACD technical indicators.
- Introduce interactive charts using Plotly.
- Add sector-wise stock comparison.
- Improve error handling and data validation.
- Optimise the correlation analysis for larger datasets.

## Learning Outcomes

This project demonstrates practical experience with:

- Data extraction from YAML files.
- Data cleaning and preprocessing.
- ETL pipeline development.
- Data manipulation using Pandas.
- Grouping and aggregation.
- Time-series data analysis.
- Financial return and volatility calculations.
- Correlation analysis.
- Data visualisation.
- Interactive dashboard development using Streamlit.
- CSV data management.

## Author

**Mohamed Ameen**

Integrated M.Tech – Computer Science and Engineering  
Vellore Institute of Technology

GitHub: https://github.com/72646
