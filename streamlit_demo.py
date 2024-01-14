import streamlit as st
import pandas as pd
import plotly.express as px


# Defining CSV file names with scraped data
epl_teams_csv = "full_data.csv"
img_teams_csv = "imgurls.csv"
update_teams_csv = "2023_matches.csv"
end_standings_csv = "end_tables.csv"
current_standings_csv = "fresh_table.csv"

# Loading data from CSV files into dataframes
epl_teams_df = pd.read_csv(epl_teams_csv)
img_teams_df = pd.read_csv(img_teams_csv)
update_teams_df = pd.read_csv(update_teams_csv)
end_standings = pd.read_csv(end_standings_csv)
current_standings = pd.read_csv(current_standings_csv)

# Data Cleaning and Transformation:
epl_teams_df = pd.concat([update_teams_df, epl_teams_df], ignore_index=True)
epl_teams_df = epl_teams_df.drop_duplicates(subset=["team", "date"], keep="first")
epl_teams_df['season'] = epl_teams_df['season'].astype(str)

epl_teams_df['secondpartseason'] = (epl_teams_df['season'].str[-2:].astype(int) + 1).astype(str)
epl_teams_df['season'] = epl_teams_df['season'] + '/' + epl_teams_df['secondpartseason']
epl_teams_df = pd.merge(epl_teams_df, img_teams_df, on="team", how="left")

# Calculate points gathered each matchweek.
epl_teams_df['points_added'] = epl_teams_df['result'].map({'W': 3, 'D': 1}).fillna(0)
# Concatenate and clean up the standings DataFrame.
epl_teams_standings = pd.concat([end_standings, current_standings], ignore_index=True)
epl_teams_standings = epl_teams_standings.rename(columns={'Season': 'season'})
epl_teams_standings['season'] = epl_teams_standings['season'].str.replace(' ', '')
epl_teams_standings['season'] = epl_teams_standings['season'].str.replace(',', '')
# Rename columns, clean team names, and merge with the main DataFrame.
epl_teams_standings.rename(columns={'Squad': 'team'}, inplace=True)
epl_teams_standings['team'] = epl_teams_standings['team'].str.replace('Utd', 'United').str.replace("Nottingham Forest", "Nott'ham Forest").str.replace("West Brom", "West Bromwich Albion").str.replace("Tottenham", "Tottenham Hotspur")
epl_teams_df = pd.merge(epl_teams_standings, epl_teams_df, on=['season', 'team'], how='right')

#Defining URLs for icons used in the dashboard 
goal_img = "https://th.bing.com/th/id/OIP.z0AsMeV8Ihpi-VYoos-_HQAAAA?rs=1&pid=ImgDetMain"
prem_img = "https://th.bing.com/th/id/OIP.0kVszlE6KlGBYZFrH_q7mQHaEK?rs=1&pid=ImgDetMain"
xg_img = "https://th.bing.com/th/id/OIP.C5gn6IJnBKmcKeWJriBLqQHaHw?w=920&h=963&rs=1&pid=ImgDetMain"
xga_img = "https://cdn0.iconfinder.com/data/icons/business-analytics-5/96/Picture19-512.png"


# Function to filter the EPL teams DataFrame based on selected team and season.
# If a specific team is selected, filter rows accordingly.
# If a specific season (other than 'All seasons') is selected, filter rows based on the season.
# Returns the filtered DataFrame.
def filter_team(selected_team, selected_season):
    filtered_teams = epl_teams_df.copy()

    if selected_team:
        filtered_teams = filtered_teams[filtered_teams['team'] == selected_team]

    if selected_season and selected_season != 'All seasons':
        filtered_teams = filtered_teams[filtered_teams['season'] == selected_season]

    return filtered_teams

