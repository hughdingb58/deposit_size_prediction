# Predicting bank non-maturity deposit size across varying economic conditions

This project aims to predict bank deposit sizes using macro-economic indicators and bank-level data.

# Project description

In the banking industry, effective liquidity management and strategic decision-making requires accurate deposit prediction. Non-maturity deposits form a significant portion of a bank's liabilities and are subject to various factors such as interest rates, economic conditions, and customer behavior. Banks can use data science techniques to gain deeper insights into the drivers of deposits and improve their forecasting accuracy.

Our goal is to forecast US bank non-maturity deposit size based on key macroeconomic indicators, including

- interest rates,
- GDP growth rate as a proxy for consumer confidence (economic expansion vs recession), and
- consumer behaviour indicators, e.g. personal savings rates and household debt-to-income ratio.

We would like to learn:

1. To what degree do these indicators affect non-maturity bank deposits?
2. Are certain types of indicators clearly more prominent in our model than others?

We use total deposits and the ratio of high maturity debt securities to estimate the size of non-maturity deposits. According to [FDIC literature](https://www.fdic.gov/analysis/cfr/bank-research-conference/annual-20th/papers/xiang-paper.pdf), non-maturity deposits constitute the majority of bank balance sheets.

# Data pipeline

You will need to have an installation of Jupyter and Python >= 3.

Analysis is done across two Jupyter notebooks:

- **1_preparation_exploration** for data gathering, preparation, and exploration.
  - For data gathering, the notebook runs **gather_api_data.py**, which makes API calls to FRED and the FDIC and saves the data to **fred_econ.feather** and **fdic_financials.feather**. Since the feather tables are already in the git repo, you may skip this step if attempting to replicate our analysis.
  - At the end of the notebook, the data is saved into **df_train.feather** for model training and **df_samples.feather** for robustness checks.
- **2_supervised_analysis.ipynb**, for supervised analysis and results. It reads in **df_train.feather** and **df_samples.feather** produced by the first notebook.

## FRED API key

You will need to create your [own FRED API key](https://fred.stlouisfed.org/docs/api/api_key.html).

Please create a file called **fred_api_key.txt** and enter your FRED API key in the first line. This file will be read in the Jupyter notebook.

## Required libraries

The following libraries are required:

- numpy
- pandas
- fredapi
- matplotlib
- pyarrow
- seaborn
- scikit-learn
- scipy

You can install them by navigating to this project's directory in cmd and running the following command:

```pip install -r requirements.txt```

## Data sources

- [Federal Reserve Economic Data (FRED)](https://fred.stlouisfed.org/)
	- An online, free-to-access database containing economic time series data from various national, international, public, and private sources. We download quarterly data from 1992 onwards for modeling purposes.
- [Federal Deposit Insurance Corporation (FDIC)](https://www.fdic.gov/)	
	- The FDIC provides free access to a variety of data related to banking and financial institutions in the United States. This includes information on deposits, bank statistics, financial reports, historical data on bank failures and resolutions. We download quarterly data from 1992 onwards.

# Results

We find that regression models (lasso and OLS) are not significantly less effective at predicting bank deposit size than more complex models such as random forest and gradient boosting. This means we are able to run interpretable regression models without a major downside to performance.

We find that CPI is the strongest predictor of bank deposit size in the following quarter. In addition, bank deposit sizes perform differently across different banking models (small, medium, and large banks).
