import requests

client_id = '52091976'
client_secret = 'e5EbLZzbqsnqwFfKHsIt'
redirect_uri = 'https://decisionss.ru/callback'

def get_auth_url():
    auth_url = f'https://oauth.vk.com/authorize?client_id={client_id}&display=page&redirect_uri={redirect_uri}&scope=email&response_type=code'
    return auth_url

def get_access_token(code):
    token_url = 'https://oauth.vk.com/access_token'
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'code': code
    }
    response = requests.get(token_url, params=params)
    if response.status_code == 200:
        access_token = response.json()['access_token']
        return access_token
    else:
        print(f'Ошибка: {response.status_code}')
        return None

def get_user_data(access_token):
    user_url = 'https://api.vk.com/method/users.get'
    params = {
        'access_token': access_token,
        'v': '5.131'
    }
    response = requests.get(user_url, params=params)
    if response.status_code == 200:
        user_data = response.json()['response'][0]
        return user_data
    else:
        print(f'Ошибка: {response.status_code}')
        return None