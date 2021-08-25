"""
===============================================================================
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
* * * * * *                                                         * * * * * *
* * * * * *                                                         * * * * * *
* * * * * *           ad88  88                                      * * * * * *
* * * * * *          d8"    88                                      * * * * * *
* * * * * *          88     88                                      * * * * * *
* * * * * *        MM88MMM  88  88       88   8b,     ,d8           * * * * * *
* * * * * *          88     88  88       88    `Y8, ,8P'            * * * * * *
* * * * * *          88     88  88       88      )888(              * * * * * *
* * * * * *          88     88  "8a,   ,a88    ,d8" "8b,            * * * * * *
* * * * * *          88     88   `"YbbdP'Y8   8P'     `Y8           * * * * * *
* * * * * *                                                         * * * * * *
* * * * * *                                                         * * * * * *
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
* * * * * *                                                         * * * * * *
* * * * * *  FINS3645 Python Project | Option #1: Asset Management  * * * * * *
* * * * * *  By: Georgia Herron | z5060047 | 15 Aug 2021 | T2 UNSW  * * * * * *
* * * * * *                                                         * * * * * *
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

                            PortfolioAnalysis.py

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

============================ PRODUCT OVERVIEW =================================

PRODUCT SUMMARY:

Flux is an automated investment advice tool that uses machine learning (ML) to
generate portfolio recommendations for investors. Its recommendations are
based on a broad spectrum of market and sentiment indicators, news and
heterogeneous data streams. It can provide customers with valuable, data-based
insights, with the main feature of portfolio optimisation, based on Modern
Portfolio Theory. Flux aims to provide customers with valuable data-based
insights, that help them make more informed investment decisions, minimise
risk and maximise returns.

CODE SEQUENCE BREAKDOWN:

• Station #1: Extract, Transform, Load
• Station #2: Feature Engineering
• Station #3: Model Design
• Station #4: Implementation
"""
# ============================  IMPORT LIBRARIES  ============================

# Import relevant libraries
import os                           # interacting with the operating system
import numpy as np                  # array mathematical operations
import pandas as pd                 # complex data processing
import plotly                       # web-based data visualisation
import plotly.express as px
import plotly.graph_objects as go
import scipy.optimize as sco        # min/max solver
import scipy.interpolate as sci     # interpolation
from SentimentAnalysis import adjustEquitites
# my "sentimentAnalysis.py" code to equity adjustments from news sentiment

# ==============================  DEFINE CONSTANTS  ==========================

# Define financial input variables
returnTan = 0
sdTan = 0
maxTol = 5
riskFree = 0.002591
# Note: Risk-free rate from 1-year bond of Australian Government (2020)

# Define +-5% limit variables for NLP adjustments
LOWER = -0.05
UPPER = 0.05

# Define "Portfolio" class
class Portfolio:
    # init method (or constructor)
    def __init__(self):
        """
        ----------------------------------------------------------------------
        __init__() (built-in | init method): class constructor
        ----------------------------------------------------------------------
        • temporarily stores x & y paramaters in stacked instance variables.
        • discards variables when init method is no longer in scope.
        • init method (__init__) is called when instance created in class.
        • allows class to initialise attributes defined within the class.
        ----------------------------------------------------------------------
        Arg: self (built-in | self parameter): class instance
        ----------------------------------------------------------------------
        • when the class constructor (_init__) is called, a new class object
          is created & returned, self, which represents instance of the class.
        ----------------------------------------------------------------------
        Returns: (all of the instances below)
        """
        # Initialise Portfolio class instance variables
        self.assets = self.setAssets()
        self.rets = {}
        self.tck = {}
        self.useNLP = 1
        self.riskTol = 3
        self.returnsAdjustments = []

    # Set risk tolerance
    def setRiskTol(self, newTol):
        """
        Arg: self (instance)
        Arg: newTol ([type]): [description]
        Returns: self.riskTol = newTol
        """
        # !!! line below was in part above, but was this a mistake?
        self.riskTol = newTol

    def setNLP(self, NLP):
        """
        Arg: NLP [int] => 1 (apply NLP in portfolio recommendation)
                       => 0 (do not apply NLP in portfolio recommendation)
        """
        # Set useNLP to NLP
        self.useNLP = NLP

