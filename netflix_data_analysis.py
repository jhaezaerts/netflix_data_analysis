import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
from PIL import UnidentifiedImageError
import datetime
import calendar
import os.path
import pickle as pkle


# Netflix Rewind App


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


image = '<svg xmlns="http://www.w3.org/2000/svg" width="222px" height="222px" viewBox="-49.6 0 222 222" ' \
        'id="svg2"><style>.st0{fill:#b1060f;stroke:#000}.st1{fill:url(#path5719_1_)}.st2{fill:#e50914}</style><g ' \
        'id="layer1" transform="translate(12.495 6.756)"><g id="g4182"><g id="g5747" transform="translate(81.631 ' \
        '113.771) scale(.29074)"><path id="path4155" class="st0" d="M-52.5-412.3l-.3 168-.3 168-13.8-39v-.1l-17.9 ' \
        '374c17.6 49.6 27 76.1 27.1 76.2.1.1 10.1.7 22.2 1.3 36.6 1.8 82 5.7 116.5 10 8 1 14.8 1.5 15.3 ' \
        '1.1s.6-171.4.5-380.1l-.3-379.4h-149z"/><path id="path4157" class="st0" d="M-322-412.8V-33c0 208.9.2 380 .5 ' \
        '380.3.3.3 13.2-1 28.8-2.7 15.6-1.7 37.1-3.9 47.8-4.8 16.4-1.4 65.6-4.5 71.2-4.6 1.7 0 1.8-8.5 ' \
        '2-160.9l.3-160.9 11.9 33.6c1.8 5.2 2.4 6.8 4.2 ' \
        '11.9l17.9-373.9c-3.8-10.7-1.8-5.1-6.1-17.3-14.6-41.3-27-76.2-27.5-77.8l-1-2.8h-150z"/><path id="path5715" ' \
        'class="st0" d="M-52.5-412.3l-.3 168-.3 168-13.8-39v-.1l-17.9 374c17.6 49.6 27 76.1 27.1 76.2.1.1 10.1.7 22.2 ' \
        '1.3 36.6 1.8 82 5.7 116.5 10 8 1 14.8 1.5 15.3 1.1s.6-171.4.5-380.1l-.3-379.4h-149z"/><path id="path5717" ' \
        'class="st0" d="M-322-412.8V-33c0 208.9.2 380 .5 380.3.3.3 13.2-1 28.8-2.7 15.6-1.7 37.1-3.9 47.8-4.8 ' \
        '16.4-1.4 65.6-4.5 71.2-4.6 1.7 0 1.8-8.5 2-160.9l.3-160.9 11.9 33.6c1.8 5.2 2.4 6.8 4.2 ' \
        '11.9l17.9-373.9c-3.8-10.7-1.8-5.1-6.1-17.3-14.6-41.3-27-76.2-27.5-77.8l-1-2.8h-150z"/><radialGradient ' \
        'id="path5719_1_" cx="18038.016" cy="-146.44" r="368.717" gradientTransform="matrix(.07072 -.02449 -.897 ' \
        '-2.5906 -1526.665 25.194)" gradientUnits="userSpaceOnUse"><stop offset="0"/><stop offset="1" ' \
        'stop-opacity="0"/></radialGradient><path id="path5719" class="st1" d="M-322-412.8v213.2l150.2 398.4c0-9.1 ' \
        '0-14.1.1-24.5l.3-160.9 11.9 33.6C-93.5 234.2-58 334.6-57.8 334.8c.1.1 10.1.7 22.2 1.3 36.6 1.8 82 5.7 116.5 ' \
        '10 8 1 14.8 1.5 15.3 1.1.3-.3.5-84.1.5-202.4L-52.7-285l-.1 40.7-.3 ' \
        '168-13.8-39c-13.5-38.1-22.5-63.6-76.8-217-14.6-41.3-27-76.2-27.5-77.8l-1-2.8H-322v.1z"/><path id="path5721" ' \
        'class="st2" d="M-322-412.8l150.5 426.5v-.2l11.9 33.6C-93.5 234.2-58 334.6-57.8 334.8c.1.1 10.1.7 22.2 1.3 ' \
        '36.6 1.8 82 5.7 116.5 10 7.9 1 14.8 1.5 15.2 ' \
        '1.1L-53.1-76.4v.1l-13.8-39c-13.5-38.1-22.5-63.6-76.8-217-14.6-41.3-27-76.2-27.5-77.8l-1-2.8h-74.9l-74.9.1z' \
        '"/></g></g></g></svg> '

