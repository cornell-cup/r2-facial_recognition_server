import io
from multiprocessing import Pool

import cv2
from bs4 import BeautifulSoup
from requests import get
from gamlogger import get_default_logger

from .utils import img_from_bytes
from .config import PROCESSORS

logger = get_default_logger(__name__)


def default_loader(url, *args, **kwargs):
    """
    Loads the html from the url and returns it as a string.
    """
    response = get(url)
    return response.text


def derive_first_last(known_name, filename):
    """
    Derives the first and last name from the known name.
    """
    filename = filename[filename.rfind('/') + 1:filename.rfind('.')]
    # Traverse known and filename until unexpected space
    i = 0
    try:
        while known_name[i] == filename[i]:
            i += 1
    except IndexError:
        raise ValueError(f'{known_name} and {filename} are not compatible. '
                         f'(Different lengths)')
    # Sanity check
    if known_name[i] != ' ':
        raise ValueError(f'{known_name} and {filename} are not compatible. '
                         f'Expected a space separated first and last name.')
    first, last = known_name[:i], known_name[i+1:]
    
    return first, last


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
    for card in cards:
        name, img, subteam = card.find('h2').text, \
                             card.find('img').get('src'), card.find('h3').text
        logger.debug('')
        if name in allow_list:
            print(f'Loaded {name}')
            first, last = derive_first_last(name, img)
            print(f'{first}_{last}')
            members[f'{first}_{last}'] = (img, subteam)
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
