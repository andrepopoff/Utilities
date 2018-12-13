"""
This script changes the order of the albums in the group on vk.com.
The script is useful, who has commercial groups on vk.com with a large number of albums.
This eliminates the routine of dragging albums with the PC mouse.
----------------------------------------------------------------------
Before you start, you need to get access_token.
Just follow:
https://oauth.vk.com/authorize?client_id=6273721&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=groups,photos,offline&response_type=token&v=5.52
and copy the data from the access_token parameter of url to the access_token variable.
-----------------------------------------------------------------------
By default, access_token = ''. Until you get access_token, the script will not work.
"""

import re
import sys
import time
import requests


APP_ID = '6273721'
API_PATH = 'https://api.vk.com/method/'
API_VERSION = 5.52
access_token = ''  # Before you start, you need to get access_token


def script_parameters():
    """
    Creates parameters for further script operation.
    Parameters differ depending on the method of calling the script.
    """
    if len(sys.argv) == 1:
        mode = 0
        album_pointer = input('Перед каким альбомом размещать? Введите ссылку: ')
        albums_to_move = input('Введите ссылку на перемещаемый альбом: ')
    else:
        mode = 1
        album_pointer = sys.argv[1]
        albums_to_move = sys.argv[2:]
    return {
        'mode': mode,
        'albums_to_move': albums_to_move,
        'album_pointer': album_pointer
    }


def pull_group_id(album_link):
    """
    Link to album --> group id
    """
    return re.findall('vk.com/album(-\d+)', album_link)[0]


def pull_album_ids(albums_to_move, album_pointer, mode):
    """
    Links to albums on vk.com --> album ids
    """
    try:
        id_for_point_album = re.findall('_([0-9]+$)', album_pointer)[0]
        album_ids = []

        if not mode:
            while albums_to_move != 'n':
                id_for_album_to_move = re.findall('_([0-9]+$)', albums_to_move)[0]
                album_ids.append(id_for_album_to_move)
                albums_to_move = input('Введите ссылку на новый альбом для перемещения (если еще есть)? Нет (n) ')
        else:
            for album in albums_to_move:
                id_for_album_to_move = re.findall('_([0-9]+$)', album)[0]
                album_ids.append(id_for_album_to_move)
    except IndexError:
        print('Неверная ссылка на альбом!')
        sys.exit()

    return album_ids, id_for_point_album


def reorder_albums(group_id, album_ids_to_move, id_for_point_album):
    """
    Changes the order of albums
    """
    print('...Выполняется перемещение альбомов...')

    for album_id in album_ids_to_move:
        time.sleep(2)
        response = requests.get(API_PATH + 'photos.reorderAlbums', params={'v': API_VERSION,
                                                                           'owner_id': group_id,
                                                                           'album_id': album_id,
                                                                           'before': id_for_point_album,
                                                                           'access_token': access_token})
        json_response = response.json()

        try:
            if json_response['response']:
                print('Альбом {} перемещен'.format(album_id))
        except KeyError:
            print('Код ошибки: {}. {}'.format(json_response['error']['error_code'], json_response['error']['error_msg']))


if __name__ == '__main__':
    parameters_dict = script_parameters()
    group_id = pull_group_id(parameters_dict['album_pointer'])
    album_ids_to_move, id_for_point_album = pull_album_ids(parameters_dict['albums_to_move'],
                                                           parameters_dict['album_pointer'], parameters_dict['mode'])
    reorder_albums(group_id, album_ids_to_move, id_for_point_album)
