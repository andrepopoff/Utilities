import vk
import re

APP_ID = '6273721'


def reorder_albums(vk_api, group_id):
    try:
        vk_api.photos.reorderAlbums(v='5.0', owner_id=group_id, album_id=239340196, before=180568944)
        print('Операция успешно выполнена')
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


if __name__ == '__main__':
    vk_api = connect_with_vk(APP_ID)
    group_id = learn_group_id(vk_api)
    reorder_albums(vk_api, group_id)