# Function to process and format standing data from a team DataFrame.
# Extracts position and converts it to a human-readable format.
# Determines an appropriate image URL based on the team's position.
# Extracts total points and points per match for further use.
def standing_data(team_df):

    position = team_df['Rk'].astype(int).iloc[0]

    if position == 1:
        position_str = '1st'
    elif position == 2:
        position_str = '2nd'
    elif position == 3:
        position_str = '3rd'
    else:
        position_str = f'{position}th'

    points = team_df['Pts'].astype(int).iloc[0]
    points_per_match = team_df['Pts/MP'].iloc[0]

    # Display tiles for goals scored and goals conceded
    col1, col2, col3, = st.columns(3)
    col1.metric('Position', position_str)
    col2.metric('Points', points)
    col3.metric("Points per Match", points_per_match)


# Function to create a scatter plot and calculate the correlation coefficient
def correelation_pass_poss(team_df):

    # Scatter plot with correlation coefficient
    fig = px.scatter(
        team_df,
        x='cmp%',
        y='poss',
        title='Correlation between Successful Passes and Possession',
        labels={'cmp%': 'Successful Passes Percentage', 'poss': 'Possession Percentage'},
        trendline='ols',  # Ordinary Least Squares regression line
    )

    # Show the plot
    st.plotly_chart(fig)
    
# Function to create a scatter plot and calculate the correlation coefficient
def correlation_goals_cmp(team_df): 
    # Scatter plot with correlation coefficient
    fig = px.scatter(
        team_df,
        x='cmp%',
        y='gf',
        title='Correlation between Goals Scored and Passes Completed',
        labels={'cmp%': 'Succesfull Passes Percentage', 'gf': 'Goals Scored'},
        trendline='ols',  # Ordinary Least Squares regression line
    )

    # Show the plot in Streamlit app
    st.plotly_chart(fig)
    
# Function to create a scatter plot and calculate the correlation coefficient
def correlation_goals_xg(team_df):
    # Scatter plot with correlation coefficient
    fig = px.scatter(
        team_df,
        x='xg',
        y='gf',
        title='Correlation between Expected Goals (xG) and Goals Scored',
        labels={'xg': 'Expected Goals', 'gf': 'Goals Scored'},
        trendline='ols',  # Ordinary Least Squares regression line
    )
    st.plotly_chart(fig)
    
# Function to create a scatter plot and calculate the correlation coefficient
def correlation_poss_ga(team_df):
    # Scatter plot with correlation coefficient
    fig = px.scatter(
        team_df,
        x='poss',
        y='ga',
        title='Correlation between Possesion (%) and Goals Conceded',
        labels={'poss': 'Possesion (%)', 'ga': 'Goals Conceded'},
        trendline='ols',  # Ordinary Least Squares regression line
    )
    st.plotly_chart(fig)

# Function to create a scatter plot and calculate the correlation coefficient
def correlation_poss_gf(team_df):
    # Scatter plot with correlation coefficient
    fig = px.scatter(
        team_df,
        x='poss',
        y='gf',
        title='Correlation between Possesion (%) and Goals Scored',
        labels={'poss': 'Possesion (%)', 'gf': 'Goals Scored'},
        trendline='ols',  # Ordinary Least Squares regression line
    )
    st.plotly_chart(fig)



