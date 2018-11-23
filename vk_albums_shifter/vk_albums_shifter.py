import vk
import re

GROUP_ID = '-54705114'
APP_ID = '6273721'


def reorder_albums(vk_api, group_id):
    try:
        vk_api.photos.reorderAlbums(v='5.0', owner_id=group_id, album_id=239117516, before=180568944)
        print('Операция успешно выполнена')
    except vk.exceptions.VkAPIError:
        print('Ошибка VkAPIError')


def learn_group_id(link):
    # vk_response = vk_api
    pass


def connect_with_vk(app_id):
    login = input('Введите логин ВК: ')
    password = input('Введите пароль: ')
    vk_session = vk.AuthSession(app_id=app_id, user_login=login, user_password=password, scope='groups, photos')
    return vk.API(vk_session)


if __name__ == '__main__':
    vk_api = connect_with_vk(APP_ID)
    link = input('Введите ссылку на группу: ')
    learn_group_id(link)

    reorder_albums(vk_api, GROUP_ID)
