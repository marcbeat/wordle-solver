import json
from os import path
json_pfad_laden = path.abspath(path.join(path.dirname(__file__), 'dict_raw.json'))
json_pfad_speichern = path.abspath(path.join(path.dirname(__file__), 'dict_new.json'))

def prep_file():
    wortliste_laden = []
    with open(json_pfad_laden, 'r', encoding='utf-8') as file:
        # Initialize an empty list to store filtered data
        wortliste_laden = json.load(file)
    print("Anzahl geladen: " + str(len(wortliste_laden)))

    wortliste_speichern = []
    allowed_chars = [ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z' ]
    for wort in wortliste_laden:
        if len(wort) == 5 and all(buchstabe in allowed_chars for buchstabe in wort):
            wortliste_speichern.append(wort)

    with open(json_pfad_speichern, 'w', encoding='utf-8') as file:
        json.dump(wortliste_speichern, file)
    print ("Anzahl gespeichert: " + str(len(wortliste_speichern)))

prep_file()