import PySimpleGUI as sg
import pikepdf as pr


def main():
    sg.theme('Light Blue')

    layout = [[sg.Text('Check email PDF for Phishing Content ><>', font=('Helvetica 15 bold'))],
              [sg.Input(size=(50, 50)), sg.FileBrowse(file_types=(("PDF files", "*.pdf"),))],
              [sg.OK(button_text='Upload'), sg.Cancel(button_text='Forget it')]]

    window = sg.Window('Phish In The Sea', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Forget it':
            break
        elif event == 'Upload':

            # Scan the document and find phishing
            file = open(values[0], 'rb')
            emailPDF = pr.Pdf.open(file)

            links = []

            for page in emailPDF.pages:
                for annots in page.get("/Annots"):
                    uri = annots.get("/A").get("/URI")
                    if uri is not None:
                        links.append(uri)

            for a in links:
                print(a)
            file.close()

    window.close()

if __name__ == "__main__":
    main()
