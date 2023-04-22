import PySimpleGUI as sg
"""window for dme output"""
def display_window(val, change):
    sg.theme('Black')
    sg.set_options(element_padding=(0, 0))

    layout = [[[sg.InputText(val, readonly=True, key='-IN-')],sg.Text(val, size=(8,2), font=('Helvetica', 20), justification='center', key='-OUTPUT-', enable_events=True)]]

    window = sg.Window('MSSB Batting Info', layout, keep_on_top=True, grab_anywhere=True)
    input = window['-IN-']
    while True:
        event, values = window.Read(timeout=10)
        if event == None or event == sg.WIN_CLOSED:
            break
        if event == sg.TIMEOUT_EVENT:
            continue
        else:
            get = input.get()
            t = f'{val}'
            input.update(value=t)