# Gain-Loss Asymmetry and Bimodal Structures in Multiscale Financial Returns

📄 **Current Status:** Author's Original Manuscript. Currently under peer review at the journal *Quantitative Finance* (Taylor & Francis).

---

## 📌 Executive Summary
This study presents a multi-scale statistical analysis of financial market dynamics by examining "Trend Returns"
(TReturns)—logarithmic returns derived from uninterrupted directional price movements—across four major
global indices (DJIA, Nasdaq, Nikkei, and IPC). By contrasting empirical data against a Monte Carlo Geomet-
ric Brownian Motion (GBM) null model, we rigorously distinguish between mechanical artifacts and genuine
structural anomalies. We document Emergent Bimodality: while daily returns (d = 1) exhibit unimodal noise,
trends persisting for d ≥ 2 structurally separate into distinct positive and negative modes. While the GBM
confirms that this separation is largely a natural topology of trend persistence, empirical data reveal a distinct
divergence at longer durations (d > 6), where the negative mode extinguishes, transitioning back to a positively
shifted unimodality—a behavior absent in the persistent bimodality of the random walk. Furthermore, we
uncovered a fundamental Dual Asymmetry. While the Asymmetry of Frequency (preference for long uptrends)
is partially consistent with positive drift, the Asymmetry of Character—quantified via Volatility Ratios (< 1)
and the Wasserstein Distance—reveals that downtrends are structurally more volatile ("violent") and possess
heavier tails than uptrends, a feature that the Gaussian control fundamentally fails to reproduce. At the macro
level, this manifests as a universal negative skewness. These findings suggest that standard Gaussian models
are structurally blind to the specific mechanics of market corrections, leading to systematic underestimation of
tail risk

---

## 🛠️ Repository Architecture & Reproducibility

This repository contains the complete, production-grade source code and environments required to replicate every empirical finding, statistical test, and figure presented in the paper.

* 📂 **`libs/`**: Core modules and implementations of the multi-scale trend identification algorithms, calculation of volatility ratios, and non-parametric estimation metrics.
* 📂 **`notebooks/`**: End-to-end research pipelines containing:
  * Financial data retrieval and data cleaning (DJIA, Nasdaq, Nikkei, IPC).
  * **Monte Carlo Null Model:** Full Geometric Brownian Motion (GBM) simulation framework used as a structural control group.
  * **Statistical Core:** Implementations of Hartigan's Dip Test, Welch's t-test, Mann-Whitney U-test, and 10,000-iteration Permutation tests for the $W_1$ Wasserstein Distance.
  * **Uncertainty Quantification:** Non-parametric bootstrapping pipelines ($N=10,000$) for statistical error estimation.
* 📄 **`Articulo_GainLossTAssimetry_BimodalTrendsDist.pdf`**: Full text manuscript draft.

---

## 🚀 Key Theoretical & Practical Insights for Industry
1. **Risk Management Beyond Gaussian Models:** Standard parametric risk metrics (like standard VaR) systematically underestimate tail risk by ignoring the *Asymmetry of Character* quantified here.
2. **observable Regime Priors:** Rather than blindly inferring latent states via classical Hidden Markov Models, our multi-scale filtering provides directly observable bimodal distributions to calibrate asymmetrical emission states (e.g., Skewed Student-t).
3. **Algorithmic Trading Thresholds:** The structural boundary between unimodal noise ($d=1$) and bimodal trends ($d \ge 2$) provides an empirical, data-driven framework to optimize trend-following filters and minimize whipsaw losses.



# Quantitative Finance & Time Series Analysis

This repository houses a collection of Python modules and Jupyter notebooks dedicated to quantitative finance, time series analysis, and market dynamics. It includes tools for financial data manipulation, statistical analysis of returns and trends, market breadth indicators, Principal Component Analysis, and advanced time series modeling.

## Table of Contents

