# Dissertation Prototype

This repository contains the prototype developed for my undergraduate dissertation project on Instagram hashtag-based engagement prediction in the Maltese context.

## Project Overview

The prototype investigates how hashtag-related features can be used to analyse and predict Instagram engagement. It focuses on features such as hashtag quantity, hashtag category, hashtag length, Maltese hashtag ratio, hashtag combinations, caption length, emoji use, sentiment polarity, and engagement rate.

The prototype includes:

* Instagram data collection
* Hashtag extraction
* Hashtag classification using Uses and Gratifications Theory
* Feature engineering
* Engagement rate calculation
* Exploratory data analysis
* Machine learning modelling
* Model evaluation
* Hypothesis testing and hashtag analysis

## Files Included

### data_collection.py

This script was used to collect Instagram post data using the Meta Instagram Graph API. It collects post captions, like counts, comment counts, timestamps, and follower counts for selected public accounts.

Sensitive information such as access tokens, account IDs, API credentials, and account lists are not included in this repository.

### Prototype.ipynb

This notebook contains the main prototype implementation. It presents the full analysis workflow used in the dissertation, including dataset loading, hashtag extraction, UGT-based hashtag classification, feature engineering, engagement rate calculation, exploratory analysis, model training, model evaluation, visualisation, and final result summaries.

## Main Features Analysed

The prototype analyses the following features:

* Total number of hashtags per post
* Average hashtag length
* Maltese hashtag ratio
* Informational hashtag count
* Entertaining hashtag count
* Relational hashtag count
* Remunerative hashtag count
* Hashtag combinations
* Caption length
* Emoji count
* Sentiment polarity
* Engagement rate

## Machine Learning Models Used

The prototype compares the following machine learning models:

* Logistic Regression
* Random Forest
* XGBoost

The models are used to classify Instagram posts into Low engagement and High engagement groups based on engagement rate.

## Notes

The raw dataset, API credentials, access tokens, account IDs, and account lists are not included in this repository for privacy, ethical, and security reasons. The notebook shows the processing, analysis, modelling, evaluation, visualisation, and hypothesis testing steps used in the dissertation prototype.

This repository was submitted as part of the dissertation prototype requirement.
