import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import numpy as np
import altair as alt
from wordcloud import WordCloud, STOPWORDS
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap

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
    ageUnique = dataUnique.tolist()
    for i in range(len(ageUnique)):
        occurrences = data.count(ageUnique[i])
        dataFiltered.append([ageUnique[i], occurrences])
    dataFiltered = pd.DataFrame(dataFiltered, columns=[xlabel, ylabel])
    dataFiltered = dataFiltered.dropna()
    return dataFiltered

def ageHistogram(age):
    ageData = dataHistogramProcess(age, 'Age', 'Frequency')
    ageData = ageData.sort_values("Age")
    ageData = ageData[ageData['Age'] > 16]
    ageData = ageData[ageData['Age'] < 100]
    c = alt.Chart(ageData).mark_bar().encode(x='Age',y='Frequency').interactive()
    st.altair_chart(c, use_container_width=True)

# Country Frequency Mapping - NEED TO CHANGE TO GRAPHING BASED ON MAPS(HEAT MAP)
def nationHistogram(nations):
    nationData = dataHistogramProcess(nations, 'Nations', 'Frequency')
    c = alt.Chart(nationData).mark_bar().encode(x='Nations',y='Frequency').interactive()
    st.altair_chart(c, use_container_width=True)

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
    c = alt.Chart(marriageData).mark_bar().encode(x='Relationship Status',y='Frequency').interactive()
    st.altair_chart(c, use_container_width=True)

def durationHistogram(duration):
    durationData = dataHistogramProcess(duration, 'Duration of Happiness', 'Frequency')
    c = alt.Chart(durationData).mark_bar().encode(x='Duration of Happiness',y='Frequency').interactive()
    st.altair_chart(c, use_container_width=True)  

def genderHistorgram(gender):
    genderData = dataHistogramProcess(gender, 'Gender', 'Frequency')
    c = alt.Chart(genderData).mark_bar().encode(x='Gender',y='Frequency').interactive()
    st.altair_chart(c, use_container_width=True)     

def parentHoodHistogram(parent):
    parentData = dataHistogramProcess(parent, 'Parenthood Status', 'Frequency')
    c = alt.Chart(parentData).mark_bar().encode(x='Parenthood Status',y='Frequency').interactive()
    st.altair_chart(c, use_container_width=True)     

def emotionHistogram(data):
    agencyData = data['agency']
    agencyData = agencyData.tolist()
    agencyOccurances = agencyData.count("yes")
    socialData = data['social']
    socialData = socialData.tolist()
    socialOccurances = agencyData.count("yes")
    emotionalFrequency = {'Labels' : ["Agency","Social"], "Frequency": [agencyOccurances, socialOccurances]}
    emotionalFrequency = pd.DataFrame(emotionalFrequency)
    c = alt.Chart(emotionalFrequency).mark_bar().encode(x='Labels',y='Frequency').interactive()
    st.altair_chart(c, use_container_width=True)

def conceptHistogram(concepts):
    conceptsArray = " "
    for index, values in concepts.items():
        conceptsArray += values + " "
    conceptsArray = conceptsArray.replace("|"," ")
    conceptsArray = pd.Series(conceptsArray.split())
    conceptsData = dataHistogramProcess(conceptsArray, 'Concepts', 'Frequency')
    c = alt.Chart(conceptsData).mark_bar().encode(x='Concepts',y='Frequency').interactive()
    st.altair_chart(c, use_container_width=True)     

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
    wordCloud = WordCloud(background_color = "black", stopwords=stopwords).generate(words) 
    plt.imshow(wordCloud, interpolation="bilinear") 
    plt.axis('off') 
    st.pyplot()


# Obtain and Process Data
trainingDF = normalizeData(pd.read_csv("./data/labeledDataTrain.csv"))
testDF = normalizeData(pd.read_csv("./data/labeledDataTest.csv",sep=",",encoding = 'cp1252'))

# Set UI and Interface
#st.set_page_config(page_title="CL-Aff Shared Task - In Pursuit of Happiness", layout="wide")

st.title("CL-Aff Shared Task - In Pursuit of Happiness")

st.markdown("""
* Corpus and annotations for the CL-Aff Shared Task - In Pursuit of Happiness - from the University of Pennsylvania
* A part of the AffCon Workshop @ AAAI 2019 for Modeling Affect-in-Action
* Check out the Workshop and Shared Task website: https://sites.google.com/view/affcon2019/home
""")

st.subheader('Data Distribution')

#User Interaction
optionMap = st.selectbox("What map woud you like to explore?",("Heatmap","Scattermap"))
if optionMap == "Heatmap":
    heatMap(nations)
if optionMap == "Scattermap":
    st.map(nations)

optionDataSet = st.selectbox("What dataset would you like to explore?",("Training","Test"))
st.write('You selected:', optionDataSet)

if optionDataSet == "Training":
    st.write(trainingDF) 
    st.title('Demographics')
    selectionOptions = pd.DataFrame(trainingDF["country"].unique()).dropna().append(["ALL"])
    nation = st.selectbox("Where would you like to explore?", selectionOptions)
    if nation == "ALL":
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
        demographicViewer(nation, trainingDF)

if optionDataSet == "Test":
    st.write(testDF) 
    st.title('Demographics')
    selectionOptions = pd.DataFrame(testDF["country"].unique()).dropna().append(["ALL"])
    nation = st.selectbox("Where would you like to explore?", selectionOptions)
    if nation == "ALL":
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
        demographicViewer(nation, testDF)
