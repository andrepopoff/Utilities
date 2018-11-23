import vk
import re

APP_ID = '6273721'


def reorder_albums(vk_api, group_id, album_ids_to_move, id_for_point_album):
    print('...Выполняется перемещение альбомов...')
    try:
        for album_id in album_ids_to_move:
            vk_api.photos.reorderAlbums(v='5.0', owner_id=group_id, album_id=album_id, before=id_for_point_album)
            print('Альбом с id {} перемещен'.format(album_id))
    except vk.exceptions.VkAPIError:
        print('Ошибка VkAPIError')


def learn_group_id(vk_api):
    link = input('Введите ссылку на группу: ')
    group_name = re.findall('vk.com/([\S]+$)', link)[0]
    group_id = vk_api.groups.getById(v='5.0', group_id=group_name)[0]['id']
    return -group_id


def connect_with_vk(app_id):
    login = input('Введите логин ВК: ')
    password = input('Введите пароль: ')
    vk_session = vk.AuthSession(app_id=app_id, user_login=login, user_password=password, scope='groups, photos')
    return vk.API(vk_session)


def find_album_id_by_reference():
    switch = True
    album_ids = []

    while switch:
        album_to_move = input('Введите ссылку на перемещаемый альбом: ')
        id_for_album_to_move = re.findall('_([0-9]+$)', album_to_move)[0]
        album_ids.append(id_for_album_to_move)
        response = input('Хотите переместить еще 1 альбом? (y/n) ')

        if response == 'n':
            switch = False

    point_album = input('Перед каким альбомом размещать? Введите ссылку: ')  # рядом с этим альбомом будет размещен альбом после перемещения
    id_for_point_album = re.findall('_([0-9]+$)', point_album)[0]

    return album_ids, id_for_point_album


if __name__ == '__main__':
    vk_api = connect_with_vk(APP_ID)
    group_id = learn_group_id(vk_api)
    album_ids_to_move, id_for_point_album = find_album_id_by_reference()
    reorder_albums(vk_api, group_id, album_ids_to_move, id_for_point_album)
