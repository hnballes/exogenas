import streamlit as st
import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
import joblib
import urllib.request
from datetime import datetime, timedelta, date
from sklearn.preprocessing import MinMaxScaler

def data_load(selectedcountry):
    covid_url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
    covid = pd.read_csv(covid_url, parse_dates=['date'], index_col=['date'])
    # We filter the country, dates and the variable to predict

    country = selectedcountry
    variable = 'new_cases' #we could make it a selectbox
    initialdate = '2020-01-01'   # first day of the year, where most of our data starts
    initialdateshift = str(date.fromordinal(datetime.strptime(initialdate, '%Y-%m-%d').toordinal() + 6))
    enddate = str(date.fromordinal(date.today().toordinal()-1))   # yesterday's date: last day of available data

    # Filtering country and dates
    covid_ctry = covid[covid['location']==country]
    covid_ctry = covid_ctry.loc[initialdate:enddate]

    # Filter the variable to predict and applying 7-day rolling mean
    covid_ctry_var = covid_ctry[variable]
    covid_ctry_varR = covid_ctry_var.rolling(7).mean().dropna()
    
    return covid_ctry_varR


# Create a title, a subheader.
st.title("Coronavirus forecast")
st.subheader("This is an app for predicting new number of coronavirus cases during two weeks according to public data. ")

#chooose a country to predict the cases
st.title("Choose a country")
country = st.selectbox("", ("Denmark","Germany","Spain","Finland","Italy","Sweden","France","Norway","United Kingdom","United States","Canada","Mexico","Australia","Indonesia","Malaysia","Philippines","Thailand","Hong Kong","Vietnam","China","India","Japan","Singapore","Taiwan","Saudi Arabia","United Arab Emirates"))

#select the values of the 2 diferent variables
st.subheader("testing policy")
st.text("0 - no testing policy\n1 - only those who both (a) have symptoms AND (b) meet specific criteria (eg key workers)\n2 - testing of anyone showing Covid-19 symptoms\n3 - open public testing (eg drive through testing available to asymptomatic people")

testing = st.slider('choose the testing policy applied next week:', 0, 3, 1)
testing2 = st.slider('choose the testing policy applied the week after:', 0, 3, 1)

st.subheader("Record government policy on contact tracing after a positive diagnosis")
st.text("0 - no contact tracing\n1 - limited contact tracing; not done for all cases\n2 - comprehensive contact tracing; done for all identified cases")

tracing = st.slider('choose the contact tracing policy applied next week:', 0, 3, 1)
tracing2 = st.slider('choose the contact tracing policy applied the week after:', 0, 3, 1)
