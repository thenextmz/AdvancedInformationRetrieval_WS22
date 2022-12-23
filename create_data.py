import pandas as pd
df_lyrics = pd.read_csv("data/lyrics-data.csv",dtype=str)
df_artist = pd.read_csv("data/artists-data.csv")

df_lyrics= df_lyrics.loc[df_lyrics.language=="en"]
df_artist = df_artist.rename(columns={"Link":"ALink"})
df_all =pd.merge(df_lyrics,df_artist,on="ALink")

# split genres
artists = df_all.ALink.unique()
artist_dict = {}
df_genre = pd.DataFrame({"ALink":[],"genre":[]})
for a in artists:
    artist_genres = []
    alink = []
    dftmp = df_all.loc[df_all.ALink == a]
    genres = dftmp.Genres.values[0]
    g_list = str(genres).split(";")
    for genre in g_list:
        genre = genre.strip()
        artist_genres.append(genre)
        alink.append(a)
    artist_dict[a] = artist_genres
    df_genre= df_genre.append(pd.DataFrame({"ALink":alink,"genre":artist_genres}),ignore_index=True)

df_all =pd.merge(df_all,df_genre,on="ALink")
df_all.to_csv("data/merged_cleaned_data.csv",index=False)
sel_genres = ["Romântico","Country","Gospel/Religioso","Hardcore","Heavy Metal","Rap"]
# sel_genres = ["Rap"]


df_genre = df_all.loc[df_all.genre.isin(sel_genres)]
len_before= len(df_genre)
df_genre = df_genre.drop_duplicates(subset=["SLink"],keep=False)#
print(f"Dropped {len_before-len(df_genre)} duplicates")
df_genre.to_csv("data/selected_genres.csv",index=False)