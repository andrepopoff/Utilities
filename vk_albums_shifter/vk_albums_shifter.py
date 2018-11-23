import vk

MY_USER_ID = '7978511'
APP_ID = '6273721'
GROUP_ID = '-54705114'

with open('login_details.txt', 'r') as f:
    login, password = [line.rstrip() for line in f]

vk_session = vk.AuthSession(app_id=APP_ID, user_login=login, user_password=password, scope='groups, photos')
vk_api = vk.API(vk_session)

try:
    vk_api.photos.reorderAlbums(v='5.0', owner_id=GROUP_ID, album_id=239117930, before=180568944)
    print('Операция успешно выполнена')
except vk.exceptions.VkAPIError:
    print('Ошибка VkAPIError')
