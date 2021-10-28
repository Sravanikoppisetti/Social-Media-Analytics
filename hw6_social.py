"""
Social Media Analytics Project
Name:
Roll Number:
"""
from typing import Counter
import hw6_social_tests as test

project = "Social" # don't edit this

### PART 1 ###

import pandas as pd
import nltk
nltk.download('vader_lexicon', quiet=True)
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
endChars = [ " ", "\n", "#", ".", ",", "?", "!", ":", ";", ")" ]
import re
'''
makeDataFrame(filename)
#3 [Check6-1]
Parameters: str
Returns: dataframe
'''
def makeDataFrame(filename):
    df=pd.read_csv(filename)
    #print(df['text'],df['message'])
    return df


'''
parseName(fromString)
#4 [Check6-1]
Parameters: str
Returns: str
'''
def parseName(fromString):
    newstring=re.split(':',fromString)[1]
    newstring1=re.split('\(',newstring)[0]
    name=newstring1.strip(" ")
    return  name


'''
parsePosition(fromString)
#4 [Check6-1]
Parameters: str
Returns: str
'''
def parsePosition(fromString):
    newstring2=re.split('\(',fromString)[1]
    newstring3=re.split('from',newstring2)[0]
    position=newstring3.strip(" ")
    return position


'''
parseState(fromString)
#4 [Check6-1]
Parameters: str
Returns: str
'''
def parseState(fromString):
    newstring4=re.split('from',fromString)[1]
    newstring5=re.split('\)',newstring4)[0]
    state=newstring5.strip(" ")
    return state


'''
findHashtags(message)
#5 [Check6-1]
Parameters: str
Returns: list of strs
'''
def findHashtags(message):
    lst=[]
    m=message.split("#")
    # print(m)
    for x in m[1:len(m)]:
        string=""
        # print(x)
        for y in x:
            if y not in endChars:
                string+=y
                # print(y)
            else:
                break
        string="#"+string
        lst.append(string)
        #print(lst)
    return lst

   #return re.findall(r"#\w+", message)


'''
getRegionFromState(stateDf, state)
#6 [Check6-1]
Parameters: dataframe ; str
Returns: str
'''
def getRegionFromState(stateDf, state):
    row=stateDf.loc[stateDf['state']==state,'region'] 
    return row.values[0]
    


'''
addColumns(data, stateDf)
#7 [Check6-1]
Parameters: dataframe ; dataframe
Returns: None
'''
def addColumns(data, stateDf):
    names = []
    positions = []
    states = []
    regions = []
    hashtags = []
    for index,row in data.iterrows():
        colvalue = data['label'].iloc[index]
        name = parseName(colvalue)
        pos = parsePosition(colvalue)
        state = parseState(colvalue)
        region = getRegionFromState(stateDf, state)
        txtvalue = data['text'].iloc[index]
        hashtag = findHashtags(txtvalue)
        names.append(name)
        positions.append(pos)
        states.append(state)
        regions.append(region)
        hashtags.append(hashtag)
    data['name'] = names
    data['position'] = positions
    data['state'] = states
    data['region'] = regions
    data['hashtags'] = hashtags
    return None



### PART 2 ###

'''
findSentiment(classifier, message)
#1 [Check6-2]
Parameters: SentimentIntensityAnalyzer ; str
Returns: str
'''
def findSentiment(classifier, message):
    score = classifier.polarity_scores(message)['compound']
    if score>0.1:
        return "positive"
    elif score<-0.1:
        return "negative"
    else:
        return "neutral"


'''
addSentimentColumn(data)
#2 [Check6-2]
Parameters: dataframe
Returns: None
'''
def addSentimentColumn(data):
    classifier = SentimentIntensityAnalyzer()
    sentiments=[]
    for index,row in data.iterrows():
        message=data['text'].iloc[index]
        text=findSentiment(classifier,message)
        sentiments.append(text)
    data["sentiment"]=sentiments
    #print(data.head(3))
    return



