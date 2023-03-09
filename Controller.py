from Constants import PROGRAM, VERSION
from datetime import date


class Controller:

    def __init__(self, parent, model, view):
        self.parent = parent
        self.model = model
        self.view = view

        self.category = None
        self.subcategory = None
        self.keys_to_display_list = []
        self.actual_key = None
        self.data_changed = False

        # View specific settings
        self.view.file_menu.entryconfig(0, command=self.open_csv_file)
        self.view.bind_all("<Control-o>", lambda e: self.open_csv_file())
        self.view.file_menu.entryconfig(1, command=self.open_excel_file, state='normal')
        self.view.bind_all("<Control-i>", lambda e: self.open_excel_file())
        self.view.file_menu.entryconfig(2, command=self.save_file, state='disabled')
        self.view.file_menu.entryconfig(3, command=self.save_as_new_file, state='disabled')
        self.view.file_menu.entryconfig(4, command=self.export_as_excel_file, state='disabled')
        self.view.file_menu.entryconfig(6, command=self.quit_program)
        self.parent.protocol("WM_DELETE_WINDOW", self.quit_program)

        # Options for generation of Excel file (will be implemented in future versions)
        self.open_in_excel = True
        self.show_autofilter = False
        print(f'{__name__}: Controller wurde initialisiert.')
        return

    def set_view(self):
        """ This function prepares the GUI in a useful state after opening of data file """

        self.data_changed = False
        self.parent.title(f'{PROGRAM} (Version {VERSION}) {self.model.filename}')

        # Show prepared GUI
        self.view.pack(fill="both", expand=True, padx=5, pady=5)

        # Update Menubar, 1='Import from Excel', 2='Save', 3='Save as', 4='Export to Excel' with Short-Cuts
        self.view.file_menu.entryconfig(1, state='normal')
        self.view.bind_all("<Control-i>", lambda e: self.open_excel_file())
        self.view.file_menu.entryconfig(2, state='normal')
        self.view.bind_all("<Control-s>", lambda e: self.save_file())
        self.view.file_menu.entryconfig(3, state='normal')
        self.view.bind_all("<Control-Alt-s>", lambda e: self.save_as_new_file())
        self.view.file_menu.entryconfig(4, state='normal')
        self.view.bind_all("<Control-e>", lambda e: self.export_as_excel_file())

        # Get a list with all primary keys
        self.keys_to_display_list = [key for key in self.model.database]

        # Prepare Comboboxes
        self.view.category_frame.combobox_category['state'] = 'readonly'
        self.view.category_frame.combobox_subcategory['state'] = 'disabled'
        self.view.category_frame.combobox_category.bind('<<ComboboxSelected>>', self.category_changed)
        self.view.category_frame.combobox_subcategory.bind('<<ComboboxSelected>>', self.subcategory_changed)

        # Fill Labels and Entries with data in View
        self.view.fill_gui_with_data(fieldnames=self.model.column_names,
                                     primary_key=self.model.primary_key,
                                     extra_category='Alle Chemikalien')

        # Prepare entry-fields callback, if updated
        for entry in self.view.entry_list:
            entry['validatecommand'] = self.save_fields

        # Prepare buttons
        self.view.category_frame.forward_button['command'] = self.next_key
        self.view.category_frame.back_button['command'] = self.previous_key
        self.view.button_frame.new_entry_button['command'] = self.create_new_entry
        self.view.button_frame.delete_entry_button['command'] = self.delete_entry

        for k in self.model.database: break  # get first key from database
        self.actual_key = k
        self.update_fields()
        print(f'{__name__}: GUI jetzt sichtbar und konfiguriert; erster Datensatz wird angezeigt.')
        return

    def category_changed(self, event):
        self.save_fields()
        self.category = self.view.category_frame.combobox_category.get()
        # find all entries with this category
        sub_category_list = []
        for key in self.model.database:
            for item in self.model.database[key]:
                if item == self.category:
                    # filling key_value_list
                    sub_category_list.append(self.model.database[key][item])
                    break
        sub_category_list = sorted(set(sub_category_list))  # keep only unique elements
        self.view.category_frame.combobox_subcategory['values'] = sub_category_list
        if len(sub_category_list) > 1:
            self.view.current_subcategory_variable.set(sub_category_list[0])
            self.view.category_frame.combobox_subcategory['state'] = 'readonly'
        elif len(sub_category_list) == 1:
            self.view.current_subcategory_variable.set(sub_category_list[0])
            self.view.category_frame.combobox_subcategory['state'] = 'disabled'
        else:
            # Extrakategorie ("Alle Chemikalien") hat keine Unterkategorien
            self.view.current_subcategory_variable.set('Keine Unterkategorie')
        self.subcategory_changed(event=None)
        return

    def subcategory_changed(self, event):
        self.save_fields()
        self.subcategory = self.view.category_frame.combobox_subcategory.get()

        # Bei Auswahl der Extrakategorie erfolgt eine Auswahl aller Chemikalien
        if self.subcategory == 'Keine Unterkategorie':
            self.subcategory = None
            self.view.category_frame.combobox_subcategory['state'] = 'disabled'
            self.view.current_subcategory_variable.set('')
            for k in self.model.database: break  # get first key from database
            self.actual_key = k
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
        self.view.actual_value_of_subcategory_variable.set(self.actual_key)

        if self.subcategory:
            if 'Name' in self.model.database[self.actual_key]:
                text = f"{self.model.database[self.actual_key]['Name']}"
                self.view.actual_value_of_subcategory_variable.set(text)

        self.view.number_of_subcategories_variable.set(
            f"Chemikalie {self.keys_to_display_list.index(self.actual_key) + 1} von {len(self.keys_to_display_list)}")
        data_entry = self.model.database[self.actual_key].values()
        for index, item in enumerate(data_entry):
            self.view.text_variable_list[index].set(item)

    def save_fields(self):
        for index, column in enumerate(self.model.column_names):
            temp = self.view.text_variable_list[index].get()
            if temp != self.model.database[self.actual_key][column]:
                self.data_changed = True
                self.model.database[self.actual_key][column] = temp
        return

    def open_csv_file(self):
        if self.data_changed:
            if not self.view.ask_confirm('Ungespeicherte Daten',
                                         'Daten in Ihrer aktuell geöffneten Datei sind noch nicht gespeichert. '
                                         'Fortfahren ohne zu speichern?'):
                return
        csv_filename = self.view.ask_open_csv_filename()
        if csv_filename != "":
            print(f'{__name__}: CSV-Datei öffnen.')
            print("-filename: ", csv_filename)
            print("-delimiter:", self.view.chosen_delimiter.get())
            print("-encoding: ", self.view.chosen_encoding.get())
            if self.model.database:  # if data present, reset to start conditions
                self.category = None
                self.subcategory = None
                self.keys_to_display_list = []
                self.actual_key = None
                self.model.database = {}
                self.model.column_names = []
                self.view.clear_data()
            self.model.get_data_from_csv_file(filename=csv_filename,
                                              delimiter=self.view.chosen_delimiter.get(),
                                              encoding=self.view.chosen_encoding.get())
            self.set_view()
        return

    def open_excel_file(self):
        if self.data_changed:
            if not self.view.ask_confirm('Ungespeicherte Daten',
                                         'Daten in Ihrer aktuell geöffneten Datei sind noch nicht gespeichert. '
                                         'Fortfahren ohne zu speichern?'):
                return
        excel_filename = self.view.ask_open_excel_filename()
        if excel_filename != "":
            print(f'{__name__}: Excel-Datei öffnen.')
            print("-filename: ", excel_filename)
            if self.model.database:  # if data present, reset to start conditions
                self.category = None
                self.subcategory = None
                self.keys_to_display_list = []
                self.actual_key = None
                self.model.database = {}
                self.model.column_names = []
                self.view.clear_data()
            self.model.import_excel_file(filename=excel_filename)
            self.set_view()
            return

    def save_file(self):
        self.save_fields()
        if not self.data_changed:
            return
        self.model.save_as_csv_file(self.model.filename, self.model.database)
        self.data_changed = False
        return

    def save_as_new_file(self):
        self.save_fields()
        save_filename = self.view.ask_save_as_filename("Daten speichern als neue CSV-Datei unter")
        if save_filename != "":
            self.model.save_as_csv_file(save_filename)
            self.data_changed = False
            # Programm ändert Namen der aktuellen Datei auf den gewählten Speichernamen
            self.model.filename = save_filename
            self.parent.title(f'{PROGRAM} (Version {VERSION}) {self.model.filename}')
        return

    def export_as_excel_file(self):
        self.save_fields()
        save_filename = self.view.ask_save_as_filename("Daten exportieren als Excel-Datei unter")
        if save_filename != "":
            self.model.export_as_excel_file(save_filename)
        return

    def quit_program(self):
        if self.data_changed:
            if self.view.ask_confirm('Ungespeicherte Daten',
                                     'Daten in Ihrer aktuell geöffneten Datei sind noch nicht gespeichert. Trotzdem '
                                     'beenden?'):
                self.parent.quit()
            return
        self.parent.quit()
        return

    def create_new_entry(self):
        self.save_fields()  # save previous entry

        new_data_entry = {}
        for item in self.model.column_names:
            new_data_entry[item] = ''

        tmp_list = []
        for index, key in enumerate(self.model.database):
            try:
                key = int(key)
            except ValueError:
                key = index
            tmp_list.append(key)
        new_key = max(tmp_list)+1  # change from len() to max() to ensure unique key
        print(f'{__name__}: Erzeugen eines neuen Eintrags #{new_key}')
        new_data_entry[self.model.primary_key] = new_key

        if 'Letzte Aktualisierung' in self.model.column_names:
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
        print(f'{__name__}: Löschen des Eintrags #{self.actual_key}')
        self.model.database.pop(self.actual_key)
        self.category = None
        self.subcategory = None
        self.keys_to_display_list = [item for item in self.model.database]
        self.actual_key = self.keys_to_display_list[0]
        self.update_fields()
        self.data_changed = True
        pass


if __name__ == '__main__':
    """Module testing"""
    print(f'Testing module "{__file__}"')

    # Testing View-Handling with a specific view
    from View import View
    CSVFILE = r'C:\Users\Marek\Desktop\In_Bearbeitung_Inventur_02.03.2023_abend.csv'
    import tkinter as tk
    root = tk.Tk()
    root.title(f'Modultest für "{__file__}"')
    root.minsize(width=400, height=400)
    v = View(parent=root)  # Start specific view
    v.pack(fill='both', expand=True, padx=10, pady=5)
    c = Controller(root, None, v)
    root.mainloop()
    for var in vars(c):
        print(f'{var:_<40}{repr(vars(c)[var])}')
