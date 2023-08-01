from wordcloud import WordCloud
from urlextract import URLExtract
import pandas as pd
from collections import Counter
import emoji
from PIL import Image
import numpy as np

extractor = URLExtract()


def fetch_stats(selected_user,df):

    if selected_user !="Overall":
        df = df[df['user']== selected_user]

    num_messages = df.shape[0]

    words=[]    # fetch number of words
    for message in df['message']:
        words.extend(message.split())

    media_message_num = df[df['message']=='<Media omitted>\n'].shape[0] # total number of media that is shared
    
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages,len(words),media_message_num,len(links)



#Fetching most busiest user


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})

    if 'Group_notification' in x:
        x= x.drop("Group_notification")
        
    return x,df


def create_wordcloud(selected_user,df):
    f = open("stop_hinglish.txt","r")
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user']== selected_user]

    temp = df[df['user'] !='group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
                
        return " ".join(y)
        

    wc = WordCloud(width = 700,height = 700,min_font_size = 10,background_color="white")
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user,df):

    f = open("stop_hinglish.txt","r")
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user']== selected_user]

    temp = df[df['user'] !='group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    emojis=[]
    for message in df['message']:
        for c in message:
            if c in emoji.EMOJI_DATA:
                emojis.extend(c)

    words=[]

    for message in temp['message']:
    #     words.extend(message.split())
        for word in message.lower().split():
            if word not in stop_words:
                if word not in emojis:
                    words.append(word)

    most_common_words_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_words_df




def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']== selected_user]

    emojis=[]
    for message in df['message']:
        for c in message:
            if c in emoji.EMOJI_DATA:
                emojis.extend(c)

    
    emoji_df = pd.DataFrame(Counter(emojis).most_common(20))

    return emoji_df




def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']== selected_user]

    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))

    timeline['time'] = time

    return timeline



def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']== selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline



def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']== selected_user]


    return df['day_name'].value_counts()



def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']== selected_user]


    return df['month'].value_counts()


def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']== selected_user]

    
    activity_heatmap = df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)

    return activity_heatmap


def sentiment_analysis(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']== selected_user]

    x = sum(df['positive'])
    y = sum(df['negative'])
    z = sum(df['neutral'])

    sent = ""

    def score(a,b,c):
        if (a>b) and (a>c):
            return ("Positive")
        elif (b>c) and (b>a):
            return ("Negative")
        else:
            return ("Neutral")
        

    da = [(x/df.shape[0])*100,(y/df.shape[0])*100,(z/df.shape[0])*100]
    emo = ['Positive','Negative','Neutral']

    


    result = score(x,y,z)

    return result,da,emo