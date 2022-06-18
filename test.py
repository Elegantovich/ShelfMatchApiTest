import base64
import logging
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    filemode='w'
)
LOGIN = os.getenv('LOGIN', default='test.task.account')
PASSWORD = os.getenv('PASSWORD', default='Z0w7S1qAdjzDZ5')
cred = {'account': {'login': LOGIN, 'password': PASSWORD}}
url_auth = 'https://oauth.shelfmatch.com/token/'
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
recognize_list = []

"""
Frequency of requests to the server.
"""
step_time = 10


"""
Recieve images for recognize. gif images are not supported!
"""


def get_files(path):
    for root, dirs, files in os.walk(path):
        for i in files:
            if '.gif' in i or '.png' in i or '.jpg' in i:
                image = f'{root}\\{i}'
                with open(image, 'rb') as image_file:
                    image64 = str(base64.b64encode(image_file.read()))[2:-1]
                recognize_list.append(image64)
    return recognize_list


if __name__ == "__main__":
    """
    Timer start.
    """
    tic = time.perf_counter()
    session = requests.Session()
    auth = session.post(url_auth, json=cred, headers=headers).json()
    try:
        token = auth['account']['token']['value']
    except KeyError as error:
        logging.error(f'{error}')
    url_recognize = f'https://tea-api.shelfmatch.com/session?token={token}'
    body = {"tradePointID": "1", "images": get_files('test_images')}
    """
    Sending images to the server.
    """
    response = session.post(url_recognize, headers=headers, json=body).json()
    sessionID = response.get('sessionID')
    logging.info(f'{len(recognize_list)} files go to recognize')
    url_ses_id = (f'https://tea-api.shelfmatch.com/session?token={token}'
                  f'&sessionID={sessionID}&full=')
    while True:
        """
        Get status recognize of images.
        """
        status = (session.get(url_ses_id)).json()['session'].get('processed')
        logging.info(f'status of recognize files: {status}')
        if status.upper() == 'PROCESSED':
            toc = time.perf_counter()
            logging.info('The task has been successfully. '
                         f'Files processed: {len(recognize_list)}, '
                         f'time spent {round((toc - tic), 2)} sec., average '
                         ' processing time per file '
                         f'= {round((toc - tic)/len(recognize_list), 2)} sec.')
            break
        elif status.upper() == 'RECOGNITION_SERVICE_ERROR':
            logging.error('An error has occurred, check that all images are '
                          'valid format(.png, .jpg)')
            break
        else:
            time.sleep(step_time)
