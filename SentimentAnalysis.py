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

                            SentimentAnalysis.py

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

============================== CODE OVERVIEW =================================

TODO

"""
# ===========================  IMPORT LIBRARIES  =============================

# Complex data processing
import pandas as pd
# VADER sentiment analyser
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from datetime import timedelta
# MATLAB-like framework for plots
import matplotlib.pyplot as plt

# ===========================  DEFINE CONSTANTS  =============================

# Leverage pre-trained model due to limited data
nltk.download('vader_lexicon')
defaultNewsLocation = './news_dump.json'
fileLocation = './'
# Initialise vader sentiment analyser
sentimentAnalyser = SentimentIntensityAnalyzer()

def loadData(newsLocation):
    """
    Given a *.json fiile location, loads Pandas df.
    Arg: newsLocation (string): Optional file location in json format.
    Returns: df (Pandas Dataframe)
    """
    if newsLocation == '':
        # If no location entered, provide the default
        newsLocation = defaultNewsLocation
    df = pd.read_json(newsLocation)
    # Convert date from string to datetime
    df['Date/Time'] = pd.to_datetime(df['Date/Time'])
    return df


def scoreData(df,toScore):
    """
    Scores the sentiment of the data.
    Arg: df (Pandas Dataframe, optional file location in json format).
    Arg: toScore (Series): Equities to score
    Returns: meanScores (Pandas Dataframe, of sentiment analysis results).
    """
    # Use pretrained vader model to score
    #! This is the biggest limitation of this model.
    # Ideally we would have more data to train our own model.
    scores = toScore.apply(sentimentAnalyser.polarity_scores).tolist()
    # Convert the 'scores' list of dicts into a DataFrame
    scores_df = pd.DataFrame(scores)
    # Combine score with relevant input - this is for sanity checking
    df = df.join(scores_df, rsuffix='_right')
    # Group by equity, then find the mean sentiment over all occurances.
    #! Ideally we weight more recent events.
    # Code is commented out as there are too few entries in the data given.
    """
    # This assumes that only last month contains relevent information.
    # Filter out all other info.
    mostRecentDate = df['Date/Time'].max()
    df = df[(df['Date/Time'] > (mostRecentDate - timedelta(days=30)))]
    df.to_csv(fileLocation + 'reduced_sentiment_scores.csv')
    """
    meanScores = df.groupby(['Equity']).mean()
    print('Sentiment analysis results:')
    print(meanScores)
    return meanScores

def analyseNews(newsLocation):
    """
    Given news, returns a dataframe estimating the impact of news on each stock.
    Arg: newLocation (json doc - provide filepath to json news).
    """
    # Stations 1 & 2: Extract, Transform and Load (ETL) & Feature Engineering.
    df = loadData(newsLocation)
    # Station 3 - Model Design
    meanScores = scoreData(df,df['Headline'])
    # Station 4 - Implementation
    # !!! graphSentiment(df, meanScores)
    return (meanScores)


def adjustEquitites(newsLocation):
    """
    Given location of json news file, the function returns the
    adjustments to make for each stock due to sentiment analysis.
    Arg: newsLocation (str - location of news file).
    Returns: equityWeights (DataFrame - adjustment to make for each
    stock, limited to +/-5%.
    """
    equityWeights = analyseNews(newsLocation)
    #Find compound adjustment and transpose so equities are columns.
    return equityWeights[['compound']].T
