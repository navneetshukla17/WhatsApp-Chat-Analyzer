import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import seaborn as sns

# props = FontProperties()

st.sidebar.title('WhatsApp Chat Analyzer')
st.sidebar.info('Export your whatsapp chat and upload .txt file to analyze you chats.')

uploaded_file = st.sidebar.file_uploader('Upload your file from here')

if uploaded_file is not None:
    byte_data = uploaded_file.getvalue()
    data = byte_data.decode(encoding='utf-8')
    df = preprocessor.preprocess(data)
    
    #st.table(df.head())
    
    # fetch unique users
    user_list = df['username'].unique().tolist()
    user_list.sort()
    # wired error !
    user_list.remove('group_notification') # comment out this line while analyzing one-to-one chats
    user_list.insert(0, 'Overall')
    
    selected_user = st.sidebar.selectbox('Select user', user_list)
    
    if st.sidebar.button('Show Analysis'):
        
        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(df, selected_user)
        st.title('Top Statistics')
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.header('Total Messages')
            st.title(num_messages)
        with col2:
            st.header('Total Words')
            st.title(words)
        with col3:
            st.header('Media Shared')
            st.title(num_media_messages)
        with col4:
            st.header('Links Shared')
            st.title(num_links)
        
        # monthly timeline
        st.title('Monthly Timeline')
        time_line = helper.monthly_timeline(df, selected_user)
        fig, ax = plt.subplots()
        ax.plot(time_line['time'], time_line['message'], color='green')
        plt.xticks(rotation=90)
        st.pyplot(fig)
        
        # Daily timeline
        st.title('Daily Timeline')
        daily_timeline = helper.daily_timeline(df, selected_user)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='orange')
        plt.xticks(rotation=90)
        st.pyplot(fig)
        
        # Activity Map
        st.title('Activity Map')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.header('Most Active Day')
            active_day = helper.week_activity_map(df, selected_user)
            fig,ax = plt.subplots()
            ax.bar(active_day.index, active_day.values)
            plt.xticks(rotation=90)
            st.pyplot(fig)
        with col2:
            st.header('Most Active Month')
            active_month = helper.month_activity_map(df, selected_user)
            fig,ax = plt.subplots()
            ax.bar(active_month.index, active_month.values)
            plt.xticks(rotation=90)
            st.pyplot(fig)
        
        # Activity Heatmap
        st.title('User Activity Heatmap')
        user_heatmap = helper.activity_heatmap(df, selected_user)
        plt.figure(figsize=(10,15))
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
        
        
        # finding most active users from the group(Grop Level)
        if selected_user == 'Overall':
            st.title('Most Active Users')
            x, x_percent = helper.fetch_most_active_users(df)
            
            fig, ax = plt.subplots()
            
            col1, col2 = st.columns(2)
            
            with col1:
                ax.bar(x.index, x.values, color='red')
                st.pyplot(fig)
            with col2:
                st.table(x_percent)
        
        # WordCloud
        st.title('Word Cloud')
        df_wc = helper.create_wordcloud(df, selected_user)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        
        # Most common words
        most_common_df = helper.most_common_words(df, selected_user)
        fig, ax = plt.subplots()
        st.title('Most Common Words')
        ax.barh(most_common_df[0], most_common_df[1], color=['red', 'blue', 'green', 'orange','pink', 'yellow'])
        st.pyplot(fig)
        plt.xticks(rotation=90)

        # emojis analysis
        emoji_df = helper.emoji_helper(df, selected_user)
        st.title('Most Common Emojis Shared')
        col1, col2 = st.columns(2)
        
        with col1:
            st.table(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct='%.2f')
            st.pyplot(fig)