import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud, STOPWORDS
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap
import plotly.express as px

st.set_option('deprecation.showPyplotGlobalUse', False)

#Variable Initialization  
nations = np.array([['EST',"59", "26"], ['ETH',"8", "38"], ['IDN',"-5", "120"], ['ASM', "-14.3333", "-170"], ['PER', "-10", "-76"], ['KOR',"40", "127"], ['ECU',"-2", "-77.5"], ['KEN',"1", "38"], ['MAC',"22.1667", "113.55"], ['USA',"38", "-97"], ['IND',"20", "77"], ['MYS',"2.5", "112.5"], ['DEU',"51", "9"], ['UGA',"1", "32"], ['BEL',"50.8333", "4"], ['ISR',"31.5", "34.75"], ['JAM', "18.25", "-77.5"], ['ARM', "40", "45"], ['SWE', "62", "15"], ['MKD', "41.8333", "22"], ['LCA',"13.8833", "-61.1333"], ['LKA',"7", "81"], ['GBR', "54", "-2"], ['ROU',"46", "25"], ['CRI',"10", "-84"], ['VEN',"8", "-66"], ['FRA',"46", "2"], ['GEO',"42", "43.5"], ['NGA',"10", "8"], ['LTU',"56", "24"], ['PAK',"30", "70"], ['TTO',"11", "-61"], ['MLT',"35.8333", "14.5833"], ['BHR',"26", "50.55"], ['FIN',"64", "26"], ['VNM',"16", "106"], ['AIA',"18.25", "-63.1667"], ['SVN', "46", "15"], ['NZL',"-41", "174"], ['DZA',"28", "3"], ['KAZ',"48", "68"], ['UMI',"19.2833", "166.6"], ['ALB',"41", "20"], ['SUR', "4", "-56"], ['COL',"4", "-72"], ['KWT',"29.3375", "47.6581"], ['ESP',"40", "-4"], ['AUS',"-27", "133"], ['MDA',"47", "29"], ['AUT',"47.3333", "13.3333"], ['NLD',"52.5", "5.75"], ['THA',"15", "100"], ['JPN',"36", "138"], ['TUR',"39", "35"], ['CHN',"35", "105"], ['NIC',"13", "-85"], ['NOR', "62", "10"], ['PRI',"18.25", "-66.5"], ['SGP',"1.3667", "103.8"], ['PRT',"39.5", "-8"], ['IRL', "53", "-8"], ['URY',"-33", "-56"], ['PHL',"13", "122"], ['ISL',"65", "-18"], ['DNK',"56", "10"], ['EGY',"27", "30"], ['GTM',"15.5", "-90.25"], ['CZE',"49.75", "15.5"], ['VCT',"13.25", "-61.2"], ['ABW',"12.5", "-69.9667"], ['ATA',"-90", "0"], ['AFG',"33", "65"], ['SRB',"44", "21"], ['BRB',"13.1667", "-59.5333"], ['UKR', "49", "32"], ['GRC',"39", "22"], ['DOM',"19", "-70.6667"], ['BRA',"-10", "-55"], ['MAR',"32", "-5"], ['CAN',"60", "-95"], ['MEX',"23", "-102"], ['ARE',"24", "54"], ['ZAF',"-29", "24"], ['RUS',"60", "100"], ['SLV',"13.8333", "-88.9167"], ['BGR',"43", "25"], ['ARG',"-34", "-64"], ['BHS',"24.25", "-76"], ['ITA',"42.8333", "12.8333"]])
nations = pd.DataFrame(nations, columns = ['Country','latitude','longitude'])
nations["latitude"] = pd.to_numeric(nations["latitude"], downcast="float")
nations["longitude"] = pd.to_numeric(nations["longitude"], downcast="float")

def normalizeData(trainingData):
    trainingData['age'] = pd.to_numeric(trainingData['age'], errors='coerce')
    return trainingData

def dataHistogramProcess(data,xlabel,ylabel):
    dataFiltered = []
    dataUnique = data.unique()
    data = data.tolist()
    dataUnique = dataUnique.tolist()
    for i in range(len(dataUnique)):
        occurrences = data.count(dataUnique[i])
        dataFiltered.append([dataUnique[i], occurrences])
    dataFiltered = pd.DataFrame(dataFiltered, columns=[xlabel, ylabel])
    dataFiltered = dataFiltered.dropna()
    return dataFiltered

def ageHistogram(age):
    ageData = dataHistogramProcess(age, 'Age', 'Frequency')
    ageData = ageData.sort_values("Age")
    ageData = ageData[ageData['Age'] > 16]
    ageData = ageData[ageData['Age'] < 100]
    fig = px.bar(ageData, x="Age",y="Frequency")
    st.plotly_chart(fig, use_container_width=True)


# Country Frequency Mapping - NEED TO CHANGE TO GRAPHING BASED ON MAPS(HEAT MAP)
def nationHistogram(nations):
    nationData = dataHistogramProcess(nations, 'Nations', 'Frequency')
    fig = px.bar(nationData, x="Nations",y="Frequency")
    st.plotly_chart(fig, use_container_width=True)

def heatMap(data):
    # Resource intensive!
    map_heatmap = folium.Map(location=[0, 0], zoom_start=2.4)
    data = data[["latitude", "longitude"]]
    # List comprehension to make list of lists
    heat_data = [[row["latitude"], row["longitude"]] for index, row in data.iterrows()]
    # Plot it on the map
    HeatMap(heat_data).add_to(map_heatmap)
    folium_static(map_heatmap)

def marriageHistogram(marriage):
    marriageData = dataHistogramProcess(marriage, 'Relationship Status', 'Frequency')
    marriageData.reindex([1,0,4,3,5])
    fig = px.bar(marriageData, x="Relationship Status",y="Frequency")
    st.plotly_chart(fig, use_container_width=True)


def durationHistogram(duration):
    durationData = dataHistogramProcess(duration, 'Duration of Happiness', 'Frequency')
    durationData = durationData.reindex([5,1,9,0,2,3,6])
    durationData = durationData.drop([3, 6])
    durationData.at[0, 'Duration of Happiness'] = 'Half a Day'
    durationData.at[1, 'Duration of Happiness'] = '1 Hour Min'
    durationData.at[2, 'Duration of Happiness'] = 'All Day'
    durationData.at[5, 'Duration of Happiness'] = 'Few Minutes'
    durationData = durationData.reset_index()
    durationData = durationData.dropna()
    fig = px.bar(durationData, x="Duration of Happiness",y="Frequency")
    st.plotly_chart(fig, use_container_width=True)

def genderHistorgram(gender):
    genderData = dataHistogramProcess(gender, 'Gender', 'Frequency')
    fig = px.bar(genderData, x="Gender",y="Frequency")
    st.plotly_chart(fig, use_container_width=True)

def parentHoodHistogram(parent):
    parentData = dataHistogramProcess(parent, 'Parenthood Status', 'Frequency')
    fig = px.bar(parentData, x="Parenthood Status",y="Frequency")
    st.plotly_chart(fig, use_container_width=True)    

def emotionHistogram(data):
    agencyData = data['agency']
    agencyData = agencyData.tolist()
    agencyOccurances = agencyData.count("yes")
    socialData = data['social']
    socialData = socialData.tolist()
    socialOccurances = agencyData.count("yes")
    emotionalFrequency = {'Emotion Types' : ["Agency","Social"], "Frequency": [agencyOccurances, socialOccurances]}
    emotionalFrequency = pd.DataFrame(emotionalFrequency)
    fig = px.bar(emotionalFrequency, x="Emotion Types",y="Frequency")
    st.plotly_chart(fig, use_container_width=True)   

def conceptHistogram(concepts):
    conceptsArray = " "
    for index, values in concepts.items():
        conceptsArray += values + " "
    conceptsArray = conceptsArray.replace("|"," ")
    conceptsArray = pd.Series(conceptsArray.split())
    conceptsData = dataHistogramProcess(conceptsArray, 'Concepts', 'Frequency')
    fig = px.bar(conceptsData, x="Concepts",y="Frequency")
    st.plotly_chart(fig, use_container_width=True)      

def demographicViewer(country, data):
    countryDataset = data[data["country"] == country]
    ageHistogram(countryDataset["age"])
    marriageHistogram(countryDataset["married"])
    durationHistogram(countryDataset["duration"])
    genderHistorgram(countryDataset["gender"])
    parentHoodHistogram(countryDataset["parenthood"])
    emotionHistogram(countryDataset)
    conceptHistogram(countryDataset["concepts"])
    genWordCloud(countryDataset["moment"])
   
