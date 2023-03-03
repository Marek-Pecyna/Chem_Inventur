from Constants import PROGRAM, VERSION
from datetime import date

class Controller:

    def __init__(self, parent, model, view):
        text = f'{__name__}: Controller wird initiiert.'
        print("*" * len(text))
        print(text)
        self.parent = parent
        self.model = model
        self.view = view
        self.filename = None
        self.category = None
        self.subcategory = None
        self.is_analysis_finished = False
        self.keys_to_display_list = []
        self.actual_key = 1
        self.view.file_menu.entryconfig(0, command=self.open_csv_file)
        self.view.file_menu.entryconfig(2, command=self.quit_program)

        # Options for view
        self.open_in_excel = True
        self.show_autofilter = False
        if self.model.database:
            self.set_view()
        return

    def set_model(self, model):
        self.model = model

    def set_view(self):
        """ This function prepares the GUI in a useful state for first usage """
        # Fill data in Viewer
        # Get a list with all primary keys
        self.keys_to_display_list = [item for item in self.model.database]
        self.view.fill_gui_with_data(fieldnames=self.model.column_names,
                                     primary_key=self.model.primary_key,
                                     extra_category='Alle Chemikalien')
        self.view.combobox_category.bind('<<ComboboxSelected>>', self.category_changed)
        self.view.combobox_subcategory.bind('<<ComboboxSelected>>', self.subcategory_changed)
        self.view.combobox_subcategory['state'] = 'disabled'
        self.view.forward_button['command'] = self.next_key
        self.view.back_button['command'] = self.previous_key
        self.view.save_button['command'] = self.save_data_to_file
        self.view.new_entry_button['command'] = self.create_new_entry
        self.view.delete_entry_button['command'] = self.delete_entry
        self.actual_key = 1
        self.update_fields()
        print(f'{__name__}: GUI ist jetzt konfiguriert für die erste Benutzung.')
        return

    def category_changed(self, event):
        self.save_fields()
        self.category = self.view.combobox_category.get()
        # find all entries with this category
        sub_category_list = []
        for key in self.model.database:
            for item in self.model.database[key]:
                if item == self.category:
                    # filling key_value_list
                    sub_category_list.append(self.model.database[key][item])
                    break
        sub_category_list = sorted(set(sub_category_list))  # keep only unique elements
        self.view.combobox_subcategory['values'] = sub_category_list
        if len(sub_category_list) > 1:
            self.view.current_subcategory_variable.set(sub_category_list[0])
            self.view.combobox_subcategory['state'] = 'readonly'
        elif len(sub_category_list) == 1:
            self.view.current_subcategory_variable.set(sub_category_list[0])
            self.view.combobox_subcategory['state'] = 'disabled'
        else:
            self.view.current_subcategory_variable.set('Keine Unterkategorie')
        self.subcategory_changed(event=None)
        return

    def subcategory_changed(self, event):
        self.save_fields()
        self.subcategory = self.view.combobox_subcategory.get()
        if self.subcategory == 'Keine Unterkategorie':
            self.subcategory = None
            self.view.combobox_subcategory['state'] = 'disabled'
            self.view.current_subcategory_variable.set('')
            self.actual_key = 1
            self.keys_to_display_list = [item for item in self.model.database]
            self.update_fields()
            return
        # display only chemicals with this sub_category, e.g. Standort=='A2'
        self.keys_to_display_list = []
        for key in self.model.database:
            subcategory = self.model.database[key][self.category]
            if subcategory == self.subcategory:
                self.keys_to_display_list.append(key)
        self.actual_key = self.keys_to_display_list[0]
        print(self.actual_key, self.keys_to_display_list)
        self.update_fields()
        return

    def previous_key(self):
        self.save_fields()
        position = self.keys_to_display_list.index(self.actual_key) + 1  # add 1 to get keys from 1-301
        if position == 1:
            self.actual_key = self.keys_to_display_list[-1]  # letztes Element der Liste auswählen
        else:
            self.actual_key = self.keys_to_display_list[position-2]
        self.update_fields()

    def next_key(self):
        self.save_fields()
        position = self.keys_to_display_list.index(self.actual_key) + 1  # add 1 to get keys from 1-301
        if position == len(self.keys_to_display_list):
            self.actual_key = self.keys_to_display_list[0]  # erstes Element der Liste auswählen
        else:
            self.actual_key = self.keys_to_display_list[position]
        self.update_fields()

    def update_fields(self):
        if self.subcategory:
            text = f"{self.model.database[self.actual_key]['Name']}"
            self.view.actual_value_of_category_variable.set(text)
        else:
            self.view.actual_value_of_category_variable.set(self.actual_key)
        self.view.number_of_chemicals_variable.set(
            f" Chemikalie {self.keys_to_display_list.index(self.actual_key) + 1} von {len(self.keys_to_display_list)}")
        data_entry = self.model.database[self.actual_key].values()
        for index, item in enumerate(data_entry):
            self.view.text_variable_list[index].set(item)

    def save_fields(self):
        for index, column in enumerate(self.model.column_names):
            self.model.database[self.actual_key][column] = self.view.text_variable_list[index].get()
        return

    def save_data_to_file(self):
        self.save_fields()
        save_filename = self.view.ask_save_filename()
        if save_filename != "":
            self.model.save_csv_file(save_filename, self.model.database)
        return

    def open_csv_file(self):
        csv_filename = self.view.ask_open_filename()
        if csv_filename != "":
            self.model.get_data_from_csv_file(csv_filename, primary_key=self.model.primary_key)
            self.set_view()
            self.parent.title(f'{PROGRAM} (Version {VERSION}) {csv_filename}')
        return

    def quit_program(self):  # TODO: Test if data are changed
        self.parent.quit()

    def create_new_entry(self):
        print("Erzeugen eines neuen Eintrags")
        self.save_fields()  # save previous entry

        new_data_entry = {}
        for item in self.model.column_names:
            new_data_entry[item] = ''

        new_key = len(self.model.database)+1
        new_data_entry[self.model.primary_key] = new_key

        today = date.today()
        new_data_entry['Letzte Aktualisierung'] = today.strftime("%d.%m.%Y")
        print(new_key, new_data_entry)
        self.model.database.update({new_key: new_data_entry})

        self.category = None
        self.subcategory = None
        self.keys_to_display_list = [item for item in self.model.database]

        self.actual_key = new_key
        self.update_fields()

    def delete_entry(self):
        print("Löschen eines Eintrags")
        pass


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
    CSVFILE = r'C:\Users\Marek\Desktop\In_Bearbeitung_Inventur_02.03.2023_abend.csv'
    import tkinter as tk
    root = tk.Tk()
    root.title(f'Modultest für "{__file__}": {PROGRAM} (Version {VERSION})')
    root.minsize(width=400, height=400)
    v = View(parent=root)  # Start specific view
    v.pack(fill='both', expand=True, padx=10, pady=5)
    c = Controller(root, None, v)
    root.mainloop()
    for var in vars(c):
        print(f'{var:_<40}{repr(vars(c)[var])}')