'''
getDataCountByState(data, colName, dataToCount)
#3 [Check6-2]
Parameters: dataframe ; str ; str
Returns: dict mapping strs to ints
'''
def getDataCountByState(data, colName, dataToCount):
    state_count={}
    for i,row in data.iterrows():
        if ((len(colName)==0) and (len(dataToCount)==0) or (row[colName]==dataToCount)):
                state=row["state"]
                if state not in state_count:
                    state_count[state] = 0
                state_count[state] += 1
    return state_count
df = makeDataFrame("data/politicaldata.csv")
stateDf = makeDataFrame("data/statemappings.csv")
addColumns(df, stateDf)
addSentimentColumn(df)
#print(getDataCountByState(df, "message", "policy"))

#df = makeDataFrame("data/politicaldata.csv")

'''
getDataForRegion(data, colName)
#4 [Check6-2]
Parameters: dataframe ; str
Returns: dict mapping strs to (dicts mapping strs to ints)
'''
def getDataForRegion(data, colName):
    region={}
    for i,row in data.iterrows():
        sub_region=row["region"]
        if sub_region not in region:
            region[sub_region] = {}
        if  sub_region  in region:
            att=row[colName]
            if att not in region[sub_region]:
                region[sub_region][att] = 0
            region[sub_region][att] += 1
    #print("rr",region)
    return region

    


'''
getHashtagRates(data)
#5 [Check6-2]
Parameters: dataframe
Returns: dict mapping strs to ints
'''
def getHashtagRates(data):
    hashtag_dict={}
    for i,row in data.iterrows():
        hash=row["hashtags"]
        for j in range(len(hash)):
            tag=hash[j]
            if tag not in hashtag_dict:
                hashtag_dict[tag] =0
            hashtag_dict[tag] += 1
    return (hashtag_dict)
'''
mostCommonHashtags(hashtags, count)
#6 [Check6-2]
Parameters: dict mapping strs to ints ; int
Returns: dict mapping strs to ints
'''
def mostCommonHashtags(hashtags, count):
    hashtagssorted={}
    Total=0
    hashtags_sorted_dict = sorted(hashtags, key=hashtags.get, reverse=True)
    for r in hashtags_sorted_dict:
        if Total<count:
            hashtagssorted[r]= hashtags[r]
            Total=Total+1
    #print(hashtagssorted)
    return (hashtagssorted)


'''
getHashtagSentiment(data, hashtag)
#7 [Check6-2]
Parameters: dataframe ; str
Returns: float
'''
def getHashtagSentiment(data, hashtag):
    #print("dd",data.head(2))
    score_list=[]
    for index,row in data.iterrows():
        if hashtag in row['text']:
            if row['sentiment']=='positive':
                score_list.append(1)
            elif row['sentiment']=='negative':
                score_list.append(-1)
            elif row['sentiment']=='neutral':
                score_list.append(0)
    #print("pp", sum(score_list)/len(score_list))
    return sum(score_list)/len(score_list)


### PART 3 ###

'''
graphStateCounts(stateCounts, title)
#2 [Hw6]
Parameters: dict mapping strs to ints ; str
Returns: None
'''
def graphStateCounts(stateCounts, title):
    import matplotlib.pyplot as plt
    xlst=[i for i in stateCounts]
    w=0.8
    ylst=[stateCounts[i] for i in stateCounts]
    for index in range(len(ylst)):
        plt.bar(xlst[index],ylst[index],width=w)
    plt.xticks(ticks=list(range(len(xlst))),label=xlst,rotation="vertical")
    plt.title("StateCount")
    plt.xlabel("State")
    plt.ylabel("Count")
    plt.show()
    return


