import sys
import requests
import re

from vk_settings import API_PATH, BASE_TOKEN, API_VERSION


APP_ID = '6967460'
access_token = BASE_TOKEN  # Before you start, you need to get access_token


def get_group_id():
    if len(sys.argv) == 2:
        group_id_by_city = {'syk': -22426905, 'uht': -79007931}
        return group_id_by_city.get(sys.argv[1])


def get_all_albums(group_id):
    response = requests.get(API_PATH + 'photos.getAlbums', params={'v': API_VERSION, 'owner_id': group_id,
                                                                   'access_token': access_token})
    response_dict = response.json()
    if response_dict.get('response'):
        return response_dict['response']['items']
    return []


if __name__ == '__main__':
    group_id = get_group_id()
    if group_id:
        all_albums = get_all_albums(group_id)

        for album in all_albums:
            if album['id'] != 140958045:
                title = album['title']
                stopped = re.findall(r'\bстоп\b', title, flags=re.I)
                if stopped:
                    break
                description = album['description']
                message = title + '\n\n' + description if description else title
                group_url = 'https://vk.com/club' + str(group_id)[1:]
                attachment = 'album{}_{}'.format(group_id, album['id'])
                album_url = 'https://vk.com/' + attachment
                signature = '\n\nАльбом: {}\nГруппа: {}'.format(album_url, group_url)
                message += signature
                response = requests.get(API_PATH + 'wall.post', params={'v': API_VERSION, 'owner_id': group_id,
                                                                        'access_token': access_token, 'from_group': 1,
                                                                        'message': message, 'attachments': attachment})
                print(response.json())
            break
