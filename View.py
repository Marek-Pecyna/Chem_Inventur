import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.messagebox import askokcancel

FONT_SIZE = 10


class CategoryFrame(ttk.Labelframe):
    """ Display and choosing of category and subcategory """
    def __init__(self, parent=None, **kwargs):
        ttk.Labelframe.__init__(self, master=parent, **kwargs)
        self.columnconfigure(1, weight=1)
        label_widget = ttk.Label(text='Kategorie auswählen', foreground='blue')
        self.configure(labelwidget=label_widget, )

        self.combobox_category = ttk.Combobox(self,
                                              textvariable=parent.current_category_variable,
                                              font=('Helvetica', FONT_SIZE))
        self.combobox_category.set('Kategorie auswählen')
        self.combobox_category['state'] = 'readonly'
        self.combobox_category.grid(row=0, column=0, sticky='we', columnspan=3)

        self.combobox_subcategory = ttk.Combobox(self,
                                                 textvariable=parent.current_subcategory_variable,
                                                 font=('Helvetica', FONT_SIZE))
        self.combobox_subcategory['state'] = 'readonly'
        self.combobox_subcategory.grid(row=1, column=0, sticky='we', columnspan=3)
        self.number_of_subcategories_label = ttk.Label(self,
                                                       textvariable=parent.number_of_subcategories_variable,
                                                       font=('Helvetica', FONT_SIZE))
        self.number_of_subcategories_label.grid(row=2, column=0, sticky='we', columnspan=3)

        self.back_button = ttk.Button(self, text='\u25C0', width=5)
        self.back_button.grid(row=3, column=0, sticky='news')
        name_label = ttk.Label(self, textvariable=parent.actual_value_of_subcategory_variable,
                               relief=tk.GROOVE,
                               anchor='c',
                               font=('Arial', 15))
        name_label.grid(row=3, column=1, sticky="we")
        self.forward_button = ttk.Button(self, text='\u25B6', width=5)
        self.forward_button.grid(row=3, column=2, sticky='news')
        return


class SearchFrame(ttk.Labelframe):
    def __init__(self, parent=None, **kwargs):
        ttk.Labelframe.__init__(self, master=parent, **kwargs)
        label_widget = ttk.Label(text='Einträge suchen', foreground='blue')
        self.configure(labelwidget=label_widget)
        self.search_entry = ttk.Entry(self)
        self.search_entry.grid(row=0, column=0, sticky="we")
        self.columnconfigure(0, weight=1)
        return


