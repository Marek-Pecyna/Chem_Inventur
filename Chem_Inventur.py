"""
Was soll dieses Inventur-Programm leisten?
1. Einlesen der alten Daten aus alter Inventur (Excel-Datei)
2. Erzeugen einer Datenbank im Speicher
3. Programmatisches Abfragen für jeden Eintrag in der Datenbank
    * Abfrage nach Einzelsubstanz
    * Abfrage nach Aufbewahrungsort (z.B. Regal 7)
4. Folgende Eigenschaften sollen am Ende erfasst sein (pro Produkt):
    * Name (zuerst der Hauptname, dann die Konfiguration)
        also z.B. Glucose, D-,
    * Alternativer Name 1
    * Alternativer Name 2
    * Englischer Name
    * Alter des Gebindes: Datum des Kaufes oder erste Erwähnung in der Inventur
    * Reinheitsgrad (98 %, technisch, ...)
    * Zustandsform (Pulver, Granulat, gelöst in Wasser, ...)
    * Verwendungszweck
    * Standort
    * Summenformel (falls vorhanden)
    * CAS-Nummer (falls vorhanden)
    * Gebindegröße
    * Restliche Menge
    * Hersteller
    * Artikelnummer (Bestellnummer) laut Hersteller
    * Gefahrenklasse (GHS-Piktogramm)
    * H-Sätze als Codes
    * P-Sätze als Codes
    * Link zum Sicherheitsdatenblatt im Netz oder zur Datei
    * Link zur GESTIS-Datenbank
5. Abfrage anhand der Daten in der Excel-Datei, z.B.
    * "Bitte geben Sie die Restmenge für Ethanol (2,5L Gebinde) ein:"
    * Was abgefragt wird, lege ich vorher fest, v.a. folgendes:
        - Restmenge
        - Reinheitsgrad
        - Zustandsform
        - Alternativname(n)
    * automatisch können von den Webseiten der Hersteller (v.a. Merck,
    Roth und VWR) die SDBs heruntergeladen werden
    (eigenes kleines Projekt: Webseite parsen und fernsteuern)
6. Eingabe von neuen Stoffen, die noch nicht in der Datenbank enthalten sind
7. Zwischenspeicherung in csv-Dateien (einfache Lesbarkeit und Portierbarkeit)
8. (Gedruckte) Ausgabe in Exceldatei
9. Grafische Oberfläche, um bequem nach Stoffen zu suchen
10. Anmerkungen von Chris: Ablaufdatum anzeigen, Anzeige der Einträge filtern
"""
""" Chemikalien-Inventur

make a complete standalone app with:
"pyinstaller .\\Chem-Inventur.spec"

making a one-folder-app with Nuitka
nuitka --follow-imports --standalone --enable-plugin=tk-inter .\\Chem-Inventur.py

making onefile app with Nuitka:
nuitka --onefile --enable-plugin=tk-inter .\\Chem-Inventur.py

nuitka --onefile --enable-plugin=tk-inter --include-data-files=.\\*.csv=.\\ .\\Chem-Inventur.py

nuitka --onefile --enable-plugin=tk-inter --include-data-files=.\\*.csv=.\\ --disable-console .\\Chem-Inventur.py
"""

import tkinter as tk
from Constants import PROGRAM, VERSION
from View import View
from Model import Model
from Controller import Controller

if __name__ == '__main__':
    main_app = tk.Tk()
    main_app.title(f'{PROGRAM} (Version {VERSION})')
    main_app.configure(bg='lightblue')
    main_app.minsize(width=500, height=500)
    view = View(parent=main_app)
    view.pack(fill="both", expand=True, padx=10, pady=5)

    model = Model(primary_key='Key')

    controller = Controller(main_app, model, view)
    main_app.mainloop()


