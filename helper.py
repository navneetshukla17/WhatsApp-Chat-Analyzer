from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import seaborn as sns

extractor = URLExtract()

def fetch_stats(df, selected_user):
    
    if selected_user != 'Overall':
        df = df[df['username'] == selected_user]
    
    # fetch the number of messages
    num_messages = df.shape[0]
    
    # fetch the total number of words
    words=[]
    for message in df['message']:
        words.extend(message.split())
    
    # fetch number of media shared
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    
    # fetch number of links shared
    links = []
    
    for message in df['message']:
        links.extend(extractor.find_urls(text=message))
        
        
    return num_messages, len(words), num_media_messages, len(links)

def fetch_most_active_users(df):
    
    x = df['username'].value_counts().head()
    x_percent = round((df['username'].value_counts()/df.shape[0])*100,2).head(6).reset_index().rename(columns={'username':'name', 'count':'percent'})
    
    return x, x_percent

def create_wordcloud(df, selected_user):
    
    # import stop words file
    f = open(file='stop_hinglish.txt', mode='r')
    stop_words = f.read()
    
    if selected_user != 'Overall':
        df = df[df['username'] == selected_user]
        
    # remove group_notification messages
    temp = df[df['username'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    
    def remove_stop_words(message):
        y = []
        for word in message:
            if word not in stop_words:
                y.append(word)
        return ' '.join(y)
       
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=' '))
    
    return df_wc

def most_common_words(df, selected_user):
    # import stop words file
    f = open(file='stop_hinglish.txt', mode='r')
    stop_words = f.read()
    
    if selected_user != 'Overall':
        df = df[df['username'] == selected_user]
        
    # remove group_notification messages
    temp = df[df['username'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(df, selected_user):
    
    if selected_user != 'Overall':
        df = df[df['username'] == selected_user]
    
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    
    return emoji_df

def monthly_timeline(df, selected_user):
    
    if selected_user != 'Overall':
        df = df[df['username'] == selected_user]
    
    time_line = df.groupby(by=['year', 'month']).count()['message'].reset_index()
    
    time = []
    for i in range(time_line.shape[0]):
        time.append(time_line['month'][i] + '-' + str(time_line['year'][i]))
    
    time_line['time'] = time
    
    return time_line

def daily_timeline(df, selected_user): 
    
    if selected_user != 'Overall':
        df = df[df['username'] == selected_user]
    
    daily_timeline = df.groupby(by=['only_date']).count()['message'].reset_index()
    
    return daily_timeline

def week_activity_map(df, selected_user):
    if selected_user != 'Overall':
        df = df[df['username'] == selected_user]
    
    return df['day_name'].value_counts()

def month_activity_map(df, selected_user):
    if selected_user != 'Overall':
        df = df[df['username'] == selected_user]
        
    return df['month'].value_counts()

def activity_heatmap(df, selected_user):
    
    if selected_user != 'Overall':
        df = df[df['username'] == selected_user]
    
    user_heatmap = data=df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap
