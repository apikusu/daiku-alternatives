import requests
import re
import json
import os

def search_anilist(query):
    # GraphQL endpoint
    url = 'https://graphql.anilist.co'
    
    # Handle direct ID input
    id_match = re.match(r'id:(\d+)', query)
    if id_match:
        media_id = id_match.group(1)
        # GraphQL query for direct ID lookup
        query_str = '''
        query ($id: Int) {
            Media (id: $id) {
                id
                title {
                    romaji
                    english
                    native
                }
                type
            }
        }
        '''
        variables = {'id': int(media_id)}
    else:
        # GraphQL query for search
        query_str = '''
        query ($search: String) {
            Page (page: 1, perPage: 10) {
                media (search: $search) {
                    id
                    title {
                        romaji
                        english
                        native
                    }
                    type
                }
            }
        }
        '''
        variables = {'search': query}

    # Make the HTTP request
    response = requests.post(url, json={'query': query_str, 'variables': variables})
    return response.json()

def display_results(data):
    if 'errors' in data:
        print("Error:", data['errors'][0]['message'])
        return None
    
    if 'Media' in data['data']:
        # Single result from ID search
        media = data['data']['Media']
        print(f"1. {media['title']['romaji']} ({media["type"]} / {media['id']})")
        return [media]
    else:
        # Multiple results from search
        results = data['data']['Page']['media']
        if not results:
            print("No results found.")
            return None
        
        for i, media in enumerate(results, 1):
            print(f"{i}. {media['title']['romaji']} ({media["type"]} / {media['id']})")
        return results

def save_override(media_id, override_title):
    # Create directory structure
    directory = f"anilist/{media_id}"
    os.makedirs(directory, exist_ok=True)
    
    # Prepare the data
    info_data = {
        "title": override_title
    }
    
    # Save to JSON file
    filepath = f"{directory}/infos.json"
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(info_data, f, ensure_ascii=False, indent=4)
    print(f"\nOverride saved to {filepath}")

def get_mal_info(title, type_media):
    base_url = "https://api.jikan.moe/v4/anime" if type_media == "ANIME" else "https://api.jikan.moe/v4/manga"
    response = requests.get(f"{base_url}?q={title}&limit=1")
    
    if response.status_code == 200:
        data = response.json()
        if data['data'] and len(data['data']) > 0:
            result = data['data'][0]
            return {
                'id': result['mal_id'],
                'title_english': result['title_english']
            }
    return None

def main():
    query = input("Enter search term or id:{number}: ")
    results = search_anilist(query)
    media_list = display_results(results)
    
    if media_list and len(media_list) > 0:
        selected_id = None
        if len(media_list) > 1:
            while True:
                try:
                    choice = int(input("Select a number: "))
                    if 1 <= choice <= len(media_list):
                        selected = media_list[choice - 1]
                        print(f"\nSelected: {selected['title']['romaji']} (ID: {selected['id']})")
                        selected_id = selected['id']
                        break
                    else:
                        print("Invalid selection. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")
        else:
            selected = media_list[0]
            print(f"\nSelected: {selected['title']['romaji']} (ID: {selected['id']})")
            selected_id = selected['id']
        
        if selected_id:
            # Get MAL info
            selected = media_list[0] if len(media_list) == 1 else media_list[choice - 1]
            mal_info = get_mal_info(selected['title']['romaji'], selected['type'])
            
            if mal_info and mal_info['title_english']:
                print(f"\nMAL ID: {mal_info['id']}")
                print(f"MAL English Title: {mal_info['title_english']}")
                use_mal = input("Use MAL English title as override? (y/n): ").lower() == 'y'
                
                if use_mal:
                    override_title = mal_info['title_english']
                else:
                    override_title = input("\nEnter override title: ")
            else:
                print("\nNo MAL information found")
                override_title = input("\nEnter override title: ")
                
            save_override(selected_id, override_title)
            return selected_id
    return None

if __name__ == "__main__":
    main()