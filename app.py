from plotly import graph_objs as go
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud, STOPWORDS
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap
import plotly.express as px
from plotly.subplots import make_subplots
import sklearn
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler

# Set Page Options
st.set_page_config(layout = 'wide')


#Variable Initialization  
nations = np.array([['EST',"59", "26"], ['ETH',"8", "38"], ['IDN',"-5", "120"], ['ASM', "-14.3333", "-170"], ['PER', "-10", "-76"], ['KOR',"40", "127"], ['ECU',"-2", "-77.5"], ['KEN',"1", "38"], ['MAC',"22.1667", "113.55"], ['USA',"38", "-97"], ['IND',"20", "77"], ['MYS',"2.5", "112.5"], ['DEU',"51", "9"], ['UGA',"1", "32"], ['BEL',"50.8333", "4"], ['ISR',"31.5", "34.75"], ['JAM', "18.25", "-77.5"], ['ARM', "40", "45"], ['SWE', "62", "15"], ['MKD', "41.8333", "22"], ['LCA',"13.8833", "-61.1333"], ['LKA',"7", "81"], ['GBR', "54", "-2"], ['ROU',"46", "25"], ['CRI',"10", "-84"], ['VEN',"8", "-66"], ['FRA',"46", "2"], ['GEO',"42", "43.5"], ['NGA',"10", "8"], ['LTU',"56", "24"], ['PAK',"30", "70"], ['TTO',"11", "-61"], ['MLT',"35.8333", "14.5833"], ['BHR',"26", "50.55"], ['FIN',"64", "26"], ['VNM',"16", "106"], ['AIA',"18.25", "-63.1667"], ['SVN', "46", "15"], ['NZL',"-41", "174"], ['DZA',"28", "3"], ['KAZ',"48", "68"], ['UMI',"19.2833", "166.6"], ['ALB',"41", "20"], ['SUR', "4", "-56"], ['COL',"4", "-72"], ['KWT',"29.3375", "47.6581"], ['ESP',"40", "-4"], ['AUS',"-27", "133"], ['MDA',"47", "29"], ['AUT',"47.3333", "13.3333"], ['NLD',"52.5", "5.75"], ['THA',"15", "100"], ['JPN',"36", "138"], ['TUR',"39", "35"], ['CHN',"35", "105"], ['NIC',"13", "-85"], ['NOR', "62", "10"], ['PRI',"18.25", "-66.5"], ['SGP',"1.3667", "103.8"], ['PRT',"39.5", "-8"], ['IRL', "53", "-8"], ['URY',"-33", "-56"], ['PHL',"13", "122"], ['ISL',"65", "-18"], ['DNK',"56", "10"], ['EGY',"27", "30"], ['GTM',"15.5", "-90.25"], ['CZE',"49.75", "15.5"], ['VCT',"13.25", "-61.2"], ['ABW',"12.5", "-69.9667"], ['ATA',"-90", "0"], ['AFG',"33", "65"], ['SRB',"44", "21"], ['BRB',"13.1667", "-59.5333"], ['UKR', "49", "32"], ['GRC',"39", "22"], ['DOM',"19", "-70.6667"], ['BRA',"-10", "-55"], ['MAR',"32", "-5"], ['CAN',"60", "-95"], ['MEX',"23", "-102"], ['ARE',"24", "54"], ['ZAF',"-29", "24"], ['RUS',"60", "100"], ['SLV',"13.8333", "-88.9167"], ['BGR',"43", "25"], ['ARG',"-34", "-64"], ['BHS',"24.25", "-76"], ['ITA',"42.8333", "12.8333"]])
nations = pd.DataFrame(nations, columns = ['Country','latitude','longitude'])
nations["latitude"] = pd.to_numeric(nations["latitude"])
nations["longitude"] = pd.to_numeric(nations["longitude"])


