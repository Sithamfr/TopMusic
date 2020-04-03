import requests
import json
import re
import pandas as pd



def get_img(url):
	page = requests.get(url)
	body = page.text
	motif1 = re.compile("id=\"naboo_artist_image\".*/>")
	select = motif1.findall(body)[0]
	motif2 = re.compile("http.*jpg")
	select = motif2.findall(select)[0]
	return select


def recup_podium(url):
	""" RECUPERATION PLAYLIST ID """
	page = requests.get(url)
	body = page.text

	motif = re.compile("<script>window.__DZR_APP_STATE__.*</script>")
	js = motif.findall(body)[0][35:-9]
	js = json.loads(js)

	""" RECUPERATION TRACKS API """
	id_playlist = int(js["DATA"]["USER"]["LOVEDTRACKS_ID"])
	path_api = f"https://api.deezer.com/playlist/{id_playlist}"
	page = requests.get(path_api)
	body = json.loads(page.text)

	js = body['tracks']['data']
	artists = []
	links = []
	previews = []
	for track in js:
		artists.append(track['artist']['name'])
		links.append(track['artist']['link'])
		previews.append(track['preview'])

	artists_unique = list(set(artists))
	L = []
	for a in artists_unique:
		L.append([links[artists.index(a)],previews[artists.index(a)],a,artists.count(a)])

	df = pd.DataFrame(L)
	df.columns = ["Link","Preview","Artiste","N_tracks"]
	df.sort_values(by=['N_tracks'], inplace=True, ascending=False)

	T = sorted(list(set(df.N_tracks)), reverse=True)[:3]
	L = []
	P = []
	for i in T:
		P.append(list(df[df.N_tracks==i].Artiste))
		L.append(list(df[df.N_tracks==i].Link))

	imgs = []
	for lst in L:
		x = []
		for l in lst:
			x.append(get_img(l))
		imgs.append(x)

	return (P,T,imgs,df)
