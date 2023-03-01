import os

# switch between reading old Excel file and reading from csv file
excel_is_parsed = True

PATH = r'C:\Users\Marek\PycharmProjects\Chemikalien_Inventur_2.0'
CSVFILE = r'In_Bearbeitung_Inventur.csv'
DATAFILE = r'Inventur_data'


class Controller:

    def __init__(self):
        text = f'{__name__}: Controller wird initiiert.'
        print("*" * len(text))
        print(text)
        self.view = None
        self.model = None
        self.filename = os.path.join(PATH, CSVFILE)
        print(f'{__name__}: Dateiname der CSV-Datei: {self.filename}')
        self.primary_key = 'Key'
        self.is_analysis_finished = False
        self.key_value_list = []
        self.actual_key = None
        self.key_value_list = []

        # Options for view
        self.open_in_excel = True
        self.show_autofilter = False
        return

    def set_model(self, model):
        self.model = model
        self.model.get_data_from_csv_file(filename=self.filename, primary_key=self.primary_key)

    def set_view(self, view):
        """ This function prepares the GUI in a useful state for first usage """
        self.view = view
        # Fill data in Viewer
        # Get a list with all primary keys
        self.key_value_list = [item for item in self.model.database]
        self.view.fill_gui_with_data(database=self.model.database,
                                     fieldnames=self.model.fieldnames)
        self.actual_key = 0
        self.update_fields()
        self.view.forward_button['command'] = self.next_key
        self.view.back_button['command'] = self.previous_key
        self.view.save_button['command'] = self.save_data_to_file
        print(f'{__name__}: GUI ist jetzt konfiguriert für die erste Benutzung.')
        return

    def previous_key(self):
        if self.actual_key is None or self.key_value_list == []:
            return
        self.save_fields()
        if self.actual_key > 0:
            self.actual_key -= 1
        elif self.actual_key == 0:
            self.actual_key = len(self.model.database) - 1  # set to last item

        self.view.actual_value_of_category_variable.set(self.key_value_list[self.actual_key])
        self.update_fields()

    def next_key(self):
        if self.actual_key is None or self.key_value_list == []:
            return
        # self.save_fields()
        if self.actual_key < len(self.model.database)-1:
            self.actual_key += 1
        elif self.actual_key == len(self.model.database)-1:
            self.actual_key = 0

        self.view.actual_value_of_category_variable.set(self.key_value_list[self.actual_key])
        self.update_fields()

    def update_fields(self):
        key_in_database = self.key_value_list[self.actual_key]
        self.view.actual_value_of_category_variable.set(key_in_database)
        data_entry = self.model.database[key_in_database].values()
        for index, item in enumerate(data_entry):
            self.view.textvariable_list[index].set(item)

    def save_fields(self):
        key_in_database = self.key_value_list[self.actual_key]
        for index, item in enumerate(self.model.database[key_in_database]):
            self.model.database[key_in_database][item] = self.view.textvariable_list[index].get()
        return

    def update_gui(self):
        """ This function implements all the logic and behaviour of GUI """
        pass
        return

    def save_data_to_file(self):  # TODO: Korrektes Abspeichern!
        self.save_fields()
        save_filename = self.view.ask_save_filename()
        if save_filename != "":
            self.model.save_csv_file(save_filename, self.model.database)


if __name__ == '__main__':
    """Module testing"""
    print(f'Testing module "{__file__}"')

    # Testing View-Handling without a view and model
    # from tkinter import filedialog
    # controller = Controller()
    # controller.filename_measurements_XML = filedialog.askopenfilename(title='XML-Datei auswählen')
    # excel_file = os.path.realpath(filedialog.askopenfilename(title='Gerätedatei auswählen'))
    # save_dir = filedialog.askdirectory(title='Speicherverzeichnis auswählen')
    # controller.save_directory = os.path.split(controller.filename_measurements_XML)[0]
    # controller.get_device_filename()
    # assert excel_file == controller.filename_devices_excel, "Excel-Filenamen wurde nicht automatisch erkannt!"
    # assert save_dir == controller.save_directory, "Save-Directory stimmt nicht überein!"
    # print('All file names present?', controller.filenames_are_complete())
    # controller.start_button_pressed()
    # for var in vars(controller):
    #    print(f'{var:_<40}{repr(vars(controller)[var])}')

    # Testing View-Handling with a specific view
    from View import View
    from Constants import PROGRAM, VERSION
    import tkinter as tk
    root = tk.Tk()
    root.title(f'Modultest für "{__file__}": {PROGRAM} (Version {VERSION})')
    v = View(parent=root)  # Start specific view
    v.pack(fill='both', expand=True, padx=10, pady=5)
    c = Controller()
    c.set_view(v)  # GUI is changed by controller
    c.update_gui()
    root.mainloop()
    for var in vars(c):
        print(f'{var:_<40}{repr(vars(c)[var])}')
