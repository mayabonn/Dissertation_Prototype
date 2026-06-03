# Dissertation Prototype

This repository contains the prototype developed for my dissertation project on Instagram hashtag-based engagement prediction in the Maltese context.

## Project Overview

The prototype investigates how hashtag-based features can be used to analyse and predict Instagram engagement. The project focuses on hashtag characteristics such as hashtag quantity, hashtag categories, hashtag length, language use, and hashtag combinations.

The prototype includes:

* Instagram data collection script
* Hashtag extraction
* Hashtag classification using Uses and Gratifications Theory (UGT)
* Feature engineering
* Engagement rate calculation
* Exploratory data analysis
* Machine learning modelling
* Model evaluation
* Hypothesis testing and hashtag analysis

## Files Included

### `data_collection.py`

This script was used to collect Instagram post data using the Instagram Graph API. It collects post captions, likes, comments, timestamps, and follower counts for selected accounts.

Sensitive information such as access tokens and account IDs are not included in this repository.

### `final.ipynb`

This notebook contains the main prototype implementation. It includes the full analysis pipeline, from loading the dataset to extracting hashtag features, training machine learning models, evaluating results, and producing the final output summary.

## Main Features Analysed

The prototype analyses the following hashtag-related features:

* Total number of hashtags per post
* Average hashtag length
* Hashtag language indicators
* UGT hashtag categories:

  * Informational
  * Entertaining
  * Relational
  * Remunerative
* Hashtag combinations
* Caption length
* Emoji count
* Sentiment score
* Engagement rate

## Machine Learning Models Used

The prototype compares the following models:

* Logistic Regression
* Random Forest
* XGBoost

The models are used to classify posts into high and low engagement groups based on the engagement rate.

## Notes

The raw dataset and API credentials are not included for privacy and ethical reasons. The prototype notebook shows the full processing, analysis, modelling, and evaluation steps used in the dissertation.

This repository was submitted as part of the dissertation prototype requirement.
