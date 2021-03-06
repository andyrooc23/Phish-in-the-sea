import PySimpleGUI as sg
import pikepdf as pr
import urllib3
import requests
import webbrowser
import pyperclip as pc

"""
This is the main function that runs the graphicak user interface of our Email Phishing scan software.
This program requires the user to save an email as a pdf file and then upload it to the scanning software.
It will then take all of the hyperlinks from the pdf and use our specific API to scan it for insecurities.
After finding vulnerabilities it will prompt the user for a few different options including block sender, copy to
clipboard, and draft a new email to alert others of the phishing scam.

"""


def main():
    sg.theme('Dark Blue')

    # This is the layout of our GUI (pretty basic)
    layout = [[sg.Text('Check email PDF for Phishing Content ><>', font=('Helvetica 15 bold'))],
              [sg.Input(size=(50, 50)), sg.FileBrowse(file_types=(("PDF files", "*.pdf"),))],
              [sg.OK(button_text='Upload'), sg.Cancel(button_text='Forget it')]]

    window = sg.Window('Phish In The Sea', layout)

    # Listens for user input before continuing
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Forget it':
            break
        elif event == 'Upload':
            try:
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
                    # print("This email includes Phishing")
                    phishy_link_window()
                else:
                    # print("Email is clean :)")
                    no_phish_window()
                # for a in links:
                # print(a)

                # file.close()
            except Exception as e:
                print(e)

    window.close()


# This is a window that pops up if the links found in the email are malicious or phishing.
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
            block_sender_window()
        elif event == "Notify Others":
            notify_others_window()
    window.close()
    window = None


# If the file is an error a new popup window is thrown.
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


# This is window that pops up to allow the user to have access on how to block senders on main mail services.
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

    layout = [[sg.Text('Instructions for How to Block:', font=fontHeader)],
              [[sg.Text(txt, tooltip=urls[txt], enable_events=True, font=font,
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


# This is a window that gives the user options on how to notify others of phishing.
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
        # window.close()
        # window = None

# Shows the user text that can be copied to the clipboard.
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

# Didn't find any phishy content.
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

# This is the API call that uses a service to scan links for a slew of malicious content. (Phishing, malware, etc)
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
