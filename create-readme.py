import json
import os
from datetime import datetime, timezone
from query_anilist import query_anilist

with open(f'./resized/anilist/overrides.json', encoding='utf-8') as f:
    file = json.load(f)
    anime_data = query_anilist(list(file.keys()))

anime_overrides_text = ''''''
tmdb_overrides_text = ''''''

for anime_id in file.keys():
    anime_id_int = int(anime_id)  # Ensure the key is an integer
    anime_overrides_count = len(file)
    text = f'''### {anime_data[anime_id_int]["type"]} [`{anime_id}`]({anime_data[anime_id_int]["url"]}) {anime_data[anime_id_int]["title"]}

'''
    covers = file[anime_id].get('covers', {})
    title = file[anime_id].get('title')
    airingEpisodesOffset = file[anime_id].get('airingEpisodesOffset', None)
    accentColor = file[anime_id].get("accentColor", None)
    releaseTime = file[anime_id].get("releaseTime", None)
    if covers:
        text += f'<img align="right" src="anilist/{covers.get("small")}" height="100px">\n\n'
        text += '* cover:\n'
        for key, value in covers.items():
            text += f'  * `{key}`: [anilist/{value}](anilist/{value})\n'

    if title:
        text += f'* title: `{title}`\n'

    if airingEpisodesOffset:
        text += f'* airing episodes offset: `{int(airingEpisodesOffset):+}`\n' # :+ so it always prints the + sign

    if releaseTime:
        text += f'* release time override: `{releaseTime[0]}:{releaseTime[1] if len(releaseTime) > 1 else '00'} UTC`\n' # :+ so it always prints the + sign
    
    if accentColor:
        text += f'* accent color: ![{accentColor}](https://singlecolorimage.com/get/{accentColor[1:]}/10x10) `{accentColor}`\n'

    readme_path = f'./anilist/{anime_id}/readme.txt'
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as readme_file:
            readme_content = readme_file.read().strip()
            text += f'* change note:\n```\n{readme_content}\n```\n'
    
    anime_overrides_text += text + f'\n' # break a line after each override

with open(f'./resized/tmdb/overrides.json', encoding='utf-8') as f:
    file = json.load(f)

for tmdb_id in file.keys():
    tmdb_overrides_count = len(file)
    title = file[tmdb_id].get('title')
    if title:
        text = f'''### {tmdb_id} - as `{title}`

'''
    else:
        text = f'''### {tmdb_id}

'''
    covers = file[tmdb_id].get('covers', {})
    airingEpisodesOffset = file[tmdb_id].get('airingEpisodesOffset', None)
    if covers:
        text += f'<img align="right" src="tmdb/{covers.get("small")}" height="100px">\n\n'
        text += '* cover:\n'
        for key, value in covers.items():
            text += f'  * `{key}`: [tmdb/{value}](tmdb/{value})\n'
    else:
        text += '* no cover override\n'
    
    readme_path = f'./tmdb/{tmdb_id}/readme.txt'
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as readme_file:
            readme_content = readme_file.read().strip()
            text += f'* change note:\n```\n{readme_content}\n```\n'
    
    tmdb_overrides_text += text + f'\n' # break a line after each override

mdtext = f'''# daiku-alternatives

last updated at: `{datetime.now(timezone.utc).strftime('%B %d, %Y %H:%M')} UTC`

## AniList overrides ({anime_overrides_count})

{anime_overrides_text}

## TMDB overrides ({tmdb_overrides_count})

{tmdb_overrides_text}

---
### made by [apix](https://github.com/apix0n) at [apikusu/daiku-alternatives](https://github.com/apikusu/daiku-alternatives) | this file is auto-generated
'''

with open('./resized/readme.md', 'w', encoding="utf-8") as f:
    f.write(mdtext)
