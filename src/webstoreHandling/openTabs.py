import webbrowser

def main():
    openTabs()

def openTabs():
    base_url = "https://chrome.google.com/webstore/detail/"
    with open('tabsToBeOpened.txt', 'r') as inF:
        endings = inF.read().splitlines()
    for e in endings:
        url = base_url + e
        chrome_path = '/usr/bin/google-chrome %s'
        webbrowser.get(chrome_path).open(url)


if __name__ == '__main__':
    main()
