import re
import pandas as pd


def preprocess(data):
    pattern = '\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}\s*[ap]m\s*-\s'
    
    message = re.split(pattern=pattern, string=data)[2:]
    dates = re.findall(pattern=pattern, string=data)[1:]
    
    # Clean the 'dates' to remove the trailing '- '
    dates = [date.strip(' -') for date in dates]
    
    df = pd.DataFrame({'user_message': message, 'message_date': dates})
    
    # Type cast into datetime
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p')

    df.rename(columns={'message_date': 'date'}, inplace=True)
    
    # Separate username and message from message data
    username = []
    messages = []
    username_pattern = '([\w\W]+?):\s'

    for message in df['user_message']:
        entry = re.split(pattern=username_pattern, string=message)
        if entry[1:]:  # Username
            username.append(entry[1])
            messages.append(entry[2])
        else:
            username.append('group_notification')
            messages.append(entry[0])

    df['username'] = username
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    
    period = []

    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        elif hour == 0:
            period.append(str('00') + '-' + str(hour+1))
        else:
            period.append(str(hour) + '-' + str(hour+1))
    
    df['period'] = period
    
    return df