# Data Processing
def normalizeData(trainingData):
    trainingData['age'] = pd.to_numeric(trainingData['age'], errors='coerce')
    return trainingData

def dataBarGraphProcess(data,xlabel,ylabel):
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

def normalizeDataGraph(data, xLabel, emotion = False):
    min_max_scaler = preprocessing.MinMaxScaler()
    column_names_to_normalize = ['Frequency']
    if emotion == False:
        data = dataBarGraphProcess(data, xLabel, 'Frequency')
        freq = data[column_names_to_normalize].values
        freq_scaled = min_max_scaler.fit_transform(freq)
        df_temp = pd.DataFrame(freq_scaled, columns= column_names_to_normalize, index = data.index)
        data[column_names_to_normalize] = df_temp
        return data
    else:
        #The Emotion Data always has the equivalent frequency for Social and Agency
        data["Frequency"] = 1
        return data

# Data Graph Plotting Functions
def ageBarGraph(age, name = "", norm = False):
    if (norm == False):
        ageData = dataBarGraphProcess(age, 'Age', 'Frequency')
    else:
        ageData = age
    ageData = ageData.sort_values("Age")
    ageData = ageData[ageData['Age'] > 16]
    ageData = ageData[ageData['Age'] < 100]
    if name == "":
        fig = px.bar(ageData, x="Age",y="Frequency")
        st.plotly_chart(fig, use_container_width=True)
    else:
        x = np.array(ageData["Age"])
        y = np.array(ageData["Frequency"])
        trace = go.Bar(name = name, x = x, y = y)
        return trace

def nationBarGraph(nations):
    nationData = dataBarGraphProcess(nations, 'Nations', 'Frequency')
    fig = px.bar(nationData, x="Nations",y="Frequency")
    st.plotly_chart(fig, use_container_width=True)

def singaporeGraph(data, xLabel):
    data = dataBarGraphProcess(data, xLabel, 'Frequency')
    fig = px.bar(data, x= xLabel,y="Frequency")
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

def marriageBarGraph(marriage, name = "", norm = False):
    if (norm == False):
        marriageData = dataBarGraphProcess(marriage, 'Relationship Status', 'Frequency')
    else:
        marriageData = marriage
    marriageData.reindex([1,0,4,3,5])
    x = np.array(marriageData["Relationship Status"])
    y = np.array(marriageData["Frequency"])
    trace = go.Bar(name = name, x = x, y = y)
    return trace

def durationBarGraph(duration, name = "", norm = False):
    if (norm == False):
        durationData = dataBarGraphProcess(duration, 'Duration of Happiness', 'Frequency')
    else:
        durationData = duration
    durationData = durationData.reindex([5,1,9,0,2,3,6])
    durationData = durationData.drop([3, 6])
    durationData.at[0, 'Duration of Happiness'] = 'Half a Day'
    durationData.at[1, 'Duration of Happiness'] = '1 Hour Min'
    durationData.at[2, 'Duration of Happiness'] = 'All Day'
    durationData.at[5, 'Duration of Happiness'] = 'Few Minutes'
    durationData = durationData.reset_index()
    durationData = durationData.dropna()
    if name == "":
        fig = px.bar(durationData, x="Duration of Happiness",y="Frequency")
        st.plotly_chart(fig, use_container_width=True)
    else:
        x = np.array(durationData["Duration of Happiness"])
        y = np.array(durationData["Frequency"])
        trace = go.Bar(name = name, x = x, y = y)
        return trace

def genderBarGraph(gender, name = "", norm = False):
    if (norm == False):
        genderData = dataBarGraphProcess(gender, 'Gender', 'Frequency')
    else:
        genderData = gender
    x = np.array(genderData["Gender"])
    y = np.array(genderData["Frequency"])
    trace = go.Bar(name = name, x = x, y = y)
    return trace

def parentHoodBarGraph(parent, name = "", norm = False):
    if (norm == False):
        parentData = dataBarGraphProcess(parent, 'Parenthood Status', 'Frequency')
    else:
        parentData = parent
    x = np.array(parentData['Parenthood Status'])
    y = np.array(parentData["Frequency"])
    trace = go.Bar(name = name, x = x, y = y)
    return trace 

def emotionBarGraph(data, name = "", norm = False):
    agencyData = data['agency']
    agencyData = agencyData.tolist()
    agencyOccurances = agencyData.count("yes")
    socialData = data['social']
    socialData = socialData.tolist()
    socialOccurances = agencyData.count("yes")
    emotionalFrequency = {'Emotion Types' : ["Agency","Social"], "Frequency": [agencyOccurances, socialOccurances]}
    emotionalFrequency = pd.DataFrame(emotionalFrequency)
    if (norm):
        emotionalFrequency = normalizeDataGraph(emotionalFrequency, "Emotion Types", True)
    x = np.array(emotionalFrequency["Emotion Types"])
    y = np.array(emotionalFrequency["Frequency"])
    trace = go.Bar(name = name, x = x, y = y)
    return trace  

def conceptBarGraph(concepts, name = "", norm = False):
    conceptsArray = " "
    for index, values in concepts.items():
        conceptsArray += str(values) + " "
    conceptsArray = conceptsArray.lower()
    conceptsArray = conceptsArray.replace("|"," ")
    conceptsArray = pd.Series(conceptsArray.split())
    if norm == False:
        conceptsData = dataBarGraphProcess(conceptsArray, 'Concepts', 'Frequency')
    else:
        conceptsData = normalizeDataGraph(conceptsArray, 'Concepts')
    if name == "":
        fig = px.bar(conceptsData, x="Concepts",y="Frequency")
        st.plotly_chart(fig, use_container_width=True)     
    else:
        x = np.array(conceptsData["Concepts"])
        y = np.array(conceptsData["Frequency"])
        trace = go.Bar(name = name, x = x, y = y)
        return trace  

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

#Plots all Data in Format
def plotCharts(data):
    #Graphs 
  #  st.subheader("Word Cloud")
    #genWordCloud(data["moment"])
    st.subheader("Dataset")
    st.write(data)
    st.subheader("Frequency Graphs")
    conceptBarGraph(data["concepts"])
    ageBarGraph(data["age"])

    # Subplots Called from Functions
    trace1 = marriageBarGraph(data["married"])
    trace2 = genderBarGraph(data["gender"])
    trace3 = parentHoodBarGraph(data["parenthood"])
    trace4 = emotionBarGraph(data)

    # Subplots Plotting to GUI
    fig = make_subplots(rows = 2, cols = 2, subplot_titles = ("Relationship Status", "Gender", "Parents", "Emotion Type"), y_title = "Frequency")
    fig.append_trace(trace1, 1,1)
    fig.append_trace(trace2, 1, 2)
    fig.append_trace(trace3, 2, 1)
    fig.append_trace(trace4, 2, 2)
    fig.layout.update(showlegend = False)
    st.plotly_chart(fig, use_container_width=True)

    #Graphs
    durationBarGraph(data["duration"])
    nationBarGraph(data["country"])

# Functionality for User Selection in @Demographics Section
def demographicAnalysis(optionDataset, optionDemographic, singapore = False):
    if optionDemographic == "Country":
        if singapore == False:
            selectionOptions = pd.DataFrame(optionDataset["country"].unique()).dropna()._append(["ALL"])
            nation = st.selectbox("Where would you like to explore?", selectionOptions)
            displayData(optionDataset, "country", nation)
        else:
            plotSingapore(optionDataset)
            
    if optionDemographic == "Age":
        selectionOptions = pd.DataFrame(optionDataset["age"].unique()).dropna()._append(["ALL"])
        age = st.selectbox("What age would you like to explore?", selectionOptions)
        if singapore == False:
            displayData(optionDataset, "age", age)      
        else:
            displayData(optionDataset, "age", age, True)

    if optionDemographic == "Gender":
        selectionOptions = pd.DataFrame(optionDataset["gender"].unique()).dropna()._append(["ALL"])
        gender = st.selectbox("What gender would you like to explore?", selectionOptions)
        if singapore == False:
            displayData(optionDataset, "gender", gender)
        else:
            displayData(optionDataset, "gender", gender, True)

