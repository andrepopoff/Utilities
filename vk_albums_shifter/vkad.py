import sys
import requests

APP_ID = '6273721'
API_PATH = 'https://api.vk.com/method/'
API_VERSION = 5.52
access_token = ''  # Before you start, you need to get access_token


def get_group_id():
    if len(sys.argv) == 2:
        group_id_by_city = {'syk': -22426905, 'uht': -79007931}
        return group_id_by_city.get(sys.argv[1])


def get_all_albums(group_id):
    response = requests.get(API_PATH + 'photos.reorderAlbums', params={'v': API_VERSION, 'owner_id': group_id,
                                                                       'access_token': access_token, 'need_covers': 1,
                                                                       'photo_sizes': 1})
    if response.get('response'):
        return response['response']['items']


if __name__ == '__main__':
    group_id = get_group_id()
    if group_id:
        all_albums = get_all_albums(group_id)