# Function to create a dashboard using Streamlit for a given team DataFrame.
# Display basic statistics, including total goals scored, total goals conceded, expected goals (xG), and expected goals conceded (xGA).
# Display a stacked horizontal bar chart comparing average possession and average opponent possession.
# Uses Plotly Express library for visualization with custom colors and formatting.
# Display a pie chart illustrating the percentage of successful and unsuccessful passes.
# Uses Plotly Express library for visualization with a hole in the center for improved clarity.
def create_dashboard(team_df):

    st.subheader(f'Basic Stats')

    # Calculate total goals scored and total goals conceded
    goals_scored = team_df['gf'].astype(int).sum()
    goals_conceded = team_df['ga'].astype(int).sum()

    xg = team_df['xG'].iloc[0]
    xga = team_df['xGA'].iloc[0]

    # Display tiles for goals scored and goals conceded
    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Goals Scored', goals_scored)
    col2.image(goal_img, width=80)
    col3.metric('Goals Conceded', goals_conceded)
    col4.image(goal_img, width=80)
    
    # Add new columns
    new_column1 = col1.metric('Expect Goals', xg)
    new_column2 = col2.image(xg_img, width=80)
    new_column3 = col3.metric('Expected Goals Conceded', xga)
    new_column4 = col4.image(xg_img, width=80)

    st.subheader(f'Dashboard for {team_df["team"].iloc[0]} in {team_df["season"].iloc[0]}')

    # Calculate mean for "cmp%" column
    pass_success = team_df['cmp%'].mean()
    pass_failure = 100 - pass_success

    #Calculate mean for possesion
    Teamposs = team_df['poss'].mean()
    Opponentposs = 100 - Teamposs

    goals_scored = team_df['gf'].sum()
    goals_conceded = team_df['ga'].sum()


    data = pd.DataFrame({
        'Metric': ['Possession'],
        'Team Possession': [Teamposs],
        'Opponent Possession': [Opponentposs]
    })

    # Create a stacked horizontal bar chart
    fig = px.bar(
        data,
        x=['Team Possession', 'Opponent Possession'],
        y='Metric',
        orientation='h',
        labels={'value': 'Possession Percentage'},
        title='Average Possession vs Average Opponent Possession',
        color_discrete_map={'Team Possession': 'blue', 'Opponent Possession': 'red'},
        height=250  # Adjust the height as needed
          # Adjust the width as needed
    )

    fig.update_traces(texttemplate='%{x:.2f}%', textposition='inside')
    fig.update_yaxes(showticklabels=False)
    # Remove legend label "index" from the left side
    fig.update_layout(legend=dict(title=''))
    fig.update_layout(legend=dict(title=''))





    # Show the chart
    st.plotly_chart(fig)


    # Create a DataFrame for the pie chart
    data = pd.DataFrame({
        'Type': ['Pass Successful', 'Pass Unsuccessful'],
        'Percentage': [pass_success, pass_failure]
    })

    # Create a pie chart
    fig2 = px.pie(
        data,
        names='Type',
        values='Percentage',
        title='Pass Success vs. Pass Failure',
        labels={'Percentage': ''},
        hole=0.4
    )

    # Show the chart
    st.plotly_chart(fig2)

# Function to create a dashboard for all seasons using Streamlit for a given team DataFrame.
# Display basic statistics, including total goals scored and total goals conceded.
# Utilizes Streamlit columns and metric elements for a visually appealing layout.
# Display a stacked horizontal bar chart comparing average possession and average opponent possession.
# Uses Plotly Express library for visualization with custom colors and formatting.
# Display a pie chart illustrating the percentage of successful and unsuccessful passes.
# Uses Plotly Express library for visualization with a hole in the center for improved clarity.

def create_dashboard_allseasons(team_df):

    st.subheader(f'Basic Stats')

    # Calculate total goals scored and total goals conceded
    goals_scored = team_df['gf'].astype(int).sum()
    goals_conceded = team_df['ga'].astype(int).sum()


    # Display tiles for goals scored and goals conceded
    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Goals Scored', goals_scored)
    col2.image(goal_img, width=80)
    col3.metric('Goals Conceded', goals_conceded)
    col4.image(goal_img, width=80)
    

    st.subheader(f'Dashboard for {team_df["team"].iloc[0]} (2017-2023)')

    # Calculate mean for "cmp%" column
    pass_success = team_df['cmp%'].mean()
    pass_failure = 100 - pass_success

    #Calculate mean for possesion
    Teamposs = team_df['poss'].mean()
    Opponentposs = 100 - Teamposs

    goals_scored = team_df['gf'].sum()
    goals_conceded = team_df['ga'].sum()


    data = pd.DataFrame({
        'Metric': ['Possession'],
        'Team Possession': [Teamposs],
        'Opponent Possession': [Opponentposs]
    })

    # Create a stacked horizontal bar chart
    fig = px.bar(
        data,
        x=['Team Possession', 'Opponent Possession'],
        y='Metric',
        orientation='h',
        labels={'value': 'Possession Percentage'},
        title='Average Possession vs Average Opponent Possession',
        color_discrete_map={'Team Possession': 'blue', 'Opponent Possession': 'red'},
        height=250  # Adjust the height as needed
          # Adjust the width as needed
    )

    fig.update_traces(texttemplate='%{x:.2f}%', textposition='inside')
    fig.update_yaxes(showticklabels=False)
    # Remove legend label "index" from the left side
    fig.update_layout(legend=dict(title=''))
    fig.update_layout(legend=dict(title=''))





    # Show the chart
    st.plotly_chart(fig)


    # Create a DataFrame for the pie chart
    data = pd.DataFrame({
        'Type': ['Pass Successful', 'Pass Unsuccessful'],
        'Percentage': [pass_success, pass_failure]
    })

    # Create a pie chart
    fig2 = px.pie(
        data,
        names='Type',
        values='Percentage',
        title='Pass Success vs. Pass Failure',
        labels={'Percentage': ''},
        hole=0.4
    )

    # Show the chart
    st.plotly_chart(fig2)

