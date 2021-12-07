import PySimpleGUI as sg
import PyPDF2 as pr

import PySimpleGUI as sg
import pikepdf as pr
import urllib3
import requests
import webbrowser
import pyperclip as pc

def main():
    sg.theme('Dark Blue')

    layout = [[sg.Text('Check email PDF for Phishing Content ><>', font=('Helvetica 15 bold'))],
              [sg.Input(size=(50, 50)), sg.FileBrowse(file_types=(("PDF files", "*.pdf"),))],
              [sg.OK(button_text='Upload'), sg.Cancel(button_text='Forget it')]]

    window = sg.Window('Phish In The Sea', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Forget it':
            break
        elif event == 'Upload':
            try:  # TODO in order to prevent it from erroring if not links

                # Scan the document and find phishing
                file = open(values[0], 'rb')
                emailPDF = pr.Pdf.open(file)

                links = []

                for page in emailPDF.pages:
                    for annots in page.get("/Annots"):
                        uri = annots.get("/A").get("/URI")
                        if uri is not None:
                            links.append(str(uri))

                # phishy_link_window()
                if is_phishing(links):
                    print("This email includes Phishing")
                    phishy_link_window()
                else:
                    print("Email is clean :)")
                    no_phish_window()
                for a in links:
                    print(a)

                # file.close()
            except Exception as e:
                print(e)

    window.close()


def phishy_link_window():
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
    urls = {
        'Gmail': 'https://support.google.com/mail/answer/8151?hl=en&co=GENIE.Platform%3DDesktop',
        'Outlook': 'https://support.microsoft.com/en-us/office/block-senders-or-mark-email-as-junk-in-outlook-com-a3ece97b-82f8-4a5e-9ac3-e92fa6427ae4',
        'Yahoo': 'https://help.yahoo.com/kb/SLN28140.html?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAAHtQ63y5LGI5OL8ypNe9vuT9a7NJ9rBpBlm45CZTm1zFkr03L_S8tVVT8o8Jzb_jhrzr6EAvGyut7OUKewo7FL1w47iEfF21ZjO1PMGdnlzyD4QorOXEYZXPZ_vTPqlsa1_XxP0jZNhS9mVlgPk8Yai3r7BkRZLUiWmtDkDLlkws',
    }

    # sort urls
    items = sorted(urls.keys())

    sg.theme("DarkBlue")
    font = ('Courier New', 16, 'underline')
    fontHeader = ('Courier New', 20, 'bold')

    layout = [[sg.Text('Instructions for How to Block:', font=fontHeader)], [[sg.Text(txt, tooltip=urls[txt], enable_events=True, font=font,
                       key=f'URL {urls[txt]}')] for txt in items]]

    window = sg.Window('How to Block Accounts', layout, finalize=True)

    # print out links
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event.startswith("URL "):
            url = event.split(' ')[1]
            webbrowser.open(url)
        print(event, values)

    window.close()


def notify_others_window():
    notify_others = [[sg.Text('Notify others', font='Helvetica 15 bold')],
                     [],
                     [sg.OK(), sg.OK('Draft E-Mail'), sg.OK('Copy E-Mail Content')],
                     ]

    window = sg.Window('Phish In The Sea', notify_others)

    while True:
        event, values = window.read()
        if event == "OK" or event == sg.WIN_CLOSED:
            window.close()
            window = None
            break
        if event == "Draft E-Mail":
            body_text = 'I recently got an email from a phishy site and wanted to let you know. Here is the name of ' \
                        'the email sender so that you can be safe.\n(Email Sender Here)\nBlessings: (Your name here)'
            body_text.replace(' ', '%20')
            webbrowser.open('mailto:?&subject=Phishing-Email&body=' + body_text, new=1)
        if event == 'Copy E-Mail Content':
            show_text()
        window.close()
        window = None


def show_text():
    notification = 'I recently got an email from a phishy site and wanted to let you know. ' \
                   'Here is the name of the email sender so that you can be safe.\n' \
                   '(Email Sender Here)\n Blessings: (Your name here)'

    notify_others = [[sg.Text('Notify others', font='Helvetica 15 bold')],
                     [sg.Text(notification, font='Helvetica 10')],
                     [sg.OK()], [sg.OK('Copy to Clipboard')]]

    window = sg.Window('Email Content', notify_others)

    while True:
        event, values = window.read()
        if event == 'Copy to Clipboard':
            pc.copy(notification)
            sg.Popup('Copied! Now paste anywhere you like :)')
        if event == 'OK' or event == sg.WIN_CLOSED:
            window.close()
            window = None
            break


def no_phish_window():
    notify_others = [[sg.Text('No phishy links were found in your email!', font='Helvetica 15 bold')],
                     [],
                     [sg.OK()]]

    window = sg.Window('Phish Free!', notify_others)
    while True:
        event, values = window.read()
        if event == "OK" or event == sg.WIN_CLOSED:
            window.close()
            window = None
            break
        window.close()
        window = None


def is_phishing(ls):
    api_link = "https://ipqualityscore.com/api/json/url/sKAXMkPigeY0JjodJK9iZW3hR8hBNhVO/"
    for x in ls:
        domain = urllib3.get_host(x)

        response = requests.get(api_link + domain[1])
        if response.json()['unsafe'] or response.json()['phishing'] or 'googleapi' in x:
            return True
        else:
            continue
    return False


if __name__ == "__main__":
    main()