### Main Page I ###
st.title('Welcome to your Netflix rewind')
st.markdown('#')

col1, col2, col3 = st.columns(3)
with col1:
    st.write('')
with col2:
    st.image(image)
with col3:
    st.write('')
st.markdown('#')

# st.write("Each year, Spotify shares a summary of your listening behaviour. Something many people happily share on "
#          "their Instagram stories. _'Look how many hours I spent listening to music! Let's see how many more I can get "
#          "next year!'_ So why doesn't Netflix share with us such a summary? Can you guess? Maybe it's because for some,"
#          " a Netflix rewind feels more like an intervention rather than a cool analysis you can show off to your "
#          "friends. I can imagine sitting through a Netflix rewind and feeling like a lazy, useless piece of garbage by "
#          "the time it's done. It's not unlikely that a Netflix rewind would reduce watching behaviour rather than "
#          "increase it. Anyway, this app means to lift the veil on your personal Netflix viewing behaviour. All you need"
#          " to do is upload your data and pick a profile. Have fun!")

### Sidebar ###
st.sidebar.subheader("1- Request your [Netflix data](https://www.netflix.com/account/getmyinfo)")
st.sidebar.subheader("2 - Upload ViewingActivity.csv")
uploaded_file = st.sidebar.file_uploader('')
if uploaded_file is not None:
    if uploaded_file.name == "ViewingActivity_.csv":
        st.sidebar.subheader('3 - Analyze and chill')
    try:
        df = pd.read_csv(uploaded_file)
    except UnicodeDecodeError:
        write("You've uploaded the wrong file")
    try:
        # Drop unnecessary columns
        df = df.drop(['Attributes', 'Supplemental Video Type', 'Device Type', 'Bookmark', 'Latest Bookmark'], axis=1)
        # Remove whitespace in column names
        df.columns = [column.replace(' ', '_') for column in df.columns]
        # Change dtype to datetime
        df['Start_Time'] = pd.to_datetime(df['Start_Time'], utc=True)
        # Change dtype to timedelta
        df['Duration'] = pd.to_timedelta(df['Duration'])
        # Correct Start_Time based on the time zone in which the viewer was located
        # Check in which countries the user has watched Netflix
        # print(df['Country'].value_counts()) # uncomment here
        # Create a list of conditions for each (set of) country(ies) with different time zones
        countries = [
            (df['Country'] == 'AU (Australia)'),
            ((df['Country'] == 'BE (Belgium)') | (df['Country'] == 'US (United States)')),
            (df['Country'] == 'PT (Portugal)')
        ]
        # create a list of time zones we want to assign to each country
        timezones = ['Australia/Melbourne', 'Europe/Brussels', 'Europe/Lisbon']
        # create a new column and use np.select to assign values to it using our lists as arguments
        df['Local_Time_Zone'] = np.select(countries, timezones)
        # Convert Start_Time to its correct time zone
        df['Local_Start_Time'] = df.apply(lambda x: x['Start_Time'].tz_convert(x['Local_Time_Zone']), axis=1)
        # Remove tz awareness and convert to datetime
        df['Local_Start_Time'] = pd.to_datetime(df['Local_Start_Time'].astype("string").apply(lambda x: x[:-6]))
        # Clean df for analysis
        df = df.drop(['Start_Time', 'Local_Time_Zone'], axis=1)
        df = df[['Profile_Name', 'Local_Start_Time', 'Duration', 'Title', 'Country']]
        # Adding features for analysis
        df['Weekday'] = df['Local_Start_Time'].dt.weekday
        df['Hour'] = df['Local_Start_Time'].dt.hour
        df['Day'] = df['Local_Start_Time'].dt.day
        df['Month'] = df['Local_Start_Time'].dt.month
        df['Year'] = df['Local_Start_Time'].dt.year
        # Split title into multiple columns to generate more content-related features
        content = df['Title'].str.split(':', expand=True)
        # Create and clean new features
        for i in range(1, 6):
            content[i].fillna("", inplace=True)
        content['Episode'] = content[2] + content[3] + content[4] + content[5]
        content = content.drop([2, 3, 4, 5], axis=1)
        content.rename(columns={0: "Title_right", 1: "Season"}, inplace=True)
        #  Cleaning of new features
        content['part'] = np.where(content['Season'].str.contains('Season'), '', content['Season'])
        content['Season'] = np.where(content['Season'].str.contains('Season'), content['Season'], '')
        content['Episode'] = content['Episode'] + content['part']
        content = content.drop(['part'], axis=1)
        # Join new features with df and perform preparations for content-related analysis
        df = pd.concat([df.reset_index(drop=True), content.reset_index(drop=True)], axis=1)
        df = df.drop(['Title'], axis=1)
        df.rename({'Title_right': 'Title'}, inplace=True, axis=1)
        df = df[
            ['Profile_Name', 'Local_Start_Time', 'Duration', 'Country', 'Weekday', 'Hour', 'Day', 'Month', 'Year', 'Title',
             'Season', 'Episode']]


        ### Main Page Content ###
        profiles = df['Profile_Name'].unique()
        select_profile = st.selectbox('PICK YOUR PROFILE', profiles)
        st.markdown('#')

        for name in profiles:
            if select_profile == name:
                df = df[df['Profile_Name'] == name]
                df = df.reset_index(drop=True)
                st.subheader('First things first. The first piece of content you ever watched on this Netflix account is')
                write(df['Title'][-1:].to_string(index=False))
                write(df['Local_Start_Time'][-1:].to_string(index=False))

                scroll_down()

                start_times_by_hour = df['Hour'].value_counts().reset_index()
                st.subheader("You're most likely to be watching Netflix between ")
                write(start_times_by_hour['index'][0].astype(str) + "h and " +
                      (start_times_by_hour['index'][0] + 1).astype(str) + "h")

                scroll_down()

                st.subheader('Your favourite day of the week for watching Netflix is')
                start_times_by_day = df['Weekday'].value_counts().reset_index()
                write(calendar.day_name[start_times_by_day['index'][0]])

                scroll_down()

                morning_hours = start_times_by_hour.sort_values('index')[6:12]['Hour'].sum()
                total_hours = start_times_by_hour['Hour'].sum()
                st.subheader('Out of all the time you have spent watching Netflix, ')
                write(round(((morning_hours / total_hours) * 100), 2).astype(str) + '%')
                st.subheader(' of it occurred between 6AM and 12PM')

                scroll_down()

                st.subheader('The percentage of time spent on Netflix between 9AM and 6PM on workdays is')
                worktime = df[df['Weekday'] < 5]['Hour'].value_counts().reset_index().sort_values('index')[9:18][
                    'Hour'].sum()
                write(round(((worktime / total_hours) * 100), 2).astype(str) + '%')

                scroll_down()

                st.subheader('Your overall time spent watching Netflix since the creation of your account is ')
                overall_time_spent = df['Duration'].sum()
                write(str(overall_time_spent))

                scroll_down()

                st.subheader("Here's a breakdown of your watching time by year")
                time_spent_by_year = df.groupby('Year')['Duration'].sum().reset_index().to_string(index=False).split('\n')[
                                     1:]
                for year in time_spent_by_year:
                    write(year.strip().replace(' ', ':\t', 1))

                scroll_down()

                max_year = df['Year'].max()
                st.subheader("And here's how you're doing by month in " + str(max_year))
                time_spent_by_month_2022 = df[df['Year'] == max_year].groupby('Month')['Duration'].sum().reset_index()
                time_spent_by_month_2022['Month'] = time_spent_by_month_2022['Month'].apply(
                    lambda x: calendar.month_name[x])
                time_spent_by_month_2022 = time_spent_by_month_2022.to_string(index=False).split('\n')[1:]
                for month in time_spent_by_month_2022:
                    write(month.strip().replace(' ', ':\t', 1))

                scroll_down()

                start_date = datetime.datetime(2022, 1, 1)
                max_date = datetime.datetime.now()
                ytd_time = str(max_date - start_date).split(',')[0]
                ytd_netflix = df[df['Year'] == max_year]['Duration'].sum()
                time_spent_pct = str(round((ytd_netflix / ytd_time) * 100, 2))
                st.subheader(
                    ytd_time + ". That's the amount of time that has passed in " + str(max_year) + " up until today. "
                                                                                                   "Given that you have spent " +
                    str(ytd_netflix).split(' ', 1)[0] + " day(s) of it on "
                                                        "Netflix, you have spent")
                write(time_spent_pct + '%')
                st.subheader("of your time watching Netflix in " + str(max_year) + ".")

                scroll_down()

                pd.options.display.max_colwidth = 100
                st.subheader("Here's some information on your longest single day binge")
                single_day_binge = df.groupby(['Year', 'Month', 'Day'])['Duration'].sum().reset_index()
                single_day_binge = single_day_binge.rename(columns={"Duration": "Sum_Duration"})
                single_day_binge = pd.merge(df, single_day_binge, how='inner', left_on=['Year', 'Month', 'Day'],
                                            right_on=['Year', 'Month', 'Day'])
                # single_day_binge = single_day_binge.sort_values('Sum_Duration', ascending=False)
                max_binge_time = single_day_binge['Sum_Duration'].max()
                single_day_binge = single_day_binge[single_day_binge['Sum_Duration'] == max_binge_time]
                st.subheader('This sitting went on for')
                write(str(max_binge_time).split(' ')[-1])
                st.subheader('It started at ')
                write(single_day_binge['Local_Start_Time'].min())
                st.subheader("And ended at")
                write(single_day_binge['Local_Start_Time'].max())
                st.subheader('You started off with watching')
                write(single_day_binge['Title'][-1:].to_string(index=False) + ' -'
                      + single_day_binge['Season'][-1:].to_string(index=False)
                      + ' -' + single_day_binge['Episode'][-1:].to_string(index=False))
                st.subheader("And ended this epic session with")
                write(single_day_binge['Title'][:1].to_string(index=False) + ' -'
                      + single_day_binge['Season'][:1].to_string(index=False)
                      + ' -' + single_day_binge['Episode'][:1].to_string(index=False))

                scroll_down()

                st.subheader("These are your top 5 favourite titles, the ones that you spent most time watching")
                most_popular_titles = df.groupby(['Title'])['Duration'].sum().reset_index()
                most_popular_titles = most_popular_titles.rename(columns={"Duration": "Total_Duration"})
                most_popular_titles = most_popular_titles.sort_values(by='Total_Duration', ascending=False).reset_index(
                    drop=True)[:5]

                top_5 = [f"%s - %s" % title for title in
                         zip(most_popular_titles['Title'], most_popular_titles['Total_Duration'])]
                for i in range(len(top_5)):
                    write(str(i + 1) + '. ' + top_5[i])
    except KeyError:
        write("You've uploaded the wrong file")
    except NameError:
        write("")

hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            footer:after {
	        content:'made by jorgo haezaerts :)';
	        visibility: visible;
	        display: block;
	        position: relative;
	        #background-color: red;
	        padding: 5px;
	        bottom: 10px;
            </style>
            """
# #MainMenu {visibility: hidden;} maybe add later on
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
