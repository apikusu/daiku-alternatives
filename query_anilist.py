import requests

def query_anilist(id_list):
    url = 'https://graphql.anilist.co'
    chunk_size = 50
    results = {}
    
    for i in range(0, len(id_list), chunk_size):
        chunk = id_list[i:i + chunk_size]
        
        query = '''
        query Media($idIn: [Int]) {
            Page {
                media(id_in: $idIn) {
                    id
                    title {
                        english
                        romaji
                    }
                    type
                    siteUrl
                }
            }
        }
        '''
        
        response = requests.post(url, json={'query': query, 'variables': {'idIn': chunk}})
        
        if response.status_code == 200:
            data = response.json()
            for item in data['data']['Page']['media']:
                title = item['title']['english'] or item['title']['romaji']
                type_info = item['type'] if item['type'] == 'MANGA' else ""
                results[item['id']] = {
                    'title': title,
                    'type': type_info,
                    'url': item['siteUrl']
                }
    
    return results