# STATION 1: EXTRACT TRANSFORM AND LOAD DATA
    def setAssets(self):
        """
        Arg: self
        Returns: reducedDf (cleansed DataFrame with select, relevant info)
        """
        # Load and convert (pre-cleaned) CSV data into Pandas DataFrame
        # Define the cleansed dataset as 'df'
        df = pd.read_csv('ASX200top10.csv', header=0)
        # Note: header=0 reads first row (index 0) as header (column names)
        # Rename date column in df
        df.rename(columns={'Unnamed: 0_level_0':'Date'}, inplace=True)
        # Returns: df (cleansed Pandas DataFrame)
        """
        Create new Pandas DataFrame called 'allStocks' with
        only the last stock price and labels for the stocks.
        """
        allStocks = set(df.columns.get_level_values(0))
        # Remove 'Date'
        allStocks.remove('Date')
        # Remove index as we can only buy it through ETFs
        allStocks.remove('AS51 Index')
        reducedDf = pd.DataFrame()

        for stock in allStocks:
            #print(df[stock]["PX_LAST"])
            #! Check if PX_LAST is correct. Use adjusted returns in other one.
            reducedDf[stock]=df[stock]["PX_LAST"]
        # Rename headers to only be ASX tickers
        reducedDf.rename(columns=lambda x: x[0:3], inplace=True)
        # Set the index of the assets df to be the date
        reducedDf.set_index(df['Date']['Dates'], inplace=True)
        # Order columns alphabetically
        reducedDf = reducedDf.reindex(sorted(reducedDf.columns), axis=1)
        return reducedDf

    def getAssetNames(self):
        """
        Get column names.
        Arg: self (instance)
        Returns: self.assets.columns (list of names)
        """
        return self.assets.columns

    def generateRandomPortfolios(self, simulations):
        """
        Generates a number of possible holdings.
        Arg: simulations (int - number of simulated portfolios to generate)
        Returns:
        - prets (array): Portfolio returns
        - pvol (array): Portfolio vol
        - psharpe (array): Portfolio sharpe
        - pweights (array): Portfolio weights to achieve above results
        """
        # Apply NLP
        self.applyAdjustments()
        # Dind & normalise returns
        rets = np.log(self.assets / self.assets.shift(1))
        numAssets = len(self.assets.columns)
        prets = []
        pvol = []
        psharpe = []
        pweights = []

        # Derive porfolio weights and obtain historical return & vol for
        # Combinations specified
        for count in range(simulations):
            # Generate uniformally distributed array
            weights = np.random.random(numAssets)
            weights /= np.sum(weights)

            # Annualise returns & apply NLP adjustment
            portfolioReturns, portfolioStd = self.annualisedPortfolioReturns(weights,rets)
            prets.append(portfolioReturns)
            pvol.append(portfolioStd)
            psharpe.append((portfolioReturns - riskFree)/portfolioStd)
            pweights.append(weights)

        return prets, pvol, psharpe, pweights

    def showRandomPortfolio(self, simulations):
        """ generates optimal weightings & returns graph of random portfolios.

        args:
        - simulations (integer): number of simulated portfolios to generate

        returns:
        - figure: plotly graph of random portfolios
        """
        returns, volatility, sharpe, weights = self.generateRandomPortfolios(simulations)

        # Combine results into one dataframe
        returns = np.array(returns)
        volatility = np.array(volatility)
        sharpe = np.array(sharpe)
        randomPortfolio = pd.DataFrame(weights, columns=self.getAssetNames())
        randomPortfolio['returns'] = returns
        randomPortfolio['volatility'] = volatility
        randomPortfolio['sharpe'] = sharpe

        # Label weights
        def labelPoints(row):
            res = ''
            for index, value in row.items():
                res = res + f"{index}: {value:.2%} <br />"
            return(res)

        randomPortfolio['combined'] = randomPortfolio[randomPortfolio.columns[0:10]].apply(lambda x: labelPoints(x), axis=1)

        ## showing individual points
        an_rets = np.log(self.assets / self.assets.shift(1)).mean() * 252

        maxSharpeIndex = randomPortfolio['sharpe'].idxmax()
        minVolatilityIndex = randomPortfolio['volatility'].idxmin()

        # client weighting adjustment
        portfolioVolRange = randomPortfolio['volatility'].max() - randomPortfolio['volatility'].min()

        # divide range by number of 'buckets', 0.2 as 1/5
        clientMaxRisk = self.riskTolerance/maxRiskTol * portfolioVolRange + randomPortfolio['volatility'].min()
        clientMinRisk = clientMaxRisk - 1/maxRiskTol * portfolioVolRange
        # print("Acceptable volatility range for this client")
        # print(clientMinRisk)
        # print(clientMaxRisk)

        # divide vol into 5 categories
        # reduce Portfolio to only include valid volatiltiy range
        reducedPortfolio = randomPortfolio[randomPortfolio['volatility'].between(clientMinRisk, clientMaxRisk)]
        # find optimal sharpe return for acceptable vol range of the client.
        reducedSharpe = reducedPortfolio['sharpe'].idxmax()

        # set all optimal weighting info
        clientOptimalMessage = "<b> Best For your Risk Tolerence Achieves: </b> <br />"+f"{reducedPortfolio['returns'][reducedSharpe]:.2%} Return <br />"+f"{reducedPortfolio['volatility'][reducedSharpe]:.2%} Volatility <br />"+ "<b> Weighting Required: </b> <br />"+reducedPortfolio['combined'][reducedSharpe]
        minVarianceMessage = "<b> Least Volatility Achieves: </b> <br />"+f"{randomPortfolio['returns'][minVolatilityIndex]:.2%} Return <br />"+f"{randomPortfolio['volatility'][minVolatilityIndex]:.2%} Volatility <br />"+" <b> Weighting Required: </b> <br />"+randomPortfolio['combined'][minVolatilityIndex]
        optimalSharpeMessage = "<b> Best Sharpe Ratio Achieves: </b> <br />"+f"{randomPortfolio['returns'][maxSharpeIndex]:.2%} Return <br />"+f"{randomPortfolio['volatility'][maxSharpeIndex]:.2%} Volatility <br />"+" <b> Weighting Required: </b> <br />"+randomPortfolio['combined'][maxSharpeIndex]
        self.optimalSharpeMessage = optimalSharpeMessage
        self.minVarianceMessage = minVarianceMessage
        self.clientOptimalMessage = clientOptimalMessage

        # Scatter plot
        figure = go.Figure(data=go.Scatter(
            x = randomPortfolio['volatility'],
            y = randomPortfolio['returns'],
            text = randomPortfolio['combined'] ,
            hovertemplate="Return: %{y}<br />Volatility: %{x}<br />Weightings: <br />%{text}<extra></extra>",
            mode='markers',
            marker=dict(
                size=10,
                color=randomPortfolio['sharpe'], #set color equal to a variable
                colorscale='Viridis', # one of plotly colorscales
                showscale=True,
                colorbar_title="Sharpe Ratio")),
            layout=dict(
                title= "Generated Portfolios",
                xaxis_title="Expected Volatility",
                yaxis_title="Expected Return"))
        return figure

