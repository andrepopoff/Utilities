#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import requests
import re
import os
import psycopg2

from vk_settings import API_PATH, BASE_TOKEN, API_VERSION


APP_ID = '6967460'
access_token = BASE_TOKEN  # Before you start, you need to get access_token
DATABASE_URL = os.environ['DATABASE_URL']
DB_CONNECT = psycopg2.connect(DATABASE_URL, sslmode='require')
DB_CURSOR = DB_CONNECT.cursor()


def get_group_id():
    if len(sys.argv) == 2:
        group_id_by_city = {'syk': -22426905, 'uht': -79007931, 'lub': 57199553}
        return group_id_by_city.get(sys.argv[1])


def get_all_albums(group_id):
    response = requests.get(API_PATH + 'photos.getAlbums', params={'v': API_VERSION, 'owner_id': group_id,
                                                                   'access_token': access_token})
    response_dict = response.json()
    if response_dict.get('response'):
        return response_dict['response']['items']
    else:
        print('response:', response_dict)
        return []


def get_state(owner_id):
    DB_CURSOR.execute('SELECT album_id FROM state WHERE owner_id=%s;', (owner_id,))
    return DB_CURSOR.fetchone()[0]


def save_state(album_id, owner_id):
    DB_CURSOR.execute('UPDATE state SET album_id = %s WHERE owner_id = %s;', (album_id, owner_id))
    DB_CONNECT.commit()


def prepare_data(album, group_id):
    if album['id'] not in (140958045, 215599660, 204790321):
        data = dict()
        title = data['title'] = album['title']
        description = data['description'] = album['description']
        data['message'] = title + '\n\n' + description if description else title
        data['group_url'] = 'https://vk.com/club' + str(group_id)[1:]
        data['attachment'] = 'album{}_{}'.format(group_id, album['id'])
        data['album_url'] = 'https://vk.com/' + data['attachment']
        data['signature'] = '\n\nАльбом: {}\nГруппа: {}'.format(data['album_url'], data['group_url'])
        data['message'] += data['signature']
        return data


def album_is_stopped(title, owner_id):
    stopped = re.findall(r'\bстоп\b', title, flags=re.I)
    if stopped:
        save_state(0, owner_id)
        print('Saved state 0. Started a new cycle')
        return True
    return False


def do_all(album, group_id, owner_id):
    data = prepare_data(album, group_id)
    if data:
        if album_is_stopped(data['title'], owner_id):
            sys.exit(0)

        response = requests.get(API_PATH + 'wall.post', params={'v': API_VERSION, 'owner_id': owner_id,
                                                                'access_token': access_token,
                                                                'from_group': 1, 'message': data['message'],
                                                                'attachments': data['attachment']})
        save_state(album['id'], owner_id)
        print(response.json())
        return True
    else:
        return False


if __name__ == '__main__':
    owner_id = get_group_id()
    album_idx = 0
    posted_album_id = get_state(owner_id)

    if owner_id:
        group_id = owner_id if owner_id < 0 else -22426905
        all_albums = get_all_albums(group_id)

        for num, album in enumerate(all_albums):
            if not posted_album_id or album_idx and num == album_idx:
                print('bench', 1)
                answer = do_all(album, group_id, owner_id)
                if answer:
                    break
                else:
                    continue
            elif album['id'] == posted_album_id:
                print('bench', 2)
                album_idx = num + 1
                continue
