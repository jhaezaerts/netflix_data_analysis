import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
from PIL import UnidentifiedImageError
import datetime
import calendar
import os.path
import pickle as pkle
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
import openai


########################################################################################################################
# Define functions and variables
########################################################################################################################


def write(text):
    st.markdown(f'<p style="color:#E50914;font-size:28px;border-radius:2%;"><strong>{text}</strong></p>',
                unsafe_allow_html=True)


def scroll_down():
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader('.')
        st.subheader('.')
    with c2:
        st.write('')
        st.write('')
    with c3:
        st.write('')
        st.write('')


# API Credentials
openai.organization = st.secrets["OPENAI_ORG"]
openai.api_key = st.secrets["OPENAI_API_KEY"]

llm = OpenAI(api_token=openai.api_key)

netflix_logo = 'netflix_logo_icon_170919.png'
netflix_logo = Image.open(netflix_logo)

########################################################################################################################
# Main Page I
########################################################################################################################


st.title('Welcome to your Netflix rewind')
st.markdown('#')
st.markdown('#')

col1, col2, col3 = st.columns(3)
with col1:
    st.write('')
with col2:
    st.image(netflix_logo)
with col3:
    st.write('')
st.markdown('#')

########################################################################################################################
# Sidebar
########################################################################################################################


