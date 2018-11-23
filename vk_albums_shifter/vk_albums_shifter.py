import vk

GROUP_ID = '-54705114'


def reorder_albums(group_id, app_id='6273721'):
    login = input('Введите логин ВК: ')
    password = input('Введите пароль: ')

    vk_session = vk.AuthSession(app_id=app_id, user_login=login, user_password=password, scope='groups, photos')
    vk_api = vk.API(vk_session)

    try:
        vk_api.photos.reorderAlbums(v='5.0', owner_id=group_id, album_id=239330927, before=180568944)
        print('Операция успешно выполнена')
    except vk.exceptions.VkAPIError:
        print('Ошибка VkAPIError')

if __name__ == '__main__':
    reorder_albums(GROUP_ID)
