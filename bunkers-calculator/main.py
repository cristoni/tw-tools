import gzip
from numpy import sqrt
import requests
import pandas as pd

pd.set_option('display.max_columns', None)

SERVER = "en133"
OUR_TRIBE = "D-ROW"
ENEMY_TRIBE = "AFK"

def scaling_min_max_normalization(df, columns):
  for column in columns:
    df[column] = (df[column] - df[column].min()) / (df[column].max() - df[column].min())

  return df

def get_file(url):
  filename = 'bunkers-calculator/data/' + url.split("/")[-1]
  out_filename = ".".join(filename.split(".")[0:-1])

  with open(filename, "wb") as f:
    r = requests.get(url)
    f.write(r.content)

  # Apri il file compresso e leggine il contenuto
  with gzip.open(filename, 'rb') as f:
    file_content = f.read()

  # Scrivi il contenuto del file su un nuovo file
  with open(out_filename, 'wb') as f:
    f.write(file_content)

  return out_filename

def get_villages_file():
  url = "http://" + SERVER + ".tribalwars.net/map/village.txt.gz"

  return get_file(url)

def get_players_file():
  url = "http://" + SERVER + ".tribalwars.net/map/player.txt.gz"

  return get_file(url)

def get_tribes_file():
  url = "http://" + SERVER + ".tribalwars.net/map/ally.txt.gz"

  return get_file(url)

def main():
  villages_file = get_villages_file()
  df_villages = pd.read_csv(villages_file, sep=",", header=None, names=["id", "name", "x", "y", "player_id", "points", "rank"])

  players_file = get_players_file()
  df_players = pd.read_csv(players_file, sep=",", header=None, names=["id", "name", "tribe_id", "villages", "points", "rank"])

  tribes_file = get_tribes_file()
  df_tribes = pd.read_csv(tribes_file, sep=",", header=None, names=["id", "name", "tag", "members", "villages", "points", "all_points", "rank"])

  df = df_villages.merge(df_players, left_on="player_id", right_on="id", how="left", suffixes=('', '_player'))
  df = df.merge(df_tribes, left_on="tribe_id", right_on="id", how="left", suffixes=('', '_tribe'))

  df_our_tribe = df.loc[df["tag"] == OUR_TRIBE]
  df_enemy_tribe = df.loc[df["tag"] == ENEMY_TRIBE]

  print(df_our_tribe.head())
  print(df_enemy_tribe.head())

  df_our_tribe = df_our_tribe.merge(df_enemy_tribe, how='cross', suffixes=('', '_enemy'))

  # add distance column equal to ipotenusa, where the catets are the difference between x and x_enemy and y and y_enemy
  df_our_tribe = df_our_tribe.assign(distance=lambda x: sqrt((x.x - x.x_enemy)**2 + (x.y - x.y_enemy)**2))
  df_our_tribe = scaling_min_max_normalization(df_our_tribe, ['distance', 'points_enemy', 'points_player_enemy'])
  df_our_tribe["score"] = (1 - df_our_tribe["distance"]) * 0.6 + df_our_tribe["points_enemy"] * 0.3 + df_our_tribe["points_player_enemy"] * 0.1
  df_our_tribe["coords"] = df_our_tribe["x"].astype(str) + "|" + df_our_tribe["y"].astype(str)


  result = df_our_tribe.groupby(['coords', 'name', 'name_player']).aggregate({'score': 'sum'}).sort_values(by=['score'], ascending=False)
  print(result.head(100))

if __name__ == "__main__":
    main()