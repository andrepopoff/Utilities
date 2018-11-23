import vk
import re

GROUP_ID = '-54705114'
APP_ID = '6273721'


def reorder_albums(login, password, group_id, app_id):
    vk_session = vk.AuthSession(app_id=app_id, user_login=login, user_password=password, scope='groups, photos')
    vk_api = vk.API(vk_session)

    try:
        vk_api.photos.reorderAlbums(v='5.0', owner_id=group_id, album_id=239330927, before=180568944)
        print('Операция успешно выполнена')
    except vk.exceptions.VkAPIError:
        print('Ошибка VkAPIError')


def get_info_about_the_group(link):
    pass


if __name__ == '__main__':
    login = input('Введите логин ВК: ')
    password = input('Введите пароль: ')
    link = input('Введите ссылку на группу: ')

    reorder_albums(login, password, GROUP_ID, APP_ID)
