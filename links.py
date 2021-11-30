import webbrowser
import PySimpleGUI as sg

urls = {
    'Gmail': 'https://support.google.com/mail/answer/8151?hl=en&co=GENIE.Platform%3DDesktop',
    'Outlook': 'https://support.microsoft.com/en-us/office/block-senders-or-mark-email-as-junk-in-outlook-com-a3ece97b-82f8-4a5e-9ac3-e92fa6427ae4',
    'Yahoo': 'https://help.yahoo.com/kb/SLN28140.html?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAAHtQ63y5LGI5OL8ypNe9vuT9a7NJ9rBpBlm45CZTm1zFkr03L_S8tVVT8o8Jzb_jhrzr6EAvGyut7OUKewo7FL1w47iEfF21ZjO1PMGdnlzyD4QorOXEYZXPZ_vTPqlsa1_XxP0jZNhS9mVlgPk8Yai3r7BkRZLUiWmtDkDLlkws',
}
# comment
items = sorted(urls.keys())

sg.theme("DarkBlue")
font = ('Courier New', 16, 'underline')

layout = [[sg.Text(txt, tooltip=urls[txt], enable_events=True, font=font,
    key=f'URL {urls[txt]}')] for txt in items]
window = sg.Window('How to Block Accounts', layout, size=(250, 150), finalize=True)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event.startswith("URL "):
        url = event.split(' ')[1]
        webbrowser.open(url)
    print(event, values)

window.close()