# Adds Functionality for Selecting Between All Data and Filtered Data
def displayData(dataset, selection, selectionType, singapore = False):
    if selectionType == "ALL":
        if singapore == False:
            plotCharts(dataset)
        else:
            plotSingapore(dataset)
    else:
        data = dataset[dataset[selection] == selectionType]
        if singapore == False:
            plotCharts(data)
        else:
            plotSingapore(data)

#Singapore Data Analysis
def plotSingapore(data):
    #Graphs 
   # st.subheader("Word Cloud")
   # genWordCloud(data["moment"])
    st.subheader("Dataset")
    st.write(data)
    st.subheader("Frequency Graphs")
    conceptBarGraph(data["concepts"])
    singaporeGraph(data["age"], "Age")
    singaporeGraph(data["race"], "Race")
    durationBarGraph(data["duration"])
    singaporeGraph(data["gender"], "Gender")

def compareSingapore(nationData, nationName):
    #Pie Chart 
    sizes = [len(singaporeData), len(nationData)]
    pie = go.Pie(labels = ["Singapore", nationName], values = sizes)
    fig = go.Figure(pie)
    fig.update_layout(barmode='group', title= "Data Composition in Comparison")
    st.plotly_chart(fig, use_container_width=True)

    #Concept Data
    trace1 = conceptBarGraph(nationData["concepts"], nationName)
    traceSGP = conceptBarGraph(singaporeData["concepts"], "Singapore")
    fig = go.Figure(data = [trace1, traceSGP])
    fig.update_layout(barmode='group', title= "Age")
    st.plotly_chart(fig, use_container_width=True)

    #Duration Data
    traceSGP = durationBarGraph(singaporeData["duration"], "Singapore")
    trace1 = durationBarGraph(nationData["duration"], nationName)
    fig = go.Figure(data = [trace1, traceSGP])
    fig.update_layout(barmode='group', title= "Age")
    st.plotly_chart(fig, use_container_width=True)


# Obtain and Process Labeled Data
trainingDF = normalizeData(pd.read_csv("./data/labeledDataTrain.csv"))
testDF = normalizeData(pd.read_csv("./data/labeledDataTest.csv",sep=",",encoding = 'cp1252'))
singaporeData = pd.read_csv("./data/sg_happydb_data_completecases.csv")
singaporeData = singaporeData.dropna()

#Merge DataSets and Process Data
testDF = testDF.reindex(columns=['hmid',"moment","concepts","agency","social","age","country","gender","married","parenthood","reflection","duration"])
allDF = pd.concat([trainingDF, testDF])
allDF = allDF.reset_index()


# Introductory Information
st.title("CL-Aff Shared Task - In Pursuit of Happiness")

st.markdown("""
* Corpus and annotations for the CL-Aff Shared Task - In Pursuit of Happiness - from the University of Pennsylvania
* A part of the AffCon Workshop @ AAAI 2019 for Modeling Affect-in-Action
* Check out the Workshop and Shared Task website: https://sites.google.com/view/affcon2019/home
* Here is the link to the Github for more information! https://github.com/kj2013/claff-happydb
* Made by @sriramelango: https://github.com/sriramelango
""")

#User Interaction
with st.expander("Survey/Data Distribution"):
    st.header('Survey/Data Distribution')
    optionMap = st.selectbox("What map woud you like to explore?",("Scattermap","Heatmap"))
    if optionMap == "Scattermap":
        st.map(nations)
    if optionMap == "Heatmap":
        heatMap(nations)

