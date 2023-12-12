# Wordles lösen
#### 🇺🇸🇬🇧 *Englisch und Deutsch* 🇩🇪🇦🇹🇨🇭


Jedes Wordle besteht aus einem Wort mit 5 Buchstaben. Dazu hat man in der Regel 6 Versuche, dieses Wort zu erraten.
Der Wordle-Solver hilft dabei das gesuchte Wort zu finden, indem er anhand der Suchkriterien eine Liste mit passenden Wörtern der ausgewählten Sprache vorschlägt.

## Installation
1. Portable App aus den [Releases](https://github.com/marcbeat/wordle-solver/releases) herunterladen
2. `.zip` entpacken
3. App starten

## Benutzung
### Grafische Oberfläche
In die 5 oberen Textfelder ("Richtige Stelle:") können jeweils ein richtiger Buchstabe an der richtigen Stelle eingetragen werden (im Wordle meist grün markiert).
D. h. fängt das gesuchte Wort z. B. mit "A" an, wird in Textfeld 1 ein "a" eingetragen.

In die darunter liegenden 5 Textfelder werden vorkommende Buchstaben, die an der falschen Stelle eingegeben wurden (im Wordle meist gelb markiert), eingetragen.

In das Textfeld "Ausgeschlossen" werden alle Buchstaben ohne irgendwelche Trennzeichen aneinandergereiht eingetragen.

Bsp.: Angenommen das Wort "LAMPE" wurde als erstes ausprobiert. Das "a" wird gelb markiert, kommt also im Wort vor, befindet sich aber nicht an 2. Stelle. Das "p" wird grün markiert, befindet sich also bereits an der richtigen Stelle 4. Die restlicehn Buchstaben sind grau hinterlegt, also nicht im Wort vorhanden.

Das bedeutet:
- Bei "Richtiger Stelle: " wird ein "p" im 4. Textfeld eingetragen,
- bei "Falscher Stelle: " wird ein "a" im 2. Textfeld eingetragen,
- bei "Ausgeschlossen: " wird "lme" eingetragen,
- ein neues Wort wird aus der Liste ausgewählt und im Wordle ausprobiert,
- danach wird alles wiederholt.

### Start
Zunächst wird immer das Wort "Adieu" angezeigt. Durch die vielen enthaltenen Vokale ist dies ein ideales Startwort ins Wordle.

Danach können nach und nach die ausgeschlossenen und richtigen Buchstaben eingetragen werden. Die Liste mit Vorschlägen für passende Wörter wird immer weiter eingeschränkt.

## Entwicklung
Zur Entwicklung werden keine externen Pakete benötigt.

## Building
Zum Builden und Packagen der App wurde [PyInstaller](https://pyinstaller.org/en/stable/index.html) verwendet.
Dazu zunächst PyInstaller zum Repo hinzufügen:
```shell
pip install -U pyinstaller
```

Anschließend die ausführbaren Dateien erstellen:
**Windows**
```shell
pyinstaller  main.py -n "Wordle Solver" --noconfirm -w --onefile --add-data=./dict_de.json:. --add-data=./dict_en.json:. --add-data=./icon.png:. --icon=icon.ico
```
**macOS**
```shell
pyinstaller  main.py -n "Wordle Solver" --noconfirm -w --onefile --add-data=./dict_de.json:. --add-data=./dict_en.json:.  --add-data=./icon.png:. --icon=icon.icns
```


**Nicht vergessen**: Im selben Verzeichnis wie die ausführbare Datei muss die Wörterbuch-Datei `dict.json` liegen.