def genWordCloud(moments):
    words = ""
    stopwords = set(STOPWORDS)
    for index,values in moments.items():
        words += values + " "
    words = words.lower()
    wordCloud = WordCloud(background_color = "black", stopwords=stopwords, prefer_horizontal=1).generate(words) 
    plt.imshow(wordCloud, interpolation="bilinear") 
    plt.axis('off') 
    st.pyplot()


# Obtain and Process Data
trainingDF = normalizeData(pd.read_csv("./data/labeledDataTrain.csv"))
testDF = normalizeData(pd.read_csv("./data/labeledDataTest.csv",sep=",",encoding = 'cp1252'))

#Merge DataSets and Process Data
testDF = testDF.reindex(columns=['hmid',"moment","concepts","agency","social","age","country","gender","married","parenthood","reflection","duration"])
allDF = pd.concat([trainingDF, testDF])
allDF = allDF.reset_index()
#st.set_page_config(page_title="CL-Aff Shared Task - In Pursuit of Happiness", layout="wide")

st.title("CL-Aff Shared Task - In Pursuit of Happiness")

st.markdown("""
* Corpus and annotations for the CL-Aff Shared Task - In Pursuit of Happiness - from the University of Pennsylvania
* A part of the AffCon Workshop @ AAAI 2019 for Modeling Affect-in-Action
* Check out the Workshop and Shared Task website: https://sites.google.com/view/affcon2019/home
""")



#User Interaction
with st.expander("Survey/Data Distribution"):
    st.subheader('Survey/Data Distribution')
    optionMap = st.selectbox("What map woud you like to explore?",("Heatmap","Scattermap"))
    if optionMap == "Heatmap":
        heatMap(nations)
    if optionMap == "Scattermap":
        st.map(nations)

with st.expander("Demographics"):
    st.subheader('Demographics')
    optionDataSet = st.selectbox("What dataset would you like to explore?",("All", "Training","Test"))
    if optionDataSet == "All":
            selectionOptions = pd.DataFrame(allDF["country"].unique()).dropna().append(["ALL"])
            nation = st.selectbox("Where would you like to explore?", selectionOptions)
            if nation == "ALL":
                st.write(allDF) 
                ageHistogram(allDF["age"])
                nationHistogram(allDF["country"])
                marriageHistogram(allDF["married"])
                durationHistogram(allDF["duration"])
                genderHistorgram(allDF["gender"])
                parentHoodHistogram(allDF["parenthood"])
                conceptHistogram(allDF["concepts"])
                emotionHistogram(allDF)
                genWordCloud(allDF["moment"])
            else:
                st.write(trainingDF[allDF["country"] == nation]) 
                demographicViewer(nation, allDF)

    if optionDataSet == "Training":
        selectionOptions = pd.DataFrame(trainingDF["country"].unique()).dropna().append(["ALL"])
        nation = st.selectbox("Where would you like to explore?", selectionOptions)
        if nation == "ALL":
            st.write(trainingDF) 
            ageHistogram(trainingDF["age"])
            nationHistogram(trainingDF["country"])
            marriageHistogram(trainingDF["married"])
            durationHistogram(trainingDF["duration"])
            genderHistorgram(trainingDF["gender"])
            parentHoodHistogram(trainingDF["parenthood"])
            conceptHistogram(trainingDF["concepts"])
            emotionHistogram(trainingDF)
            genWordCloud(trainingDF["moment"])
        else:
            st.write(trainingDF[trainingDF["country"] == nation]) 
            demographicViewer(nation, trainingDF)

    if optionDataSet == "Test":
        selectionOptions = pd.DataFrame(testDF["country"].unique()).dropna().append(["ALL"])
        nation = st.selectbox("Where would you like to explore?", selectionOptions)
        if nation == "ALL":
            st.write(testDF) 
            ageHistogram(testDF["age"])
            nationHistogram(testDF["country"])
            marriageHistogram(testDF["married"])
            durationHistogram(testDF["duration"])
            genderHistorgram(testDF["gender"])
            parentHoodHistogram(testDF["parenthood"])
            conceptHistogram(trainingDF["concepts"])
            emotionHistogram(testDF)
            genWordCloud(trainingDF["moment"])
        else:
            st.write(testDF[testDF["country"] == nation]) 
            demographicViewer(nation, testDF)

with st.expander("Compare"):
    selectionOptions = pd.DataFrame(allDF["country"].unique()).dropna()
    compareOptions = st.multiselect("Select Two Countries to Compare", selectionOptions)

    