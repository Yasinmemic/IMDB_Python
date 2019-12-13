
from bs4 import BeautifulSoup
import requests
import sys
from Film import Film
sys.path.append("./Film/")

images = []
filmLinksWithId = []
filmNames = []
films = []


def getFilms(filmName):
    films = []
    filmNames = []
    filmLinksWithId = []
    images = []

    filmName = filmName.replace(" ", "+")

    source = requests.get(
        'https://www.imdb.com/find?q=' + filmName+'&ref_=nv_sr_sm')

    soup = BeautifulSoup(source.text, 'html.parser')
    i = soup.find(class_="findList")

    for j in i(class_="result_text"):
        filmNames.append(j.text)
        for k in j("a"):
            a = k['href']
            filmLinksWithId.append(a)
            source_profile = requests.get('https://www.imdb.com'+a)
            profile_resim = BeautifulSoup(source_profile.text, 'html.parser')
            profile_div = profile_resim.find(class_="poster")
            profile_img = profile_div.find("img")
            images.append(profile_img['src'])

    for i in range(len(filmNames)):
        film = Film(filmNames[i], images[i], filmLinksWithId[i])
        films.append(film)

    return films
