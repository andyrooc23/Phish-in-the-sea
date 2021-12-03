import requests
import urllib3


def is_phishing(ls):
    api_link = "https://ipqualityscore.com/api/json/url/sKAXMkPigeY0JjodJK9iZW3hR8hBNhVO/"
    for x in ls:
        domain = urllib3.get_host(x)

        response = requests.get(api_link + domain[1])
        if response.json()['unsafe'] or response.json()['phishing'] or response.json()['suspicious']\
                or 'googleapi' in x:
            return True
        else:
            continue
    return False


if __name__ == '__main__':
    links = [
        'www.google.com',
        'www.instagram.com',
        'outlook.office.com'
    ]
    links2 = [
        # 'www.google.com',
        # 'www.instagram.com',
        # 'outlook.office.com',
        'https://storage.googleapis.com/hpcore5wn/s98p214sm32s5sd4hui1jh4f7z85ttty2u5ik5j1g26/cH5df9DG2hER3g'
    ]
    # if is_phishing(links):
    #     print("is phishing 1")
    if is_phishing(links2):
        print("is phishing 2")
    else:
        print('is clean')
