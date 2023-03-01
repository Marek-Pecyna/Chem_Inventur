from openpyxl import load_workbook
import csv


class Model:
    def __init__(self):
        self.database = {}
        self.fieldnames = []

    @staticmethod
    def read_excel_file(filename: str, sheets: list) -> dict:
        """
        From an Excel file (from old stock-taking ("Inventur"))
        list of sheets will be processed
        stored in shelve

        :param filename:
        :param sheets:
        :return db:
        """

        # Load your workbook and sheets as you want, for example
        wb = load_workbook(filename)
        header = []
        db = {}  # dictionary with all data, keys = consecutive number

        for sheet in sheets:
            actual_sheet = wb[sheet]
            data = list(actual_sheet.iter_rows(values_only=True))  # read in
            print(f"   \u2022 {len(data)} Einträge mit Header")

            for index, row in enumerate(data):
                if index == 0:  # analysis of header
                    print("   \u2022 Header enthält folgende Spalten: ",
                          end="")
                    for entry in row:
                        header.append(entry)
                        print(f"{entry}", end=",")
                    print()
                else:
                    row_db = {'Name': None,
                              'Alternativer Name 1': None,
                              'Alternativer Name 2': None,
                              'Englischer Name': None,
                              'Alter des Gebindes': None,
                              'Reinheitsgrad': None,
                              'Zustandsform': None,
                              'Verwendungszweck': None,
                              'Standort': None,
                              'Summenformel': None,
                              'CAS-Nummer': None,
                              'Gebindegröße': None,
                              'Restmenge': None,
                              'Hersteller': None,
                              'Bestellnummer': None,
                              'Gefahrenklasse': None,
                              'H-Sätze': None,
                              'P-Sätze': None,
                              'Link SDB': None,
                              'Link GESTIS': None,
                              }

                    for position, entry in enumerate(row):
                        # print(header[position])
                        row_db.update({header[position]: entry})
                    db.update({index: row_db})
        return db

    def save_csv_file(self, filename: str, dialect=csv.excel):
        with open(filename, 'w', newline='', encoding='utf-16') as csvfile:
            writer = csv.writer(csvfile, dialect=dialect, delimiter=';')
            writer.writerow(self.fieldnames)
            # writing all lines
            for key in self.database:
                text = [key]
                for feature in self.database[key]:
                    text.append(self.database[key][feature])
                writer.writerow(text)
        return

    def get_data_from_csv_file(self, filename: str, primary_key, dialect=csv.excel):
        print(f'{__name__}: Analyse der CSV-Datei mit den Chemikaliendaten beginnt.')

        with open(filename, newline='', encoding='utf-16') as csv_file:
            # Create CSV reader
            csv_reader = csv.DictReader(csv_file, delimiter=';', dialect=dialect)

            # Extract fieldnames without primary key
            self.fieldnames = csv_reader.fieldnames
            print(f'{__name__}: Alle Spaltennamen: {self.fieldnames}')

            # Extract data from reader
            for row in csv_reader:
                tmp = {}
                for index, key in enumerate(row):
                    # use value as primary key
                    if key == primary_key:
                        prim_key = row[key]
                        # continue
                    tmp.update({key: row[key]})
                    # Create entry in dictionary
                # only if 'Name' is empty:
                if tmp['Name'] == "":
                    if 'Handelsname' in tmp:
                        tmp['Name'] = tmp['Handelsname']
                    else:
                        tmp['Name'] = prim_key
                self.database.update({prim_key: tmp})
        print(f'{__name__}: Analyse der CSV-Datei mit den Chemikaliendaten beendet.')
        return