st.sidebar.subheader("1 - Request your [Netflix data](https://www.netflix.com/account/getmyinfo)")
st.sidebar.subheader("2 - Upload ViewingActivity.csv")
uploaded_file = st.sidebar.file_uploader('')
if uploaded_file is not None:
    if uploaded_file.name == "ViewingActivity.csv":
        st.sidebar.subheader('3 - Analyze and chill')
    try:
        df = pd.read_csv(uploaded_file)
    except UnicodeDecodeError as ude:
        print(ude)
        write("You've uploaded the wrong file")
        df = None
    try:
        # Drop unnecessary columns
        df = df.drop(['Attributes', 'Supplemental Video Type', 'Device Type', 'Bookmark', 'Latest Bookmark'], axis=1)
        # Remove whitespace in column names
        df.columns = [column.replace(' ', '_') for column in df.columns]
        # Change dtype to datetime
        df['Start_Time'] = pd.to_datetime(df['Start_Time'], utc=True)
        # Change dtype to timedelta
        df['Duration'] = pd.to_timedelta(df['Duration'])
        # Only keep data gathered in Belgium.
        df = df[df['Country'] == 'BE (Belgium)']
        # Clean df for analysis
        df = df[['Profile_Name', 'Start_Time', 'Duration', 'Title', 'Country']]
        # Add features for further analysis
        df['Weekday'] = df['Start_Time'].dt.weekday
        df['Hour'] = df['Start_Time'].dt.hour
        df['Day'] = df['Start_Time'].dt.day
        df['Month'] = df['Start_Time'].dt.month
        df['Year'] = df['Start_Time'].dt.year
        # Split title into multiple columns to generate more content-related features
        content = df['Title'].str.split(':', expand=True)
        # Create and clean new features
        for i in range(1, 6):
            content[i].fillna("", inplace=True)
        content['Episode'] = content[2] + content[3] + content[4] + content[5]
        content = content.drop([2, 3, 4, 5], axis=1)
        content.rename(columns={0: "Title_right", 1: "Season"}, inplace=True)
        #  Clean new features
        content['part'] = np.where(content['Season'].str.contains('Season'), '', content['Season'])
        content['Season'] = np.where(content['Season'].str.contains('Season'), content['Season'], '')
        content['Episode'] = content['Episode'] + content['part']
        content = content.drop(['part'], axis=1)
        # Join new features with df and perform preparations for content-related analysis
        df = pd.concat([df.reset_index(drop=True), content.reset_index(drop=True)], axis=1)
        df = df.drop(['Title'], axis=1)
        df.rename({'Title_right': 'Title'}, inplace=True, axis=1)
        df = df[
            ['Profile_Name', 'Start_Time', 'Duration', 'Country', 'Weekday', 'Hour', 'Day', 'Month', 'Year', 'Title',
             'Season', 'Episode']]

        ########################################################################################################################
        # Main Page II
        ########################################################################################################################

        t1, t2 = st.tabs(["Get ready-made analysis", "Perform GPT-powered analysis"])
        with t1:
            profiles = df['Profile_Name'].unique()
            select_profile = st.selectbox('PICK YOUR PROFILE', profiles)
            st.markdown('#')

            for name in profiles:
                if select_profile == name:
                    df = df[df['Profile_Name'] == name]
                    df = df.reset_index(drop=True)
                    st.subheader(
                        'First things first. The first piece of content you ever watched on this Netflix profile is')
                    write(df['Title'][-1:].to_string(index=False))
                    write(df['Start_Time'][-1:].to_string(index=False))

                    st.markdown("""---""")

                    start_times_by_hour = df['Hour'].value_counts().reset_index()
                    st.subheader("You're most likely to be watching Netflix between ")
                    st.write("test")
                    write(start_times_by_hour['index'][0].astype(str) + "h and " + (
                                start_times_by_hour['index'][0] + 1).astype(str) + "h")
                    st.write("another test")
                    st.markdown("""---""")

                    st.subheader('Your favourite day of the week for watching Netflix is')
                    start_times_by_day = df['Weekday'].value_counts().reset_index()
                    write(calendar.day_name[start_times_by_day['index'][0]])

                    st.markdown("""---""")

                    morning_hours = start_times_by_hour.sort_values('index')[6:12]['Hour'].sum()
                    total_hours = start_times_by_hour['Hour'].sum()
                    st.subheader('Morning person? Out of all the time you have spent watching Netflix, ')
                    write(round(((morning_hours / total_hours) * 100), 2).astype(str) + '%')
                    st.subheader(' of it occurred before noon (6am-12pm)')

                    st.markdown("""---""")

                    st.subheader(
                        'Worktime watcher? The percentage of time spent on Netflix during working hours (9am-5pm) on workdays is')
                    worktime = df[df['Weekday'] < 5]['Hour'].value_counts().reset_index().sort_values('index')[9:17][
                        'Hour'].sum()
                    write(round(((worktime / total_hours) * 100), 2).astype(str) + '%')

                    st.markdown("""---""")

                    st.subheader(
                        'Your overall time spent watching Netflix since the creation of your profile is approximately')
                    overall_time_spent = df['Duration'].sum()
                    overall_time_spent_hours = int(overall_time_spent.total_seconds() / (60 * 60))
                    write(str(overall_time_spent_hours) + " hours (that's " + str(overall_time_spent).split(' ')[
                        0] + " days!)")

                    st.markdown("""---""")

                    st.subheader("Here's a breakdown of your watching time by year")
                    time_spent_by_year = df.groupby('Year')['Duration'].sum().reset_index().to_string(
                        index=False).split('\n')[1:]
                    for year in time_spent_by_year:
                        write(year.strip().replace(' ', ' :  ', 1))

                    st.markdown("""___""")

                    max_year = df['Year'].max()
                    st.subheader("And here's how you're doing by month in " + str(max_year))
                    time_spent_by_month_2022 = df[df['Year'] == max_year].groupby('Month')[
                        'Duration'].sum().reset_index()
                    time_spent_by_month_2022['Month'] = time_spent_by_month_2022['Month'].apply(
                        lambda x: calendar.month_name[x])
                    time_spent_by_month_2022 = time_spent_by_month_2022.to_string(index=False).split('\n')[1:]
                    for month in time_spent_by_month_2022:
                        write(month.strip().replace(' ', ' : ', 1))

                    st.markdown("""---""")

                    max_date = datetime.datetime.now()
                    start_date = datetime.datetime(max_date.year, 1, 1)
                    max_date = datetime.datetime.now()
                    ytd_time = str(max_date - start_date).split(',')[0]
                    ytd_netflix = df[df['Year'] == max_year]['Duration'].sum()

                    time_spent_pct = str(round((ytd_netflix / ytd_time) * 100, 2))
                    st.subheader(ytd_time + ". That's the amount of time that has passed in " + str(max_year) +
                                 " up until today. Given that you have spent " + str(ytd_netflix).split(' ')[
                                     0] + " days " +
                                 "and " + str(ytd_netflix).split(' ')[2].split(':')[0] + " hours " + "(" +
                                 str(int(str(ytd_netflix).split(' ')[0]) * 24 + int(
                                     str(ytd_netflix).split(' ')[2].split(':')[0])) +
                                 " hours)" + " of it on Netflix, you have spent")
                    write(time_spent_pct + '%')
                    st.subheader("of your time watching Netflix in " + str(max_year) + ".")

                    st.markdown("""---""")

                    pd.options.display.max_colwidth = 100
                    st.subheader("Here's some information on your longest single day binge")
                    single_day_binge = df.groupby(['Year', 'Month', 'Day'])['Duration'].sum().reset_index()
                    single_day_binge = single_day_binge.rename(columns={"Duration": "Sum_Duration"})
                    single_day_binge = pd.merge(df, single_day_binge, how='inner', left_on=['Year', 'Month', 'Day'],
                                                right_on=['Year', 'Month', 'Day'])
                    max_binge_time = single_day_binge['Sum_Duration'].max()
                    single_day_binge = single_day_binge[single_day_binge['Sum_Duration'] == max_binge_time]
                    st.subheader('This sitting went on for')
                    write(str(max_binge_time).split(' ')[-1])
                    st.subheader('It started at ')
                    write(str(single_day_binge['Start_Time'].min()).split('+')[0])
                    st.subheader("And ended at")
                    write((str(single_day_binge['Start_Time'].max() + single_day_binge['Duration'].iloc[0])).split('+')[
                              0])
                    st.subheader('You started off with watching')
                    write(single_day_binge['Title'][-1:].to_string(index=False) + ' -'
                          + single_day_binge['Season'][-1:].to_string(index=False)
                          + ' -' + single_day_binge['Episode'][-1:].to_string(index=False))
                    st.subheader("And ended this epic session with")
                    write(single_day_binge['Title'][:1].to_string(index=False) + ' -'
                          + single_day_binge['Season'][:1].to_string(index=False)
                          + ' -' + single_day_binge['Episode'][:1].to_string(index=False))

                    st.markdown("""---""")

                    st.subheader("These are the shows that you spent most time watching")
                    most_popular_titles = df.groupby(['Title'])['Duration'].sum().reset_index()
                    most_popular_titles = most_popular_titles.rename(columns={"Duration": "Total_Duration"})
                    most_popular_titles = most_popular_titles.sort_values(by='Total_Duration',
                                                                          ascending=False).reset_index(drop=True)[:5]

                    top_5 = [f"%s - %s" % title for title in
                             zip(most_popular_titles['Title'], most_popular_titles['Total_Duration'])]
                    for i in range(len(top_5)):
                        write(str(i + 1) + '. ' + top_5[i])

        with t2:
            st.write("test")
            """
            st.subheader("flix-GPT")
            st.write("query your Netflix data using natural language.")
            st.dataframe(df.head())
            query = st.textbox(label='pandasai', placeholder='Ask me about your Netflix data',
                               label_visibility='collapsed')
            pandas_ai = PandasAI(llm, conversational=False)
            if query:
                response = pandas_ai.run(df, prompt=query)
            st.write(response)
            """
    except KeyError as ke:
        print(ke)
    except NameError as ne:
        print(ne)

hide_streamlit_style = """
                       <style>
                       # MainMenu {visibility: hidden;}
                       footer {visibility: hidden;}
                       footer:after {
                       content:'made by jorgo haezaerts';
                       visibility: visible;
                       display: block;
                       position: relative;
                       text-align: left;
                       #background-color: red;
                       padding: 5px;
                       bottom: 10px;
                       </style>
                       """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

########################################################################################################################