# Function to create a line chart representing the cumulative points for a team across matchweeks.
def create_points_chart(team_df):
    st.subheader(f'Points Chart for {team_df["team"].iloc[0]} in {team_df["season"].iloc[0]}')

    # Create a line chart for matchweek vs. cumulative points
    points_chart = px.line(
        team_df,
        x='round',
        y=team_df['points_added'].cumsum(),
        labels={'round': 'Matchweek', 'y': 'Cumulative Points'},  # Explicitly set the y-axis label
        title=f'Cumulative Points for {team_df["team"].iloc[0]}',
        )
    st.plotly_chart(points_chart)



# Function to create an indicator for the last 5 matches' results.
def create_form_indicator(team_df):
    st.subheader('Last 5 Matches')

        # Get the last 5 matches, reverse the order, and create tiles based on the result
    last_5_matches = team_df.tail(5).iloc[::-1]
        
    form_indicator_html = ""
    for _, match in last_5_matches.iterrows():
        result = match['result']
        color = 'green' if result == 'W' else 'orange' if result == 'D' else 'red'
        form_indicator_html += f'<div style="display:inline-block; background-color:{color}; color:white; width:20px; height:20px; text-align:center;">{result}</div> '

    st.markdown(form_indicator_html, unsafe_allow_html=True)


