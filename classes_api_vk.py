import time
import requests


class User:
    def __init__(self, access_token, user_id, user_name=None, user_last_name=None, friends=None, info=None,
                 mistake=None):
        self.access_token = access_token
        self.user_name = user_name
        self.user_last_name = user_last_name
        self.friends = friends
        self.user_id = user_id
        self.info = info
        self.mistake = mistake

    def __str__(self):
        return f'https://vk.com/id{self.user_id}'

    def get_params(self):
        return dict(
            access_token=self.access_token,
            v='5.52',
            user_id=self.user_id
        )

    def checking(self):
        params = self.get_params()
        response = requests.get(
            'https://api.vk.com/method/users.get',
            params
        )
        self.info = response.json().keys()
        if self.info == {'error'}:
            self.mistake = 'error'
            self.mistake = response.json()[self.mistake]['error_msg']
            if self.mistake == 'User authorization failed: invalid access_token (4).':
                self.mistake = 'Введен не верный Access Token...'
                raise SystemExit(self.mistake)
            else:
                self.mistake = 'Пустой Access Token или что-то пошло не так...'
                raise SystemExit(self.mistake)
        elif self.info == {'response'}:
            self.mistake = 'response'
            self.mistake = response.json()[self.mistake]  # [0]#['deactivated']

            try:
                if not self.mistake:
                    self.mistake = f'Пользователь не существует: {self.user_id}'
                    raise SystemExit(self.mistake)
                elif not self.mistake[0]['deactivated']:
                    self.mistake = f'Пользователь {self.user_id} проверен, продолжаем...'
                else:
                    self.mistake = f'Пользователь удален или отключен: {self.user_id}'
                    raise SystemExit(self.mistake)
            except KeyError:
                self.mistake = f'Пользователь {self.user_id} проверен, продолжаем...'

        return self.mistake

    def get_info(self):
        params = self.get_params()
        response = requests.get(
            'https://api.vk.com/method/users.get',
            params
        )
        self.user_name = response.json()['response'][0]['first_name']
        self.user_last_name = response.json()['response'][0]['last_name']
        return response.json()

    def get_friends(self):
        params = self.get_params()
        response = requests.get(
            'https://api.vk.com/method/friends.get',
            params
        )
        self.friends = response.json()['response']['items']
        return response.json()


def check_token_user(access_token, user_id):
    print(f'Сначала проверим введенные данные для пользователя {user_id}:')
    user = User(access_token, user_id)
    user.checking()
    print(user.mistake)


def main():
    access_token = input('Введите Access Token: ')
    users = input('Введите ID пользователей для сравнения через & (например, 16168864 & 35982287): ').replace(" ", "").split("&")
    if len(users) != 2:
        raise SystemExit('Нужно ввести 2-х пользователей для сравения...')
    user_length = 1
    friends_list = list()
    try:
        for user_id in users:
            check_token_user(access_token, user_id)
            # if user_length < 10:
            #     user_key = f"user_0{user_length}"
            # else:
            #     user_key = f"user_0{user_length}"
            user = User(access_token, user_id)
            user.get_friends()
            friends_list.append(user.friends)
            user_length += 1
            time.sleep(0.5)

        print('И так, начинаем искать общих друзей: ')
        time.sleep(0.5)
        for friend_one_user in friends_list[0]:
            for friend_another_user in friends_list[1]:
                if friend_one_user == friend_another_user:
                    user_id = friend_one_user
                    friend = User(access_token, user_id)
                    friend.get_info()
                    print(friend.user_name, friend.user_last_name, friend)
                    time.sleep(0.5)
        print('\nПрограмма завершена.')

    except IndexError:
        raise SystemExit('Нужно ввести 2-х пользователей для сравения...')

main()