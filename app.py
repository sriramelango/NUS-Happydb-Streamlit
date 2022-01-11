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


st.title("CL-Aff Shared Task - In Pursuit of Happiness")
st.markdown("""
* Corpus and annotations for the CL-Aff Shared Task - In Pursuit of Happiness - from the University of Pennsylvania
* A part of the AffCon Workshop @ AAAI 2019 for Modeling Affect-in-Action
* Check out the Workshop and Shared Task website: https://sites.google.com/view/affcon2019/home
""")

option = st.selectbox("What dataset would you like to explore?",("Training","Test"))
st.write('You selected:', option)



def ageHistorgram(age):
    ageCount = []
    ageUnique = age.unique()
    age = age.tolist()
    print(type(ageUnique))
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


if option == "Training":
    st.write(trainingDF) 
    ageHistorgram(trainingDF["age"])


if option == "Test":
    st.write(testDF)
    ageHistorgram(testDF["age"])



# Country Frequency Mapping