with st.expander("Demographics"):
    st.header('Demographics')
    optionDataSet = st.selectbox("What dataset would you like to explore?",("All", "Training","Test", "Singapore"))
    optionDemographic = st.selectbox("What demographic would you like to explore?",("Country","Age", "Gender"))
    if optionDataSet == "All":
        demographicAnalysis(allDF, optionDemographic)
    if optionDataSet == "Training":
        demographicAnalysis(trainingDF, optionDemographic)
    if optionDataSet == "Test":
        demographicAnalysis(testDF, optionDemographic)
    if optionDataSet == "Singapore":
        demographicAnalysis(singaporeData, optionDemographic, True)

with st.expander("Compare"):
    selectionOptions = pd.DataFrame(allDF["country"].unique()).dropna()._append(["SGP"])
    compareOptions = st.multiselect("Select Two Countries to Compare", selectionOptions)
    normalizeOption = st.selectbox("Do you want to normalize the data?", ["No","Yes"])

    if normalizeOption == "No":

        if (len(compareOptions) == 2):

            if (compareOptions[0] == "SGP"):
                country1 = allDF[allDF["country"] == compareOptions[1]]
                compareSingapore(country1, compareOptions[1])
            
            elif (compareOptions[1] == "SGP"):
                country1 = allDF[allDF["country"] == compareOptions[0]]
                compareSingapore(country1, compareOptions[0])

            else:          
                # Obtain Data
                country1 = allDF[allDF["country"] == compareOptions[0]]
                country2 = allDF[allDF["country"] == compareOptions[1]]

                #Pie Chart 
                sizes = [len(country1), len(country2)]
                pie = go.Pie(labels = [compareOptions[0], compareOptions[1]], values = sizes)
                fig = go.Figure(pie)
                fig.update_layout(barmode='group', title= "Data Composition in Comparison")
                st.plotly_chart(fig, use_container_width=True)

                #Age Data
                trace1 = ageBarGraph(country1["age"], compareOptions[0])
                trace2 = ageBarGraph(country2["age"], compareOptions[1])
                fig = go.Figure(data = [trace1, trace2])
                fig.update_layout(barmode='group', title= "Age")
                st.plotly_chart(fig, use_container_width=True)

                #Concepts Data
                trace1 = conceptBarGraph(country1["concepts"], compareOptions[0])
                trace2 = conceptBarGraph(country2["concepts"], compareOptions[1])
                fig = go.Figure(data = [trace1, trace2])
                fig.update_layout(barmode='group', title= "Concepts")
                st.plotly_chart(fig, use_container_width=True)

                #Duration Data
                trace1 = durationBarGraph(country1["duration"], compareOptions[0])
                trace2 = durationBarGraph(country2["duration"], compareOptions[1])
                fig = go.Figure(data = [trace1, trace2])
                fig.update_layout(barmode='group', title= "Duration of Happiness")
                st.plotly_chart(fig, use_container_width=True)

                #Gender Data
                trace1 = genderBarGraph(country1["gender"], compareOptions[0])
                trace2 = genderBarGraph(country2["gender"], compareOptions[1])
                fig = go.Figure(data = [trace1, trace2])
                fig.update_layout(barmode='group', title="Gender")
                st.plotly_chart(fig, use_container_width=True)

                #Emotion Data
                trace1 = emotionBarGraph(country1, compareOptions[0])
                trace2 = emotionBarGraph(country2, compareOptions[1])
                fig = go.Figure(data = [trace1, trace2])
                fig.update_layout(barmode='group', title= "Emotion Type")
                st.plotly_chart(fig, use_container_width=True)

                #Marriage Data
                trace1 = marriageBarGraph(country1["married"], compareOptions[0])
                trace2 = marriageBarGraph(country2["married"], compareOptions[1])
                fig = go.Figure(data = [trace1, trace2])
                fig.update_layout(barmode='group', title="Relationship Status")
                st.plotly_chart(fig, use_container_width=True)

                #Parenthood Data
                trace1 = parentHoodBarGraph(country1["parenthood"], compareOptions[0])
                trace2 = parentHoodBarGraph(country2["parenthood"], compareOptions[1])
                fig = go.Figure(data = [trace1, trace2])
                fig.update_layout(barmode='group', title= "Parenthood Status")
                st.plotly_chart(fig, use_container_width=True)


    if normalizeOption == "Yes":

        if (len(compareOptions) == 2):

            st.warning("Note: Normalization is through min-max method - Graphs with few data types and minimal data will be impacted")
            
            if (compareOptions[0] == "SGP" or compareOptions[1] == "SGP"):
                st.error("Singapore is not supported for data normalization")

            else:
                # Obtain Data
                country1 = allDF[allDF["country"] == compareOptions[0]]
                country2 = allDF[allDF["country"] == compareOptions[1]]

                #Age Data
                ageData1 = normalizeDataGraph(country1["age"],"Age")
                ageData2 = normalizeDataGraph(country2["age"],"Age")
                trace1 = ageBarGraph(ageData1, compareOptions[0], True)
                trace2 = ageBarGraph(ageData2, compareOptions[1], True)
                fig = go.Figure(data = [trace1, trace2])
                fig.update_layout(barmode='group', title= "Age")
                st.plotly_chart(fig, use_container_width=True)

                #Concepts Data
                trace1 = conceptBarGraph(country1["concepts"], compareOptions[0], True)
                trace2 = conceptBarGraph(country2["concepts"], compareOptions[1], True)
                fig = go.Figure(data = [trace1, trace2])
                fig.update_layout(barmode='group', title= "Concepts")
                st.plotly_chart(fig, use_container_width=True)

                #Duration Data
                durationData1 = normalizeDataGraph(country1["duration"],"Duration")
                durationData2 = normalizeDataGraph(country2["duration"],"Duration")
                trace1 = durationBarGraph(durationData1, compareOptions[0], True)
                trace2 = durationBarGraph(durationData2, compareOptions[1], True)
                fig = go.Figure(data = [trace1, trace2])
                fig.update_layout(barmode='group', title= "Duration of Happiness")
                st.plotly_chart(fig, use_container_width=True)

                #Gender Data
                genderData1 = normalizeDataGraph(country1["gender"],"Gender")
                genderData2 = normalizeDataGraph(country2["gender"],"Gender")
                trace1 = genderBarGraph(genderData1, compareOptions[0], True)
                trace2 = genderBarGraph(genderData2, compareOptions[1], True)
                fig = go.Figure(data = [trace1, trace2])
                fig.update_layout(barmode='group', title="Gender")
                st.plotly_chart(fig, use_container_width=True)

                #Marriage Data
                marriageData1 = normalizeDataGraph(country1["married"],"Relationship Status")
                marriageData2 = normalizeDataGraph(country2["married"],"Relationship Status")
                trace1 = marriageBarGraph(marriageData1, compareOptions[0], True)
                trace2 = marriageBarGraph(marriageData2, compareOptions[1], True)
                fig = go.Figure(data = [trace1, trace2])
                fig.update_layout(barmode='group', title="Relationship Status")
                st.plotly_chart(fig, use_container_width=True)

                #Parenthood Data
                parentHood1 = normalizeDataGraph(country1["parenthood"],"Parenthood Status")
                parentHood2 = normalizeDataGraph(country2["parenthood"],"Parenthood Status")
                trace1 = parentHoodBarGraph(parentHood1, compareOptions[0], True)
                trace2 = parentHoodBarGraph(parentHood2, compareOptions[1], True)
                fig = go.Figure(data = [trace1, trace2])
                fig.update_layout(barmode='group', title= "Parenthood Status")
                st.plotly_chart(fig, use_container_width=True)