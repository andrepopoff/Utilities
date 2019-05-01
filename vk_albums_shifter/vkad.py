import sys

APP_ID = '6273721'
API_PATH = 'https://api.vk.com/method/'
API_VERSION = 5.52
access_token = ''  # Before you start, you need to get access_token


def get_group():
    if len(sys.argv) == 2:
        group_id_by_city = {'syk': 123, 'uht': 123}
        group_id = group_id_by_city[sys.argv[1]]


if __name__ == '__main__':
    group = get_group()
    if group:
        pass
