"""
This script changes the order of the albums in the group on vk.com.
The script is useful, who has commercial groups on vk.com with a large number of albums.
This eliminates the routine of dragging albums with the PC mouse.
"""

import vk
import re
import sys

APP_ID = '6273721'


def reorder_albums(vk_api, group_id, album_ids_to_move, id_for_point_album):
    """
    Changes the order of albums
    """
    print('...Выполняется перемещение альбомов...')
    try:
        for album_id in album_ids_to_move:
            vk_api.photos.reorderAlbums(v='5.0', owner_id=group_id, album_id=album_id, before=id_for_point_album)
            print('Альбом {} перемещен'.format(album_id))
    except vk.exceptions.VkAPIError:
        print('Ошибка VkAPIError')


def pull_group_id(vk_api, link):
    """
    Link to group --> group id
    """
    try:
        group_name = re.findall('vk.com/([\S]+$)', link)[0]
        group_id = vk_api.groups.getById(v='5.0', group_id=group_name)[0]['id']
    except IndexError:
        print('Вы ввели неверную ссылку на группу!')
        sys.exit()
    return -group_id


def connect_with_vk(app_id):
    """
    Authorization on vk.com
    """
    try:
        login = input('Введите логин ВК: ')
        password = input('Введите пароль: ')
        vk_session = vk.AuthSession(app_id=app_id, user_login=login, user_password=password, scope='groups, photos')
    except vk.exceptions.VkAuthError:
        print('Неправильный логин или пароль!')
        sys.exit()
    return vk.API(vk_session)


def pull_album_ids(albums_to_move, album_pointer, mode):
    """
    Links to albums on vk.com --> album ids
    """
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

    id_for_point_album = re.findall('_([0-9]+$)', album_pointer)[0]

    return album_ids, id_for_point_album


def script_parameters():
    """
    Creates parameters for further script operation.
    Parameters differ depending on the method of calling the script.
    """
    if len(sys.argv) == 1:
        mode = 0
        group_link = input('Введите ссылку на группу: ')
        albums_to_move = input('Введите ссылку на перемещаемый альбом: ')
        album_pointer = input('Перед каким альбомом размещать? Введите ссылку: ')
    else:
        mode = 1
        group_link = input('Введите ссылку на группу: ')
        albums_to_move = sys.argv[2:]
        album_pointer = sys.argv[1]
    return {
        'mode': mode,
        'group_link': group_link,
        'albums_to_move': albums_to_move,
        'album_pointer': album_pointer
    }


if __name__ == '__main__':
    vk_api = connect_with_vk(APP_ID)
    parameters_dict = script_parameters()
    group_id = pull_group_id(vk_api, parameters_dict['group_link'])
    album_ids_to_move, id_for_point_album = pull_album_ids(parameters_dict['albums_to_move'],
                                                           parameters_dict['album_pointer'], parameters_dict['mode'])
    reorder_albums(vk_api, group_id, album_ids_to_move, id_for_point_album)
