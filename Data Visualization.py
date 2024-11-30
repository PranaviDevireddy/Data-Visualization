from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


url = 'https://myanimelist.net/topanime.php'
response = requests.get(url)
if response.status_code == 200:
  soup = BeautifulSoup(response.content, 'html.parser')

else:
  print('Failed to retrive web page code', response.status_code())

anime_rank = soup.find_all( 'td', "rank ac")
anime_title = soup.find_all('h3', 'fl-l fs14 fw-b anime_ranking_h3')
anime_info = soup.find_all('div', 'information di-ib mt4')
anime_episodes = []
anime_airing_dates = []
anime_members = []

for info in anime_info:
  details = list(info.stripped_strings)
  episodes_text = details[0].split()[1][1:]
  airing_dates = details[1]
  members = details[2].split()[0]
  if episodes_text == 'pecial':
    episodes_int = 1
  elif episodes_text == '?':
    episodes_int = None
  else:
    episodes_int = int(episodes_text)


  anime_episodes.append(episodes_int)
  anime_airing_dates.append(airing_dates)
  anime_members.append(int(members.replace(',', '')))

#anime directory for csv file process
anime_data = []

for rank, title, episodes, airing_dates, members in zip(anime_rank, anime_title, anime_episodes, anime_airing_dates, anime_members):
  anime_data.append({
      'Rank': rank.text.strip(),
      'Title': title.text.strip(),
      'Episodes': episodes,
      'Airing Dates': airing_dates,
      'Members': members
  })


#creating csv
csv_file = 'anime_top_50.csv'
with open(csv_file, 'w', newline='') as file:
  writer = csv.DictWriter(file, fieldnames=anime_data[0].keys())
  writer.writeheader()
  writer.writerows(anime_data)

#using pandas
df = pd.read_csv('anime_top_50.csv')
df.set_index('Rank', inplace = True)

#cleaning data
missing = df.isnull().sum()

df['Episodes'] = df['Episodes'].fillna(0)
plt.figure(figsize = (10,6))
sns.scatterplot(data=df, x=df.index, y = 'Episodes', color = 'blue')
plt.title('Anime rank vs Episodes')
plt.xlabel('Rank')
plt.ylabel('Episodes')
plt.show()

correlation = df.index.to_series().corr(df['Episodes'])
print(correlation)