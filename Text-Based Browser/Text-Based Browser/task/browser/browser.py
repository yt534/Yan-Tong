import sys
import os
import requests
from collections import deque
from bs4 import BeautifulSoup
from colorama import init, Fore

dir_name = sys.argv[1]

if not os.path.exists(dir_name):
    os.mkdir(dir_name)

history = deque()


def get_site_content(url):
    """
    output: string
    """
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'html.parser')
    tags = ['h{}'.format(i) for i in range(1,7)]
    tags += ['p','a','ul','ol','li']
    content = soup.find_all(tags)
    output = ''
    for i in content:
        if i.name == 'a':
            output += Fore.BLUE + i.text
        else:
            output += i.text
    return output
#     return soup.prettify()


def save_site_content(data, path):
    history.append(path)
    with open(os.path.join(dir_name, path), "w") as f:
        f.write(data)


def go_site(site):
    address = site if site.startswith("https://") else f"https://{site}"
    site_content = get_site_content(address)
    save_site_content(site_content, site)
    print(site_content)


def go_back():
    history.pop()
    with open(os.path.join(dir_name, history.pop()), 'r') as f:
        print(f.read())


while True:
    command = input()
    if command == "exit":
        break
    if command == "back":
        go_back()
    elif "." in command:
        go_site(command)
    else:
        print("Error: Incorrect URL")