1.  [QuantLib: Quantitative Finance Utilities](#1-quantlib-quantitative-finance-utilities)
2.  [Multi-Scale Trend Returns Analysis](#2-multi-scale-trend-returns-analysis)
3.  [Principal Component Analysis & Random Matrix Theory](#3-principal-component-analysis--random-matrix-theory)
4.  [Market Dynamics & Power Law Analysis](#4-market-dynamics--power-law-analysis)
5.  [Market Breadth Trading Strategy](#5-market-breadth-trading-strategy)
6.  [Financial Data Quantitative Analysis & Stylized Facts](#6-financial-data-quantitative-analysis--stylized-facts)
7.  [General Dependencies](#7-general-dependencies)

---

### 1. QuantLib: Quantitative Finance Utilities

*   **File:** `QuantLib.py`
*   **Description:** This Python module serves as a foundational library for quantitative financial analysis. It provides a comprehensive set of functions for data acquisition, preprocessing, transformation, and statistical visualization of financial time series.
*   **Key Features:**
    *   **Data Fetching:** Functions to download daily and intraday historical stock data from Yahoo Finance (`yf.download`).
    *   **Returns & Trends:** Calculation of logarithmic returns, conversion between log returns and prices, and generation of multi-scale "trends" (price runs).
    *   **Data Splitting:** Separation of positive and negative returns/trend returns for independent analysis.
    *   **Visualization:** Tools for plotting histograms, CDFs (Cumulative Distribution Functions), PDFs (Probability Density Functions), and custom charts for trend durations.
    *   **Distribution Fitting:** Adjustment of empirical data to theoretical distributions (e.g., Exponential, Pareto) using Maximum Likelihood Estimation via `scipy.stats`.
    *   **Normalization:** Standard (Z-score) and Min-Max scaling of data.
    *   **Resampling:** Functions to resample data by trading minutes, trading days, or calendar days.
*   **Dependencies:** `pandas`, `matplotlib`, `yfinance`, `numpy`, `seaborn`, `scipy.stats`.

### 2. Multi-Scale Trend Returns Analysis

*   **File:** `TReturns_MultiScaleAnalysis.ipynb`
*   **Description:** This Jupyter notebook applies the utilities from `QuantLib.py` to perform a detailed multi-scale analysis of financial indices like Dow Jones (`^DJI`), Nasdaq (`^IXIC`), Nikkei (`^N225`), and IPC (`^MXX`). It investigates the distributions of multi-scale trend returns and their statistical properties.
*   **Key Concepts:**
    *   **Trend Generation:** Identifying significant price trends (up/down runs) in historical data.
    *   **Trend Durations:** Analysis of the statistical distribution of trend durations, including fitting to exponential distributions.
    *   **Bimodality:** Visualization and analysis of the bimodal nature of trend returns using KDE (Kernel Density Estimation).
    *   **Symmetry Tests:** Application of Welch's t-test and Mann-Whitney U-test to compare the distributions of positive and absolute negative trend returns across different trend lags, assessing market asymmetry.
    *   **Monte Carlo Simulations:** Usage of Geometric Brownian Motion (GBM) to generate synthetic price paths and analyze trend statistics in a controlled environment.
    *   **Statistical Ratios:** Calculation and visualization of ratios between statistics of positive and absolute negative returns, with error propagation.
    *   **Hartigan's Dip Test:** A statistical test for unimodality vs. multimodality (bimodality) in distributions.
*   **Dependencies:** `QuantLib.py`, `pandas`, `matplotlib`, `yfinance`, `numpy`, `seaborn`, `scipy.stats`, `diptest`, `IPython.display`.

### 3. Principal Component Analysis & Random Matrix Theory

*   **File:** `RM_PCA.ipynb`
*   **Description:** This notebook demonstrates the application of Principal Component Analysis (PCA) and concepts from Random Matrix Theory (RMT) to a correlation matrix of stock returns, specifically for companies in the IPC index. It explores dimensionality reduction and the identification of dominant market factors.
*   **Key Concepts:**
    *   **Data Preprocessing:** Handling missing values, calculating logarithmic returns, and standardizing returns.
    *   **Correlation Matrix:** Construction and visualization of the correlation matrix of stock returns.
    *   **Eigenvalue Decomposition:** Calculation of eigenvalues and eigenvectors of the correlation matrix.
    *   **Scree Plot:** Visualization of eigenvalues to determine the number of significant principal components.
    *   **Explained Variance:** Analysis of individual and cumulative explained variance by principal components.
    *   **PCA with Scikit-learn:** Application of `sklearn.decomposition.PCA` to project data onto principal components.
    *   **Loadings:** Interpretation of component loadings to understand the contribution of individual stocks to each principal component.
    *   **IPC Index Comparison:** Comparison of principal components with the actual IPC index returns.
*   **Dependencies:** `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `QuantLib.py` (for normalization functions).

### 4. Market Dynamics & Power Law Analysis

*   **File:** `Market_Dynamics.ipynb`
*   **Description:** This notebook delves into advanced market dynamics, primarily focusing on Bitcoin (`BTC-USD`) price behavior. It applies power-law fitting to long-term price trends and introduces concepts akin to "velocity" and "acceleration" in financial time series.
*   **Key Concepts:**
    *   **Power Law Fitting:** Fitting a power-law curve to historical Bitcoin prices on a log-log scale.
    *   **Trend Channels:** Identifying and fitting power-law trends to local price peaks and troughs, creating a dynamic channel.
    *   **Price Projections:** Extending power-law fits to project future price channels and potential intersection points.
    *   **Detrended Analysis:** Analyzing price cycles by removing the dominant power-law trend.
    *   **Market Velocity & Acceleration:** Deriving and visualizing first and second-order differences of logarithmic returns, interpreted as financial velocity and acceleration.
    *   **Market Energy (MEBI):** An exploratory concept for market energy derived from price velocity and acceleration.
*   **Dependencies:** `pandas`, `numpy`, `yfinance`, `matplotlib`, `scipy.signal`, `QuantLib.py` (for normalization).

### 5. Market Breadth Trading Strategy

*   **File:** `MarketBreadth2.ipynb`
*   **Description:** This notebook explores market breadth indicators and implements a simple trading strategy based on the "Daily Positive Percent" indicator for the IPC index. It focuses on using the percentage of advancing stocks to generate buy/sell signals.
*   **Key Concepts:**
    *   **Market Breadth Indicators:** Calculation of "Daily Total Returns" and "Daily Positive Percent" from a basket of stocks.
    *   **Visualization:** Plotting market breadth indicators and their distributions.
    *   **Strategy Simulation:** Implementation of a rule-based trading strategy using buy and sell thresholds on the "Daily Positive Percent" indicator, with optional stop-loss.
    *   **Performance Evaluation:** Calculation of final balance, trading returns, and comparison with a buy-and-hold strategy.
    *   **Threshold Optimization:** A framework for optimizing buy/sell thresholds to maximize trading returns.
    *   **Trade Visualization:** Plotting entry and exit points on the price chart and analyzing balance evolution.
*   **Dependencies:** `pandas`, `numpy`, `matplotlib`, `seaborn`, `QuantLib.py` (for normalization).

### 6. Financial Data Quantitative Analysis & Stylized Facts

*   **File:** `Cuantitative_Analysis_TS.ipynb`
*   **Description:** This notebook covers fundamental concepts in the quantitative analysis of financial time series. It introduces common stylized facts observed in financial markets and methods to analyze long-range dependencies.
*   **Key Concepts:**
    *   **Logarithmic Returns:** Calculation and visualization of log returns.
    *   **Descriptive Statistics:** Calculation of mean, standard deviation, skewness, and kurtosis of returns.
    *   **Stylized Facts:** Verification and visualization of characteristic properties of financial returns, such as:
        *   **Fat Tails:** Leptokurtic distributions (high kurtosis).
        *   **Volatility Clustering:** Periods of high volatility tend to be followed by periods of high volatility.
        *   **Absence of Linear Autocorrelations:** Returns themselves show little autocorrelation, but their squares (volatility) do.
    *   **Autocorrelation Function (ACF) & Partial Autocorrelation Function (PACF):** Analysis of linear dependencies in time series.
    *   **Detrended Fluctuation Analysis (DFA):** A method to quantify long-range correlations in non-stationary time series and estimate the Hurst exponent ($\alpha$).
    *   **Fractional Brownian Motion (fBM):** Generation of synthetic fBM series with a specified Hurst exponent to simulate long-range dependent processes.
    *   **Stationary Time Series:** Generation and analysis of AR(1) processes as examples of stationary series.
*   **Dependencies:** `pandas`, `numpy`, `matplotlib`, `yfinance`, `seaborn`, `statsmodels`, `scipy.stats`, `fbm`, `diptest`.

---

### 7. General Dependencies

Most projects in this repository rely on the following Python libraries. It is recommended to use a virtual environment to manage these dependencies.

*   `numpy`
*   `pandas`
*   `scikit-learn`
*   `torch`
*   `matplotlib`
*   `seaborn`
*   `yfinance`
*   `scipy`
*   `statsmodels`
*   `tqdm`
*   `networkx`
*   `fbm`
*   `diptest`
*   `ucimlrepo` (for specific datasets)