class ScrollbarFrame(ttk.Frame):
    """
    Extends class tk.Frame to support a scrollable Frame
    This class is independent of the widgets to be scrolled and
    can be used to replace a standard tk.Frame
    """
    def __init__(self, parent=None, **kwargs):
        ttk.Frame.__init__(self, master=parent, **kwargs)

        # The Scrollbar, layout to the right
        self.vsb = tk.Scrollbar(self, orient="vertical")
        self.vsb.pack(side='right', fill='y')

        # The Canvas which supports the Scrollbar Interface, layout to the left
        self.canvas = tk.Canvas(self, width=0, height=0, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Bind the Scrollbar to the self.canvas Scrollbar Interface
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.configure(command=self.canvas.yview)

        # The Frame to be scrolled, layout into the canvas
        # All widgets to be scrolled have to use this Frame as parent
        self.scrolled_frame = ttk.Frame(self.canvas)
        self.windows_item = self.canvas.create_window((0, 0), window=self.scrolled_frame, anchor="nw")

        # Configures the scrollregion of the Canvas dynamically
        self.bind("<Configure>", self.on_configure)
        self.bind('<Enter>', self._bound_to_mousewheel)
        self.bind('<Leave>', self._unbound_to_mousewheel)

        self.event = None
        return

    def on_configure(self, event):
        """Set the scroll region to encompass the scrolled frame"""
        self.event = event
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        if event:
            self.canvas.itemconfig(self.windows_item, width=event.width-int(1.5*self.vsb.winfo_reqwidth()))
        return

    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")


class InputFrame(ttk.Labelframe):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        label_widget = ttk.Label(text='Bitte machen Sie Ihre Eingaben', foreground='blue')
        self.configure(labelwidget=label_widget, padding=5)
        self.sbf = ScrollbarFrame(self, relief=tk.GROOVE, borderwidth=3)
        self.sbf.pack(fill='both', expand=True)
        self.edit_frame = self.sbf.scrolled_frame
        sg = ttk.Sizegrip(self, style='BW.TSizegrip')
        sg.pack(side='right')
        return


class ButtonFrame(ttk.Frame):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.delete_entry_button = ttk.Button(self, text='Eintrag löschen', style='my1.TButton')
        self.delete_entry_button.pack(side='left')
        self.new_entry_button = ttk.Button(self, text='Neuer Eintrag', style='my1.TButton')
        self.new_entry_button.pack(side='right')
        return


class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Variables to display
        self.chosen_delimiter = tk.StringVar(value=';')
        self.chosen_encoding = tk.StringVar(value='utf-16')
        self.current_category_variable = tk.StringVar()
        self.current_subcategory_variable = tk.StringVar()
        self.number_of_subcategories_variable = tk.StringVar()
        self.actual_value_of_subcategory_variable = tk.StringVar()
        self.edit_label_width = 0
        self.label_list = []
        self.entry_list = []
        self.text_variable_list = []

        # Style definitions
        s = ttk.Style()
        s.configure('my1.TButton', font=('Arial', 12), foreground='blue')
        s.configure("BW.TSizegrip", background="blue")

        # Menu
        self.build_menu_bar()

        # Prepare GUI
        self.category_frame = CategoryFrame(self, padding=5)
        self.category_frame.pack(fill='x')
        self.input_frame = InputFrame(self, padding=5)
        self.input_frame.pack(fill='both', expand=True)

        self.search_frame = SearchFrame(self, padding=5)
        # self.search_frame.pack(fill='x')

        self.button_frame = ButtonFrame(self, padding=5)
        self.button_frame.pack(side='bottom', fill='x')

        print(f'{__name__}:       View wurde initialisiert.')
        return

    def build_menu_bar(self):
        menubar = tk.Menu(self.winfo_toplevel())
        self.winfo_toplevel().configure(menu=menubar)

        self.file_menu = tk.Menu(menubar, tearoff=0)
        self.file_menu.add_command(label='Öffnen', accelerator="Strg+O", underline=1,
                                   command=self.ask_open_csv_filename)
        self.file_menu.add_command(label='Importieren aus Excel', accelerator="Strg+I", underline=0,
                                   command=self.ask_open_excel_filename)
        self.file_menu.add_command(label='Speichern', accelerator="Strg+S", underline=0)
        self.file_menu.add_command(label='Speichern unter...', accelerator="Strg+Alt+S",
                                   underline=10, command=lambda: self.ask_save_as_filename("Speichern unter"))
        self.file_menu.add_command(label='Exportieren nach Excel', accelerator="Strg+E", underline=0)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Beenden', underline=0, command=self.winfo_toplevel().destroy)
        menubar.add_cascade(label='Datei', underline=0, menu=self.file_menu)

        self.option_menu = tk.Menu(menubar, tearoff=0)
        self.option_menu.add_radiobutton(label='Semikolon', value=';',
                                         variable=self.chosen_delimiter)
        self.option_menu.add_radiobutton(label='Komma', value=',',
                                         variable=self.chosen_delimiter)
        self.option_menu.add_radiobutton(label='Tab', value='\t',
                                         variable=self.chosen_delimiter)
        self.option_menu.add_separator()
        self.option_menu.add_radiobutton(label='UTF', value='utf',
                                         variable=self.chosen_encoding)
        self.option_menu.add_radiobutton(label='UTF-8', value='utf-8',
                                         variable=self.chosen_encoding)
        self.option_menu.add_radiobutton(label='UTF-16', value='utf-16',
                                         variable=self.chosen_encoding)
        self.option_menu.add_radiobutton(label='ASCII', value='ascii',
                                         variable=self.chosen_encoding)
        menubar.add_cascade(label='Optionen', underline=0, menu=self.option_menu)

    def fill_gui_with_data(self, fieldnames, primary_key=None, extra_category=None):
        categories = [name for name in fieldnames if name != primary_key]
        if extra_category:
            categories = [extra_category] + categories
        self.category_frame.combobox_category['values'] = categories

        # Get longest string for display in edit_frame
        for name in fieldnames:
            if len(name) > self.edit_label_width:
                self.edit_label_width = len(name)

        # Build labels and entry widgets
        self.text_variable_list = [None for key in fieldnames]

        for index, key in enumerate(fieldnames):
            textvariable = tk.StringVar(value='No data')
            # self.listbox.insert("end", key)
            label = ttk.Label(self.input_frame.edit_frame,
                              text=key,
                              anchor='w',
                              justify='left',
                              width=self.edit_label_width,
                              font=('Helvetica', FONT_SIZE))
            label.grid(row=index, column=0, padx=0)
            self.label_list.append(label)

            entry = ttk.Entry(self.input_frame.edit_frame,
                              textvariable=textvariable,
                              justify='left',
                              width=50,
                              font=('Helvetica', FONT_SIZE),
                              cursor="xterm",
                              validate="focusout",
                              validatecommand=None)  # 'validatecommand' gets called, when focus is lost
            entry.grid(row=index, column=1, sticky='we', padx=0)
            if key == primary_key:
                entry['state'] = 'disabled'
            self.entry_list.append(entry)
            self.text_variable_list[index] = textvariable
        self.input_frame.edit_frame.columnconfigure(1, weight=1)

        # Hack for getting scrollbar handle without changing the window size:
        self.winfo_toplevel().minsize(width=500, height=363)
        self.input_frame.sbf.on_configure(self.input_frame.sbf.event)
        return

    def clear_data(self):
        for entry in self.label_list:
            entry.destroy()
        for entry in self.entry_list:
            entry.destroy()
        self.label_list = []
        self.entry_list = []
        for variable in self.text_variable_list:
            del variable
        self.text_variable_list = []
        self.update_idletasks()
        return

    @staticmethod
    def ask_save_as_filename(title):
        return filedialog.asksaveasfilename(title=title)

    @staticmethod
    def ask_open_csv_filename():
        return filedialog.askopenfilename(
            title="CSV-Datei öffnen", filetypes=(('CSV-Dateien', '*.csv'), ('Alle Dateien', '*.*')))

    @staticmethod
    def ask_open_excel_filename():
        return filedialog.askopenfilename(
            title="Excel-Datei importieren", filetypes=(('Excel-Dateien', '*.xlsx'), ('Alle Dateien', '*.*')))

    @staticmethod
    def ask_confirm(title, message):
        return askokcancel(title, message)


if __name__ == '__main__':
    """Module testing"""
    main_app = tk.Tk()
    main_app.title(f'Modultest {__file__}')
    main_app.minsize(width=500, height=330)
    main_app.configure(bg='lightblue')
    view = View(parent=main_app)
    view.pack(fill="both", expand=True, padx=5, pady=5)
    main_app.mainloop()
