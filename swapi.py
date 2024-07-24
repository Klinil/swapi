import requests
from pathlib import Path


class APIRequester:

    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, url):
        if url == self.base_url:
            url = str(self.base_url) + '/'
        else:
            url = f"{self.base_url}{url}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError:
            print('HTTP ошибка')
        except requests.exceptions.ConnectionError:
            print('Ошибка соединения')
        except requests.exceptions.Timeout:
            print('Timeout Error')
        except requests.exceptions.RequestException:
            print('Возникла ошибка при выполнении запроса')


class SWRequester(APIRequester):

    def __init__(self, base_url):
        super().__init__(base_url)

    def get_sw_categories(self) -> list:
        response = self.get(self.base_url)
        if response.status_code != 200:
            print('Ошибка получения категорий')
            return []
        else:
            return response.json().keys()

    def get_sw_info(self, sw_type) -> str:
        response = self.get(f'/{sw_type}/')
        return response.text


def save_sw_data():

    sw_requester = SWRequester('https://swapi.dev/api')

    Path('data').mkdir(exist_ok=True)

    for category in sw_requester.get_sw_categories():
        with open(f'data/{category}.txt', 'w') as f:
            f.write(sw_requester.get_sw_info(category))


save_sw_data()
