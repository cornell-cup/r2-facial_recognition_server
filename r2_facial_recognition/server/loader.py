import io
from multiprocessing import Pool

import cv2
from bs4 import BeautifulSoup
from requests import get
from gamlogger import get_default_logger

try:
    from .utils import img_from_bytes
    from .config import PROCESSORS
except ImportError:
    from utils import img_from_bytes
    from config import PROCESSORS

logger = get_default_logger(__name__)


def default_loader(url, *args, **kwargs):
    """
    Loads the html from the url and returns it as a string.
    """
    response = get(url)
    return response.text


def cornellcup_loader(url, allow_list=None, *args, **kwargs):
    """
    Loads the html from the url and parse all the members of CUP into Mappings.
    """
    allow_list = [] if allow_list is None else allow_list
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
    print(f'allow_list={allow_list}')
    for card in cards:
        name, img, subteam = card.find('h2').text, \
                             card.find('img').get('src'), card.find('h3').text
        logger.debug('')
        if name in allow_list:
            print(f'Loaded {name}')
            members[name] = (img, subteam)
        else:
            print(f'{name} was not loaded.')

    with Pool(processes=PROCESSORS) as pool:
        # Load the image from the url
        for member, (image_url, subteam) in members.items():
            image = pool.apply_async(_load_content,
                                     (f'{url_stem}/{image_url}',))
            members[member] = (image, subteam)
        for member, (image, subteam) in members.items():
            img = img_from_bytes(image.get())
            print(f'{member} ({subteam}) loaded!')
            members[member] = (img, subteam)

    return members


def _load_content(url):
    return get(url).content


def load(url, loader='default_loader', *args, **kwargs):
    vals = globals()[loader](url, *args, **kwargs)
    return vals


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
    

    
