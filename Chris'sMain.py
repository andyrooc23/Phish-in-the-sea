import PySimpleGUI as sg
import PyPDF2 as pr


def main():
    sg.theme('Light Blue')

    layout = [[sg.Text('Check email PDF for Phishing Content ><>', font='Helvetica 15 bold')],
              [sg.Input(size=(50, 50)), sg.FileBrowse(file_types=(("PDF files", "*.pdf"),))],
              [sg.OK(), sg.Cancel()]]

    window = sg.Window('Phish In The Sea', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        if event == 'OK':
            try:
                file = open(values[0], 'rb')
                emailPDF = pr.PdfFileReader(file)
                print(emailPDF.getPage(0).extractText())
                file.close()
                open_phishy_link_window()
                break
            except FileNotFoundError:
                file_not_found_window()

    window.close()


def open_phishy_link_window():
    phishy_window = [[sg.Text(
        'This email contains a malicious link! Consider blocking the sender and \nnotifying people you know about the '
        'potential threat.',
        font='Helvetica 15 bold')],
        [sg.OK("Block Sender"), sg.OK("Notify Others"), sg.Cancel()]]

    window = sg.Window('This email contains a malicious link!', phishy_window)

    while True:
        event, values = window.read()
        if event == "Cancel" or event == sg.WIN_CLOSED:
            break
        elif event == "Block Sender":
            window.close()
            block_sender_window()
            break
        elif event == "Notify Others":
            window.close()
            notify_others_window()
            break
        window.close()
        window = None


def file_not_found_window():
    not_found = [[sg.Text('File not found', font=('Helvetica 15 bold'))],
                 [],
                 [sg.OK()]]

    window = sg.Window('Phish In The Sea', not_found)

    while True:
        event, values = window.read()
        if event == "OK" or event == sg.WIN_CLOSED:
            window.close()
            window = None
            break
        window.close()
        window = None


def block_sender_window():
    print("blocked")

def notify_others_window():
    notify_others = [[sg.Text('Notify others', font='Helvetica 15 bold')],
                 [],
                 [sg.OK()]]

    window = sg.Window('Phish In The Sea', notify_others)

    while True:
        event, values = window.read()
        if event == "OK" or event == sg.WIN_CLOSED:
            window.close()
            window = None
            break
        window.close()
        window = None

if __name__ == "__main__":
    main()