'''
graphTopNStates(stateCounts, stateFeatureCounts, n, title)
#3 [Hw6]
Parameters: dict mapping strs to ints ; dict mapping strs to ints ; int ; str
Returns: None
'''
def graphTopNStates(stateCounts, stateFeatureCounts, n, title):
    featurerate={}
    topstates={}
    for i in stateFeatureCounts:
        featurerate[i]=(stateFeatureCounts[i]/stateCounts[i])
    topstates=dict(Counter(featurerate).most_common(n))
    graphStateCounts(topstates,"Top n Featured")
    return    


'''
graphRegionComparison(regionDicts, title)
#4 [Hw6]
Parameters: dict mapping strs to (dicts mapping strs to ints) ; str
Returns: None
'''
def graphRegionComparison(regionDicts, title):
    featurelst=[]
    regionlst=[]
    regionvalue=[]
    for i in regionDicts:
        templist=[]
        x=regionDicts[i]
        for j in x:
            if j not in featurelst:
                featurelst.append(j)
            templist.append(x[j])
        regionvalue.append(templist)
        regionlst.append(i)
    sideBySideBarPlots(featurelst,regionlst,regionvalue,title)
    return


'''
graphHashtagSentimentByFrequency(data)
#4 [Hw6]
Parameters: dataframe
Returns: None
'''
def graphHashtagSentimentByFrequency(data):
    return


#### PART 3 PROVIDED CODE ####
"""
Expects 3 lists - one of x labels, one of data labels, and one of data values - and a title.
You can use it to graph any number of datasets side-by-side to compare and contrast.
"""
def sideBySideBarPlots(xLabels, labelList, valueLists, title):
    import matplotlib.pyplot as plt

    w = 0.8 / len(labelList)  # the width of the bars
    xPositions = []
    for dataset in range(len(labelList)):
        xValues = []
        for i in range(len(xLabels)):
            xValues.append(i - 0.4 + w * (dataset + 0.5))
        xPositions.append(xValues)

    for index in range(len(valueLists)):
        plt.bar(xPositions[index], valueLists[index], width=w, label=labelList[index])

    plt.xticks(ticks=list(range(len(xLabels))), labels=xLabels, rotation="vertical")
    plt.legend()
    plt.title(title)

    plt.show()

"""
Expects two lists of probabilities and a list of labels (words) all the same length
and plots the probabilities of x and y, labels each point, and puts a title on top.
Expects that the y axis will be from -1 to 1. If you want a different y axis, change plt.ylim
"""
def scatterPlot(xValues, yValues, labels, title):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    plt.scatter(xValues, yValues)

    # make labels for the points
    for i in range(len(labels)):
        plt.annotate(labels[i], # this is the text
                    (xValues[i], yValues[i]), # this is the point to label
                    textcoords="offset points", # how to position the text
                    xytext=(0, 10), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center

    plt.title(title)
    plt.ylim(-1, 1)

    # a bit of advanced code to draw a line on y=0
    ax.plot([0, 1], [0.5, 0.5], color='black', transform=ax.transAxes)

    plt.show()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    # print("\n" + "#"*15 + " WEEK 1 TESTS " +  "#" * 16 + "\n")
    # test.week1Tests()
    # print("\n" + "#"*15 + " WEEK 1 OUTPUT " + "#" * 15 + "\n")
   

    ## Uncomment these for Week 2 ##
    """ print("\n" + "#"*15 + " WEEK 2 TESTS " +  "#" * 16 + "\n")
    # test.week2Tests()"""
    # print("\n" + "#"*15 + " WEEK 2 OUTPUT " + "#" * 15 + "\n")
    # test.runWeek2()
    # df = makeDataFrame("data/politicaldata.csv")
    # stateDf = makeDataFrame("data/statemappings.csv")
    # addColumns(df, stateDf)
    # addSentimentColumn(df)
    #test.testGetHashtagSentiment(df)
    #print(scatterPlot())

    #test.testGetDataCountByState(df)


    ## Uncomment these for Week 3 ##
    print("\n" + "#"*15 + " WEEK 3 OUTPUT " + "#" * 15 + "\n")
    test.runWeek3()