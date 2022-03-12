import requests
from rich.console import Console
console = Console()
API_URL = 'https://graphql.anilist.co'

class Anime:

    def __init__(self, data):
        try:
            self.id = data['id']
            self.idMal = data['idMal']
            self.title_romaji = data['title']['romaji']
            self.title_english = data['title']['english']
        except Exception: #boş gelirse data
            pass
        
class Character:

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']['userPreferred']
        self.image = data['image']['large']
        self.gender = data['gender']
        self.age = data['age']
        self.favourites = data['favourites']
        self.siteUrl = data['siteUrl']

    def picture_data(self):
        response = requests.get(self.image)
        return response.content

    def __repr__(self):
        return f'{self.name} at age {self.age}, favs = {self.favourites}'

class GET:
    def media_anime(search_name):
        q = '''
        query($name: String){
            Media(search: $name, sort: FAVOURITES_DESC, type: ANIME)
            {
                id
                idMal
                title
                {
                    romaji
                    english
                }
            }
        }
        '''
        v = {'name': search_name}
        response = requests.post(API_URL, json={'query': q, 'variables': v})
        data = response.json()['data']
        return Anime(data['Media'])
    
    def charaterlist_from_anime(anime_id, count):
        list_of_characters = []
        last_page = (count // 25) + 1
        for page in range(1, last_page + 1):
            q = '''
            query($id: Int, $page: Int, $perPage: Int){
                Media(id: $id) {
                    characters(sort: FAVOURITES_DESC, page: $page, perPage: $perPage) {
                    nodes {
                        id
                        name {
                        userPreferred
                        }
                        image {
                            large
                        }
                        gender
                        age
                        favourites
                        siteUrl
                    }
                    }
                }
            }
            '''
            v = {'id' : anime_id, 'page': page, 'perPage': 25 if page != last_page else count % 25}
            response = requests.post(API_URL, json={'query': q, 'variables': v})
            if response.status_code != 200:
                console.print_exception(f'Hata {response.status_code}')
            data = response.json()['data']
            for sub_data in data['Media']['characters']['nodes']:
                list_of_characters.append(Character(sub_data))
        
        return list_of_characters

if __name__ == '__main__':
    console.print_exception('You are trying to run wrong app')