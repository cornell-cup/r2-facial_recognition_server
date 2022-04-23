import io
from multiprocessing import Pool

import cv2
from PIL import Image
from bs4 import BeautifulSoup
from requests import get
import numpy as np

try:
    from .config import PROCESSORS
except ImportError:
    from config import PROCESSORS


def DEFAULT_LOADER(url):
    """
    Loads the html from the url and returns it as a string.
    """
    response = get(url)
    return response.text


def cornellcup_loader(url):
    """
    Loads the html from the url and parse all the members of CUP into Mappings.
    """
    response = get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    cards = soup.find_all('div', {'class': 'cards'})
    # card : {
    #   'name': [name],
    #   'image': [image_url],
    #   'subteam': [subteam],
    # }
    # 
    # 
    url_stem = url.rsplit('/', 1)[0]
    members: dict = {}
    for card in cards:
        print(card)
        members[card.find('h2').text] = (card.find('h3').text, card.find('img').get('src'))

    with Pool(processes=PROCESSORS) as pool:
        # Load the image from the url
        for member, (subteam, image_url) in members.items():
            image = pool.apply_async(load_content, (f'{url_stem}/{image_url}',))
            members[member] = (subteam, image)
        for member, (subteam, image) in members.items():
            img_io = io.BytesIO(image.get())
            print(f'{member} ({subteam}) loaded!')
            members[member] = (subteam, )

    return members


def load_content(url):
    return get(url).content


def load(url, loader=DEFAULT_LOADER):
    return loader(url)


def _display_info(map_, name):
    subteam = map_[name][0]
    image = cv2.resize(map_[name][1], (0, 0), fx=0.25, fy=0.25)
    cv2.putText(image, name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(image, subteam, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow(name, image)


if __name__ == '__main__':
    mappings = cornellcup_loader('https://cornellcuprobotics.com/members.html')
    _display_info(mappings, 'Christopher De Jesus')
    cv2.waitKey(0)
    

    