# Streamlit App - Main
def main():
    import streamlit as st
    import pandas as pd
    
    # Sidebar with team dropdown and season dropdown
    sorted_teams = sorted(epl_teams_df['team'].unique())
    selected_team = st.sidebar.selectbox('Select team', [''] + sorted_teams, format_func=lambda x: x.upper())

    unique_seasons = epl_teams_df['season'].unique()
    sorted_seasons = sorted(unique_seasons, reverse=True)
    # Create the season dropdown
    selected_season = st.sidebar.selectbox('Select season', ['All seasons'] + sorted_seasons)
    st.sidebar.text("")  # You can use st.sidebar.markdown("___") for a separator

    st.sidebar.markdown("___")

    # Custom button-like appearance
    button_html = f'<button style="width:300px; padding:8px; background-color:#4CAF50; color:white; border:none; text-align:center; text-decoration:none; display:inline-block; font-size:16px; margin-bottom:10px; cursor:pointer;" onclick="matchFinderClicked()">Match Finder <span style="font-size: 12px;">BETA</span></button>'
    

    st.sidebar.markdown(button_html, unsafe_allow_html=True)

    # Creating input fields for Match Finder

    date = st.sidebar.date_input("Select a Date", pd.to_datetime("today"))
    user_input = date.strftime("%Y%m%d")
    city_name = st.sidebar.text_input("Enter the name and country of the city (separated by comma):", "London, England")
    
    
    if st.sidebar.button("Find Matches"):

        # Import libraries an making a request to a website
        import requests
        from bs4 import BeautifulSoup
        import pandas as pd
        from datetime import datetime, timedelta
        import re
        from datetime import datetime
        import streamlit as st
        import requests
        from bs4 import BeautifulSoup
        import pandas as pd
        from datetime import datetime, timedelta
        from geopy.geocoders import Nominatim
        from geopy.distance import geodesic
        
        
        url = f'https://www.espn.in/football/fixtures/_/date/{user_input}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }
        
        page = requests.get(url, headers= headers, verify = False)
        
        if page.status_code == 200:
            st.write("Request succesfull")  # Print the content of the response
        else:
            st.write(f'Request failed with status code: {page.status_code}')

        soup = BeautifulSoup(page.text)
        table = soup.find_all('table', class_ = 'Table')

        # Initialize lists to store the rows and cells
        all_rows = []

        # Now, 'df' does not contain rows with "location" in the "Location" column
        column_names = ['Home Team', 'Away Team', 'Time', 'Location']
        mydata = pd.DataFrame(columns = column_names)

        for tabl in table:
            rows = tabl.find_all('tr')
                
            for row in rows:
                    cells = row.find_all(['td', 'th'])
                    cell_data = [cell.get_text(strip=True) for cell in cells]
                    all_rows.append(cell_data)

            column_names = ['Home Team', 'Away Team', 'Time', '4', 'Location', '6']
            df = pd.DataFrame(all_rows, columns = column_names)
            df = df[~df.apply(lambda row: row.astype(str).str.contains('location').any(), axis=1)]
            df = df.drop(columns=["4", "6"])
            df['Away Team'] = df['Away Team'].str[1:]

        time_format = '%I:%M %p'
        df['Time'] = pd.to_datetime(df['Time'], format=time_format, errors='coerce')
        df = df.dropna(subset=['Time'])
        # Subtract 1.5 hours from the datetime values (adjust the time zone to CEE)
        df['Time'] = df['Time'] - timedelta(hours=3, minutes=30)
        df['Time'] = df['Time'].dt.strftime(time_format)

        df = df.dropna(subset=['Time'])
        # Format the datetime values back to the original time format

        df[['Stadium', 'City', 'Country']] = df['Location'].str.split(',', expand=True, n=2)
        df = df.drop(columns=["Location"])
        # Reset the index of the DataFrame


        df.reset_index(drop=True, inplace=True)
        df['Location'] = df['City'] + ', ' + df['Country']

        # Drop the original "City" and "Country" columns
        df = df.drop(['City', 'Country'], axis=1)
        df = df.dropna(subset=['Location'])

        # List of countries to filter for
        endings_to_filter = ['England', 'Spain', 'Italy', 'France', 'Germany']

        # Filter the DataFrame using boolean indexing
        df = df[df['Location'].str.endswith(tuple(endings_to_filter))]



        from geopy import Nominatim
        import pandas as pd

        # Initialize the geolocator
        geolocator = Nominatim(user_agent="stadium_coordinates")

     
        # Create empty lists to store the latitude and longitude
        latitudes = []
        longitudes = []

        # Iterate through the rows of the DataFrame and geocode the stadium names
        for stadium_name in df['Location']:
            location = geolocator.geocode(stadium_name)

            if location:
                latitudes.append(location.latitude)
                longitudes.append(location.longitude)
            else:
                latitudes.append(None)
                longitudes.append(None)

        # Add the latitude and longitude columns to DataFrame
        df['Latitude'] = latitudes
        df['Longitude'] = longitudes

        from geopy import Nominatim
        from geopy.distance import geodesic
        import pandas as pd

        # Create a geolocator object
        geolocator = Nominatim(user_agent="stadium_coordinates")



        # Use geocoder to get the coordinates
        your_location = geolocator.geocode(city_name)

        data = df
        data.dropna(subset=['Latitude', 'Longitude'], inplace=True)
        # Create an empty list to store the distances
        distances = []

        # Iterate through the rows of the dataframe and calculate distances
        for index, row in data.iterrows():
            stadium_location = (row['Latitude'], row['Longitude'])
            distance = geodesic(your_location.point, stadium_location).kilometers
            distances.append(distance)

        # Add the distances column to dataframe
        data['Distance (km)'] = distances

        data_sorted = data.sort_values(by='Distance (km)')

        # Select the first 5 rows with the smallest distances
        smallest_distances = data_sorted.head(5).reset_index(drop=True).drop(columns=['Latitude', 'Longitude'])

        # Display the 5 rows with the smallest distances
        st.write(smallest_distances)    
    







    # Display filtered results and create the dashboard
    if selected_team or (selected_season and selected_season != 'All seasons'):
        filtered_results = filter_team(selected_team, selected_season)

        # Update the title dynamically based on the selected season and team
        if selected_team and selected_season and selected_season != 'All seasons':
            title = f"{selected_team} Stats ({selected_season})"
            col1, col2 = st.columns([3, 1])
            team_row = epl_teams_df[epl_teams_df["team"] == selected_team]
            img_url = team_row["cresturl"].iloc[0] if not team_row.empty else None
            col1.header(title)
            col2.image(img_url, width=100)
            standing_data(filtered_results)
            create_form_indicator(filtered_results)
            create_dashboard(filtered_results)
            create_points_chart(filtered_results)
            correelation_pass_poss(filtered_results)
            correlation_goals_cmp(filtered_results)
            correlation_poss_gf(filtered_results)
            correlation_goals_xg(filtered_results)
            correlation_poss_ga(filtered_results)
        elif selected_team:
            title = f"{selected_team} Stats (2017-2023)"
            team_row = epl_teams_df[epl_teams_df["team"] == selected_team]
            img_url = team_row["cresturl"].iloc[0] if not team_row.empty else None
            col1, col2 = st.columns([3, 1])
            col1.header(title)
            col2.image(img_url, width=100)
            create_dashboard_allseasons(filtered_results)
            correelation_pass_poss(filtered_results)
            correlation_goals_cmp(filtered_results)
            correlation_poss_gf(filtered_results)
            correlation_poss_ga(filtered_results)
            correlation_goals_xg(filtered_results)
            

        elif selected_season and selected_season != 'All seasons':
            st.header(f"{selected_season} Full Standings Table")

            epl_teams_standings_filtered = epl_teams_standings[epl_teams_standings['season'] == selected_season]
            epl_teams_standings_filtered = epl_teams_standings_filtered.iloc[:, :-4]
            epl_teams_standings_filtered = epl_teams_standings_filtered.rename(columns={'Rk': 'Position', 'team': 'Team'})

            st.write(epl_teams_standings_filtered.reset_index(drop=True))

            # Display various statistics and visualizations
            st.subheader("Statistics and Visualizations")
            

            # Goal Difference Plot
            st.write("Goal Difference Plot:")
            goal_diff_chart = px.bar(epl_teams_standings_filtered, x='Team', y='GD', title='Goal Difference')
            st.plotly_chart(goal_diff_chart)

            
            # Position vs. Points Scatter Plot
            st.write("Position vs. Points Scatter Plot:")
            scatter_plot = px.scatter(epl_teams_standings_filtered, x='Position', y='Pts', text='Team', title='Position vs. Points')
            st.plotly_chart(scatter_plot)

            # Goal For vs. Goal Against Scatter Plot
            st.write("Goal For vs. Goal Against Scatter Plot:")
            goal_scatter_plot = px.scatter(epl_teams_standings_filtered, x='GF', y='GA', text='Team', title='Goals For vs. Goals Against')
            st.plotly_chart(goal_scatter_plot)

            # Goal For vs. Expected Goals Scatter Plot
            st.write("Goals Scored vs. Expected Goals:")
            goal_scatter_plot = px.scatter(epl_teams_standings_filtered, x='xG', y='GF', text='Team', title='Goals For vs. Expected Goals')
            st.plotly_chart(goal_scatter_plot)


            # Scatter plot with correlation line
            scatter_fig = px.scatter(epl_teams_standings_filtered, x='Attendance', y='GF', trendline='ols', title='Correlation between Attendance and Goals Scored')

            # Customize the layout
            scatter_fig.update_layout(
                xaxis_title='Attendance',
                yaxis_title='Goals Scored',
            )

            # Show the scatter plot
            st.plotly_chart(scatter_fig)

    else:
        st.image(prem_img, width=100, use_column_width=True)
        st.subheader('Please select a team and/or a season.')
        

   

if __name__ == '__main__':
    main()
