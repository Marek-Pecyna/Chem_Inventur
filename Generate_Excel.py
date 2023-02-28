import xlsxwriter


def create_excel(data):
    def data_to_excel(data, worksheet, start_row):
        for n, entry in enumerate(data):
            col = 0
            text = int(entry['Name'])
            worksheet.write(start_row + n, col, text, right)
            col += 1
        return

    def create_cover_sheet():
        # Creation of first sheet in workbook object
        cover_sheet = workbook.add_worksheet()
        cover_sheet.set_column(0, 0, 17)
        cover_sheet.set_column('B:B', 12.5)
        cover_sheet.set_column('C:C', 12.5)
        row = 0  # used for relative positioning

        for i in range(1, 7):
            cover_sheet.write(row, i, None, header_cell_format)
        row += 1

    # Create workbook and formats
    workbook = xlsxwriter.Workbook(
        'Inventur 2022.xlsx')

    header_cell_format = workbook.add_format({
        'bg_color': r'#d4ddcf',
        'font_size': 16,
        'bottom': True})

    great = workbook.add_format({'font_size': 15})
    small = workbook.add_format({'font_size': 9})

    italic_small = workbook.add_format({'italic': True,
                                        'font_size': 9})

    top = workbook.add_format({'top': True})
    bottom = workbook.add_format({'bottom': True})
    right = workbook.add_format({'right': True})
    left = workbook.add_format({'left': True})
    bottom_right = workbook.add_format({'bottom': True, 'right': True})
    bottom_left = workbook.add_format({'bottom': True, 'left': True})
    bold = workbook.add_format({'bold': True})
    grey = workbook.add_format({'font_color': 'gray'})
    grey_left = workbook.add_format({'font_color': 'gray',
                                     'left': True})
    grey_bottom = workbook.add_format({'font_color': 'gray',
                                       'bottom': True})
    grey_bottom_left = workbook.add_format({'font_color': 'gray',
                                            'bottom': True,
                                            'left': True})

    float_format = workbook.add_format()
    float_format.set_num_format('0.000; [Red] (-0.000); [Magenta] 0')

    integer_format = workbook.add_format()
    integer_format.set_num_format('0; [Red] (-0); [Magenta] 0')

    float_left = workbook.add_format({'left': True})
    float_left.set_num_format('0.000; [Red] (-0.000); [Magenta] 0')

    integer_left = workbook.add_format({'left': True})
    integer_left.set_num_format('0; [Red] (-0); [Magenta] 0')

    float_format_grey = workbook.add_format({'font_color': 'gray',
                                             'left': True})
    float_format_grey.set_num_format('0.000; [Red] (-0.000); [Magenta] 0')

    integer_format_grey = workbook.add_format({'font_color': 'gray',
                                               'left': True})
    integer_format_grey.set_num_format('0; [Red] (-0); [Magenta] 0')

    create_cover_sheet()  # create Cover Sheet

    # Closing of workbook necessary for writing
    workbook.close()

    return