# ================== MODERN PORTFOLIO THEORY HELPER FUNCTIONS ================

    def annualisedPortfolioReturns(self, weights, rets):
        """
        Arg: weights (DataFrame): Numpy array of weights to hold in a stock
        Arg: rets (DataFrame): DataFrame containing % daily returns for each stock

        Returns: returns (returns of annualised portfolio)
        Returns: std (standard deviation of annualised portfolio)
        """
        newRets=np.array([])

        # Adjust equity returns based on NLP, before optimising the portfolio
        if (self.useNLP == 1):
            # Adjust equity returns using NLP adjustment
            for idx, equity in enumerate(self.returnsAdjustments):
                newRets = np.append(newRets, rets.mean()[idx]
                                    + self.returnsAdjustments[idx]
                                    * rets.mean()[idx])
        else: 
        newRets = rets.mean()
        print("Unadjusted Returns", rets.mean())
        print("Adjusted Returns", newRets)

        # Final return & standard deviation of the Portfolio
        returns = np.sum(newRets * weights) * 252
        std = np.sqrt(np.dot(weights.T,np.dot(rets.cov() * 252, weights)))
        return returns, std


    def applyAdjustments(self):
        # Determine news sentiment adjustments
        equityAdjustments = adjustEquitites(newsLocation)

        # Sort equities to match adjustments
        equityAdjustments = equityAdjustments.reindex(sorted(equityAdjustments.columns), axis=1)
        limitedAdjustments = []

        # 5% limit for equity adjustments
        for equity in equityAdjustments:
            limitedAdjustments.append(self.restrict(equityAdjustments[equity][0],LOWER,UPPER))
        self.returnsAdjustments = limitedAdjustments

        # print("Adjustments are")
        # print(self.returnsAdjustments)
        return 1


    def restrict(self, num, minNum, maxNum):
        """ given a number, limit it to be within min and max

        args:
            n ([type]): [description]
            minn ([type]): [description]
            maxn ([type]): [description]

        returns:
            [type]: [description]
        """
        return max(min(maxNum, num), minNum)

    # Note: helper functions below were sourceed from Juraj Hric FINS3645 UNSW T2 2021
    def statistics(self, weights):
        weights = np.array(weights)
        pret = np.sum(self.rets.mean() * weights) * 252
        pstd = np.sqrt(np.dot(weights.T, np.dot(self.rets.cov() * 252, weights)))
        return np.array([pret, pstd, pret / pstd])

    def min_func_sharpe(self, weights):
        return - self.statistics(weights)[2]

    def min_func_variance(self, weights):
        return self.statistics(weights)[1] ** 2

    def min_func_port(self, weights):
        return self.statistics(weights)[1]

    def f(self, x):
        # efficient frontier function (splines approximation)
        return sci.splev(x, tck, der=0)
    def df(self, x):
        # first derivative of efficient frontier function
        return sci.splev(x, tck, der=1)

    def equations(self, p, rf=riskFree):
        eq1 = rf - p[0]
        eq2 = rf + p[1] * p[2] - f(p[2])
        eq3 = p[1] - df(p[2])
        return eq1, eq2, eq3

    def read_client_positions(self):
        df = pd.read_csv('clientLocation.csv', header=0)
        return df
