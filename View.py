import tkinter as tk
from tkinter import ttk, filedialog
import os
#from PIL import Image, ImageTk

WIDTH, HEIGHT = 450, 630
INITIAL_X_POSITION, INITIAL_Y_POSITION = 0, 0
PADX, PADY = 5, 5
FONT_SIZE = 10


class View(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = None

        # data instances
        self.primary_key = None

        self.current_category_variable = tk.StringVar()
        self.actual_value_of_category_variable = tk.StringVar()
        self.actual_key = None
        self.key_value_list = []
        self.fieldnames = []

        self.edit_label_width = 0
        self.database = []  # list of dictionaries

        # Style definitions
        s = ttk.Style()
        s.configure('my1.TButton', font=('Arial', 12), foreground='blue')
        s.configure("BW.TSizegrip", background="blue")

        # Build GUI and fill with data
        self.__build_gui()
        return

    def __build_gui(self):
        row = 0

        label_widget = ttk.Label(text='Kategorie auswählen', foreground='blue')
        name_frame = ttk.LabelFrame(self, relief=tk.GROOVE, labelwidget=label_widget, padding=5)
        name_frame.grid(row=row, column=0, sticky='news', padx=5, pady=2)

        self.combobox = ttk.Combobox(name_frame, textvariable=self.current_category_variable)
        self.combobox.set('Kategorie auswählen')
        self.combobox['state'] = 'readonly'
        self.combobox.grid(row=0, column=0, sticky='we', columnspan=3)

        name_frame.columnconfigure(1, weight=1)
        back_button = ttk.Button(name_frame, text='\u25C0', width=5, command=self.previous_key)
        back_button.grid(row=1, column=0, sticky='news')
        name_label = ttk.Label(name_frame, textvariable=self.actual_value_of_category_variable,
                               relief=tk.GROOVE,
                               anchor='c',
                               font=('Arial', 15))
        name_label.grid(row=1, column=1, sticky="we")
        forward_button = ttk.Button(name_frame, text='\u25B6', width=5, command=self.next_key)
        forward_button.grid(row=1, column=2, sticky='news')
        row += 1

        # Display of data for one compound
        label_widget = ttk.Label(text='Bitte machen Sie Ihre Eingaben', foreground='blue')
        self.edit_frame = ttk.LabelFrame(self, relief=tk.GROOVE, labelwidget=label_widget)
        self.edit_frame.grid(row=row, column=0, sticky='news', padx=5, pady=2)
        row += 1

        self.save_button = ttk.Button(self, text='Speichern', style='my1.TButton')
        self.save_button.grid(row=row, column=0, padx=5, pady=0)
        sg = ttk.Sizegrip(self, style='BW.TSizegrip')
        sg.grid(row=row, column=0, sticky='se')
        self.columnconfigure(0, weight=1)
        return

    def previous_key(self):
        if self.actual_key is None or self.key_value_list == []:
            return
        self.save_fields()
        if self.actual_key > 0:
            self.actual_key -= 1
        elif self.actual_key == 0:
            self.actual_key = len(self.database) - 1  # set to last item

        self.actual_value_of_category_variable.set(self.key_value_list[self.actual_key])
        self.update_fields()

    def next_key(self):
        if self.actual_key is None or self.key_value_list == []:
            return
        self.save_fields()
        if self.actual_key < len(self.database)-1:
            self.actual_key += 1
        elif self.actual_key == len(self.database)-1:
            self.actual_key = 0

        self.actual_value_of_category_variable.set(self.key_value_list[self.actual_key])
        self.update_fields()

    def fill_gui_with_data(self, database, fieldnames, primary_key):
        self.database = database
        self.fieldnames = fieldnames
        self.primary_key = primary_key

        self.combobox['values'] = self.fieldnames

        # Get longest string for display in edit_frame
        for name in self.fieldnames:
            if len(name) > self.edit_label_width:
                self.edit_label_width = len(name)

        # Get a list with all primary keys
        self.key_value_list = [item for item in self.database]

        # Build labels and entry widgets
        self.actual_value_of_category_variable.set(self.actual_key)
        self.v = tk.IntVar()
        self.label_list = []
        self.entry_list = []
        self.textvariable_list = [None for key in self.fieldnames]

        for index, key in enumerate(self.fieldnames):
            textvariable = tk.StringVar(value='No data')
            # self.listbox.insert("end", key)
            label = ttk.Label(self.edit_frame,
                              text=key,
                              anchor='w',
                              justify='left',
                              width=self.edit_label_width,
                              font=('Arial', FONT_SIZE))
            label.grid(row=index, column=1, padx=5)
            self.label_list.append(label)

            entry = ttk.Entry(self.edit_frame,
                              textvariable=textvariable,
                              justify='left',
                              width=40)
            entry.grid(row=index, column=2, sticky='we', padx=5)
            self.entry_list.append(entry)
            self.textvariable_list[index] = textvariable
        self.edit_frame.columnconfigure(2, weight=1)
        self.actual_key = 0
        self.update_fields()
        return

    def update_fields(self):
        key_in_database = self.key_value_list[self.actual_key]
        self.actual_value_of_category_variable.set(key_in_database)
        data_entry = self.database[key_in_database].values()
        for index, item in enumerate(data_entry):
            self.textvariable_list[index].set(item)

    def save_fields(self):
        key_in_database = self.key_value_list[self.actual_key]
        for index, item in enumerate(self.database[key_in_database]):
            self.database[key_in_database][item] = self.textvariable_list[index].get()
        return

    @staticmethod
    def ask_save_filename():
        return filedialog.asksaveasfilename(title="Daten speichern")

    def set_controller(self, controller):
        self.controller = controller


if __name__ == '__main__':
    """Module testing"""
    from Constants import PROGRAM, VERSION

    main_app = tk.Tk()
    main_app.title('Chemikalien-Inventur Version 0.1')
    main_app.minsize(width=400, height=400)
    view = View(parent=main_app)
    view.pack(fill="both", expand=True, padx=10, pady=5)

    # from Controller import Controller
    # c = Controller()
    # c.set_view(view)  # GUI behaviour is changed by controller
    # view.set_controller(c)  # currently not needed
    main_app.mainloop()
