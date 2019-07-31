from bs4 import BeautifulSoup
from urllib import request

#print("Input the name of the artist please:")
"??? Resource temporarily unavailable..."
artist = "Drake"
artist = artist.lower()
artist_url = "https://www.azlyrics.com/"+artist[0]+"/"+artist+".html"
print(artist_url)
songs_urls = []

with request.urlopen(artist_url) as artists_html:
    artists_songs = BeautifulSoup(artists_html.read().decode('utf-8'), 'html.parser')
    albums_list = artists_songs.find('div', {"id":"listAlbum"})
    for a in albums_list.find_all('a', href=True):
        songs_urls.append(a['href'].replace('..', "https://www.azlyrics.com"))

count = 0
past_start = False
for song_url in songs_urls:
    print(count/len(songs_urls))
    past_start = song_url == 'https://www.azlyrics.com/lyrics/drake/ownit.html'
    if(past_start):
        with request.urlopen(song_url) as lyric_page:
             song_soup = BeautifulSoup(lyric_page.read().decode('utf-8'), 'html.parser')
             for div in song_soup.find_all('div'):
                 if not div.has_attr('class'):
                     with open('song_lyrics.txt', 'a+') as lyrics:
                         lyrics.write(div.get_text().lower())
    count += 1
