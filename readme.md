# Predicting bank deposit size across varying economic conditions

This project aims to predict bank deposit sizes using macro-economic indicators and bank-level data.

# Project description

In today's dynamic banking environment, accurately predicting deposits is crucial for effective liquidity management and strategic decision-making. Deposits form a significant portion of a bank's liabilities and are subject to various factors such as interest rates, economic conditions, and customer behavior. By leveraging data science techniques, banks can gain deeper insights into the drivers of deposits and improve their forecasting accuracy.

Our goal is specifically to forecast US bank deposit size based on key macroeconomic indicators, including

- interest rates,
- GDP growth rate as a proxy for consumer confidence (economic expansion vs recession), and
- consumer behaviour indicators, e.g. personal savings rates and household debt-to-income ratio.

We would like to learn:

1. To what degree do these indicators affect bank deposits?
2. Are certain types of indicators clearly more prominent in our model than others?

# Running the notebook

The full analysis is done in a single Jupyter notebook for clarity and ease of use. You will need to have an installation of Jupyter and Python >= 3.

## Required libraries

- NumPy
- Pandas
- fredapi
- scikit-learn
- matplotlib
- seaborn

## Data sources

- [Federal Reserve Economic Data (FRED)](https://fred.stlouisfed.org/)
	- An online, free-to-access database containing economic time series data from various national, international, public, and private sources. We download quarterly data from 1992 onwards for modeling purposes.
- [Federal Deposit Insurance Corporation (FDIC)](https://www.fdic.gov/)	
	- The FDIC provides free access to a variety of data related to banking and financial institutions in the United States. This includes information on deposits, bank statistics, financial reports, historical data on bank failures and resolutions. We will be downloading quarterly data from 1992 onwards.

## Outline of notebook

Our notebook is structured as follows:

- Data gathering and preparation
	- FRED
	- FDIC
- Data exploration
	- FRED
	- FDIC
- Unsupervised modelling exploration
- Supervised modelling and analysis
	- Results and interpretation

# Results

## Areas of further consideration
