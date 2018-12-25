### Parse the html file

import urllib.request
from bs4 import BeautifulSoup
from collections import OrderedDict
import json
import csv


csvfile = open('top_spotify.csv', 'rt', encoding = 'utf-8')
jsonfile = open('top_spotify.json', 'w')

fieldnames = ("id","name","artist", "danceability","energy","key","loudness","mode","speechiness","acousticness","instrumentalness","liveness","valence","tempo","duration_ms","time_signature")
reader = csv.DictReader( csvfile, fieldnames)
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write('\n')