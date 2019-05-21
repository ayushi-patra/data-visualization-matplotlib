# --------------

import pandas as pd 
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Load the dataset and create column `year` which stores the year in which match was played

df = pd.read_csv(path)
df['date'] = pd.to_datetime(df['date'])
df['year']= df['date'].dt.year.values

# Plot the wins gained by teams across all seasons 
df_winners = df.drop_duplicates(['winner', 'year', 'match_code'])

total_wins = df_winners['winner'].value_counts().plot(kind='bar')
total_wins.set_xlabel('Winners') 
total_wins.set_ylabel('Number of Matches Won by Each Team') 
plt.show()

# Plot Number of matches played by each team through all seasons
team_list = df_winners.groupby('team1').groups.keys() 

 # New dataframe for teams which appears either in the team1 or team2 
df_team = pd.DataFrame(columns=('team', 'matches'), index=range(len(team_list)))
 
 # To identify teams in both team1 and team2 and placing them in new dataframe
for n, team in enumerate(team_list):
    n_matches = df_winners[(df_winners['team1'] == team) | (df_winners['team2'] == team)]['match_code'].shape[0] 
    df_team.loc[n] = [team, n_matches] 

print('Number of matches played by each team through all seasons \n{}'.format(df_team.sort_values('matches', ascending=False))) 

df_team.sort_values('matches', ascending=False).plot(kind='bar') 
plt.xlabel('IPL Teams') 
plt.ylabel('Number of Matches Won across all seasons')
plt.xticks(range(len(team_list)), ['MI', 'RCB', 'KXP', 'DD', 'KKR', 'CSK', 'RR', 'DC', 'SH', 'PW', 'GL', 'KTK', 'RPS'], rotation=0) 
plt.show() 

# Top bowlers through all seasons
valid_wicket_kind = ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled', 'hit wicket']

df_wickets = df[df['wicket_kind'].isin(valid_wicket_kind)]

ax2 = df_wickets.groupby(['bowler'])['wicket_kind'].count().sort_values(ascending=False).to_frame().reset_index().head(10) 
print('Top Bowlers through all seasons are {}'.format(ax2['bowler'].values.tolist())) 
ax2.plot(x='bowler', kind='bar', color = 'c', legend=False) 
plt.xlabel('Bowlers')
plt.ylabel('Number of Wickets taken by each bowler across all seasons')
plt.show()

# How did the different pitches behave? What was the average score for each stadium?

total_score_for_each_stadium = df.groupby(['venue'])['total'].agg('sum').to_frame() 
column = total_score_for_each_stadium.columns = ['runs']
column_index = total_score_for_each_stadium.reset_index()
print('The behavior of pitches based on runs are {}'.format(column_index.sort_values('runs', ascending=False))) 

number_of_matches_played_venue = df.groupby('venue')['total'].agg('count').to_frame()

number_of_matches_played_venue.columns = ['matches']
number_of_matches_played_venue.reset_index()

df_merged = total_score_for_each_stadium.merge(number_of_matches_played_venue, on=['venue']).reset_index()
df_merged['avg_runs'] = df_merged['runs']/df_merged['matches']
print(f'Average Score for each Stadium are \n {df_merged}') 

# Types of Dismissal and how often they occur

dismissal_types = df['wicket_kind'].value_counts()
print(f'Type of Dismissal are listed as follows\n {dismissal_types}') 

dismissal_types.plot.bar(legend=True)
plt.xlabel('Dismissal Types')
plt.ylabel('Count') 
plt.show()

# Plot no. of boundaries across IPL seasons

grouped_runs = df.groupby('runs')['runs'].count().to_frame().rename(columns={'runs':'counts'}).reset_index() 
boundaries_count = grouped_runs[(grouped_runs['runs'] == 4) | (grouped_runs['runs'] == 6)] 
total_boundaries_count = boundaries_count['counts'].agg('sum')
boundaries_count.plot(x='runs', y='counts', kind='bar', rot=0, legend=False)
plt.xlabel('Boundaries across IPL seasons')
plt.ylabel('Boundaries Count') 
plt.show()

# Average statistics across all seasons

matches_per_season = df_winners.groupby('year')['match_code'].count()
bowls_per_match_per_season = df.groupby(['year', 'match_code'])['delivery'].sum().groupby('year').mean()
runs_per_match_per_season = df.groupby(['year', 'match_code'])['runs'].sum().groupby('year').mean()
runs_per_bowl_per_season = df.groupby(['year', 'match_code', 'delivery'])['runs'].sum().groupby('year').mean()

bowls_per_match_per_season.plot.bar(rot = 0)
plt.xlabel('Bowls per match per season')
plt.ylabel('Bowls Count') 
plt.show()

runs_per_match_per_season.plot.bar(rot=0)
plt.xlabel('Runs per match per season')
plt.ylabel('Runs Count') 
plt.show()

runs_per_bowl_per_season.plot.bar(rot=0)
plt.xlabel('Runs per match per season')
plt.ylabel('Runs Count') 
plt.show()



