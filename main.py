import PySimpleGUI as sg
import PyPDF2 as pr


sg.theme('Light Blue')

layout = [  [sg.Text('Check email PDF for Phishing Content ><>', font=('Helvetica 15 bold'))],
            [sg.Input(size=(50,50)), sg.FileBrowse()],
            [sg.OK(), sg.Cancel()]]

window = sg.Window('Phis In The Sea', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    elif event == 'OK':
        file = open(values[0], 'rb')
        emailPDF = pr.PdfFileReader(file)
        print(emailPDF.getPage(0).extractText())

        file.close()

window.close()