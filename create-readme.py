import json
import os
from datetime import datetime, timezone

with open(f'./resized/anilist/overrides.json') as f:
    file = json.load(f)

anime_overrides_text = ''''''
tmdb_overrides_text = ''''''

for anime_id in file.keys():
    anime_overrides_count = len(file)
    title = file[anime_id].get('title')
    if title:
        text = f'''### {anime_id} - as `{title}`

'''
    else:
        text = f'''### {anime_id}

'''
    covers = file[anime_id].get('covers', {})
    airingEpisodesOffset = file[anime_id].get('airingEpisodesOffset', None)
    accentColor = file[anime_id].get("accentColor", None)
    releaseTime = file[anime_id].get("releaseTime", None)
    if covers:
        text += f'<img align="right" src="anilist/{covers.get("small")[3:]}" height="100px">\n\n'
        text += '* cover:\n'
        for key, value in covers.items():
            text += f'  * `{key}`: [anilist/{value[3:]}](anilist/{value[3:]})\n'
    else:
        text += '* no cover override\n'

    if airingEpisodesOffset:
        text += f'* airing episodes offset: `{int(airingEpisodesOffset):+}`\n' # :+ so it always prints the + sign

    if releaseTime:
        text += f'* release time override: `{releaseTime[0]}:{releaseTime[1] if len(releaseTime) > 1 else '00'} UTC`\n' # :+ so it always prints the + sign
    
    if accentColor:
        text += f'* accent color: ![{accentColor}](https://singlecolorimage.com/get/{accentColor[1:]}/10x10) `{accentColor}`\n'

    readme_path = f'./anilist/{anime_id}/readme.txt'
    if os.path.exists(readme_path):
        with open(readme_path, 'r') as readme_file:
            readme_content = readme_file.read().strip()
            text += f'* change note:\n```\n{readme_content}\n```\n'
    
    anime_overrides_text += text + f'\n' # break a line after each override

with open(f'./resized/tmdb/overrides.json') as f:
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
        text += f'<img align="right" src="tmdb/{covers.get("small")[3:]}" height="100px">\n\n'
        text += '* cover:\n'
        for key, value in covers.items():
            text += f'  * `{key}`: [tmdb/{value[3:]}](tmdb/{value[3:]})\n'
    else:
        text += '* no cover override\n'
    
    readme_path = f'./tmdb/{tmdb_id}/readme.txt'
    if os.path.exists(readme_path):
        with open(readme_path, 'r') as readme_file:
            readme_content = readme_file.read().strip()
            text += f'* change note:\n```\n{readme_content}\n```\n'
    
    tmdb_overrides_text += text + f'\n' # break a line after each override

mdtext = f'''# daiku-alternatives

last updated at: `{datetime.now(timezone.utc).strftime('%B %d, %Y %H:%M')} UTC`

total anilist overrides count: `{anime_overrides_count}`

total tmdb overrides count: `{tmdb_overrides_count}`

## anilist overrides

{anime_overrides_text}

## tmdb overrides

{tmdb_overrides_text}
'''

with open('./resized/readme.md', 'w') as f:
    f.write(mdtext)
