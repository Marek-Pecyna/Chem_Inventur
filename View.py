import tkinter as tk
from tkinter import ttk, filedialog

WIDTH, HEIGHT = 450, 630
INITIAL_X_POSITION, INITIAL_Y_POSITION = 0, 0
PADX, PADY = 5, 5
FONT_SIZE = 10


class View(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Variables to display
        self.current_category_variable = tk.StringVar()
        self.current_subcategory_variable = tk.StringVar()
        self.number_of_chemicals_variable = tk.StringVar()
        self.actual_value_of_category_variable = tk.StringVar()
        self.edit_label_width = 0
        self.label_list = []
        self.entry_list = []
        self.text_variable_list = []

        # Style definitions
        s = ttk.Style()
        s.configure('my1.TButton', font=('Arial', 12), foreground='blue')
        s.configure("BW.TSizegrip", background="blue")

        # Build GUI
        self.__build_gui()
        return

    def __build_gui(self):
        row = 0

        label_widget = ttk.Label(text='Kategorie auswählen', foreground='blue')
        name_frame = ttk.LabelFrame(self, relief=tk.GROOVE, labelwidget=label_widget, padding=5)
        name_frame.grid(row=row, column=0, sticky='news', padx=5, pady=2)

        self.combobox_category = ttk.Combobox(name_frame,
                                              textvariable=self.current_category_variable,
                                              font=('Arial', FONT_SIZE))
        self.combobox_category.set('Kategorie auswählen')
        self.combobox_category['state'] = 'readonly'
        self.combobox_category.grid(row=0, column=0, sticky='we', columnspan=3)

        self.combobox_subcategory = ttk.Combobox(name_frame,
                                                 textvariable=self.current_subcategory_variable,
                                                 font=('Arial', FONT_SIZE))
        self.combobox_subcategory.set('Unterkategorie auswählen')
        self.combobox_subcategory['state'] = 'readonly'
        self.combobox_subcategory.grid(row=1, column=0, sticky='we', columnspan=3)
        self.number_of_chemicals_label = ttk.Label(name_frame, textvariable=self.number_of_chemicals_variable)
        self.number_of_chemicals_label.grid(row=2, column=0, sticky='we', columnspan=3)

        name_frame.columnconfigure(1, weight=1)
        self.back_button = ttk.Button(name_frame, text='\u25C0', width=5)
        self.back_button.grid(row=3, column=0, sticky='news')
        name_label = ttk.Label(name_frame, textvariable=self.actual_value_of_category_variable,
                               relief=tk.GROOVE,
                               anchor='c',
                               font=('Arial', 15))
        name_label.grid(row=3, column=1, sticky="we")
        self.forward_button = ttk.Button(name_frame, text='\u25B6', width=5)
        self.forward_button.grid(row=3, column=2, sticky='news')
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

    def fill_gui_with_data(self, fieldnames, primary_key=None, extra_category=None):
        categories = [name for name in fieldnames if name != primary_key]
        if extra_category:
            categories = [extra_category] + categories
        self.combobox_category['values'] = categories

        # Get longest string for display in edit_frame
        for name in fieldnames:
            if len(name) > self.edit_label_width:
                self.edit_label_width = len(name)

        # Build labels and entry widgets
        self.text_variable_list = [None for key in fieldnames]

        for index, key in enumerate(fieldnames):
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
                              width=40,
                              font=('Arial', FONT_SIZE))
            entry.grid(row=index, column=2, sticky='we', padx=5)
            if key == primary_key:
                entry['state'] = 'disabled'
            self.entry_list.append(entry)
            self.text_variable_list[index] = textvariable
        self.edit_frame.columnconfigure(2, weight=1)
        return

    @staticmethod
    def ask_save_filename():
        return filedialog.asksaveasfilename(title="Daten speichern")


if __name__ == '__main__':
    """Module testing"""
    from Constants import PROGRAM, VERSION

    main_app = tk.Tk()
    main_app.title(f'Modultest {__file__} {PROGRAM} (Version {VERSION})')
    main_app.minsize(width=400, height=400)
    view = View(parent=main_app)
    view.pack(fill="both", expand=True, padx=10, pady=5)

    # from Controller import Controller
    # c = Controller()
    # c.set_view(view)  # GUI behaviour is changed by controller
    # view.set_controller(c)  # currently not needed
    main_app.mainloop()
