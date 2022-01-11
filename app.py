import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import numpy as np
import altair as alt

def normalizeData(trainingData):
    trainingData['age'] = pd.to_numeric(trainingData['age'], errors='coerce')
    return trainingData

# Obtain and Process Data
trainingDF = pd.read_csv("./data/labeledDataTrain.csv")
testDF = pd.read_csv("./data/labeledDataTest.csv",sep=",",encoding = 'cp1252')
trainingDF = normalizeData(trainingDF)
testDF = normalizeData(testDF)

st.set_page_config(page_title="CL-Aff Shared Task - In Pursuit of Happiness", layout="wide")

st.title("CL-Aff Shared Task - In Pursuit of Happiness")
st.markdown("""
* Corpus and annotations for the CL-Aff Shared Task - In Pursuit of Happiness - from the University of Pennsylvania
* A part of the AffCon Workshop @ AAAI 2019 for Modeling Affect-in-Action
* Check out the Workshop and Shared Task website: https://sites.google.com/view/affcon2019/home
""")

option = st.selectbox("What dataset would you like to explore?",("Training","Test"))
st.write('You selected:', option)


def ageHistogram(age):
    ageCount = []
    ageUnique = age.unique()
    age = age.tolist()
    ageUnique = ageUnique.tolist()
    for i in range(len(ageUnique)):
        occurrences = age.count(ageUnique[i])
        ageCount.append([ageUnique[i], occurrences])
    ageCount = pd.DataFrame(ageCount, columns=['Age', 'Frequency'])
    ageCount = ageCount.sort_values("Age")
    ageCount = ageCount[ageCount['Age'] > 16]
    ageCount = ageCount[ageCount['Age'] < 100]
    c = alt.Chart(ageCount).mark_bar().encode(x='Age',y='Frequency')
    st.altair_chart(c, use_container_width=True)

# Country Frequency Mapping
def nationHistogram(nations):
    nationsCount = []
    nationUnique = nations.unique()
    nations = nations.tolist()
    nationUnique = nationUnique.tolist()
    for i in range(len(nationUnique)):
        occurrences = nations.count(nationUnique[i])
        nationsCount.append([nationUnique[i], occurrences])
    nationsCount = pd.DataFrame(nationsCount, columns=['Nations', 'Frequency'])
    nationsCount = nationsCount.sort_values("Frequency")
    nationsCount = nationsCount.dropna()
    c = alt.Chart(nationsCount).mark_bar().encode(x='Nations',y='Frequency')
    st.altair_chart(c, use_container_width=True)

def marriageHistogram(marriage):
    marriageCount = []
    marriageUnique = marriage.unique()
    marriage = marriage.tolist()
    marriageUnique = marriageUnique.tolist()
    for i in range(len(marriageUnique)):
        occurrences = marriage.count(marriageUnique[i])
        marriageCount.append([marriageUnique[i], occurrences])
    marriageCount = pd.DataFrame(marriageCount, columns=['Relationship Status', 'Frequency'])
    marriageCount = marriageCount.dropna()
    c = alt.Chart(marriageCount).mark_bar().encode(x='Relationship Status',y='Frequency')
    st.altair_chart(c, use_container_width=True)


def durationHistogram(duration):
    durationCount = []
    durationUnique = duration.unique()
    duration = duration.tolist()
    durationUnique = durationUnique.tolist()
    for i in range(len(durationUnique)):
        occurrences = duration.count(durationUnique[i])
        durationCount.append([durationUnique[i], occurrences])
    durationCount = pd.DataFrame(durationCount, columns=['Duration', 'Frequency'])
    durationCount = durationCount.dropna()
    c = alt.Chart(durationCount).mark_bar().encode(x='Duration',y='Frequency')
    st.altair_chart(c, use_container_width=True)  

def genderHistorgram(gender):
    genderCount = []
    genderUnique = gender.unique()
    gender = gender.tolist()
    genderUnique = genderUnique.tolist()
    for i in range(len(genderUnique)):
        occurrences = gender.count(genderUnique[i])
        genderCount.append([genderUnique[i], occurrences])
    genderCount = pd.DataFrame(genderCount, columns=['Gender', 'Frequency'])
    genderCount = genderCount.dropna()
    c = alt.Chart(genderCount).mark_bar().encode(x='Gender',y='Frequency')
    st.altair_chart(c, use_container_width=True)     

def parentHoodHistogram(parent):
    parentCount = []
    parentUnique = parent.unique()
    parent = parent.tolist()
    parentUnique = parentUnique.tolist()
    for i in range(len(parentUnique)):
        occurrences = parent.count(parentUnique[i])
        parentCount.append([parentUnique[i], occurrences])
    parentCount = pd.DataFrame(parentCount, columns=['Parenthood', 'Frequency'])
    parentCount = parentCount.dropna()
    c = alt.Chart(parentCount).mark_bar().encode(x='Parenthood',y='Frequency')
    st.altair_chart(c, use_container_width=True)     



















if option == "Training":
    st.write(trainingDF) 
    st.title('Demographics')
    ageHistogram(trainingDF["age"])
    nationHistogram(trainingDF["country"])
    marriageHistogram(trainingDF["married"])
    durationHistogram(trainingDF["duration"])
    genderHistorgram(trainingDF["gender"])
    parentHoodHistogram(trainingDF["parenthood"])
    st.title('Demographics')


if option == "Test":
    st.write(testDF)
    st.title('Demographics')
    ageHistogram(testDF["age"])
    nationHistogram(testDF["country"])
    marriageHistogram(testDF["married"])
    durationHistogram(testDF["duration"])
    genderHistorgram(testDF["gender"])
    parentHoodHistogram(testDF["parenthood"])
