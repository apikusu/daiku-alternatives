import json
import os
from datetime import datetime, timezone

with open(f'./resized/overrides.json') as f:
    file = json.load(f)

anime_overrides_text = ''''''

for anime_id in file.keys():
    title = file[anime_id].get('title')
    if title:
        text = f'''### {anime_id} - as `{title}`

'''
    else:
        text = f'''### {anime_id}

'''
    covers = file[anime_id].get('covers', {})
    if covers:
        text += f'<img align="right" src="{covers.get("small")[3:]}" height="80px">\n\n'
        for key, value in covers.items():
            text += f'* `size: {key}`: [{value[3:]}]({value[3:]})\n'
    else:
        text += '* no cover override\n'
    
    readme_path = f'./anilist/{anime_id}/readme.txt'
    if os.path.exists(readme_path):
        with open(readme_path, 'r') as readme_file:
            readme_content = readme_file.read().strip()
            text += f'* change description:\n```\n{readme_content}\n```\n'
    
    anime_overrides_text += text + f'\n' # break a line after each override

mdtext = f'''# daiku-alternatives

last updated at: `{datetime.now(timezone.utc).strftime('%B %d, %Y %H:%M')} UTC`

total anilist overrides count: `{len(file)}`

## anilist overrides

{anime_overrides_text}
'''

with open('./resized/readme.md', 'w') as f:
    f.write(mdtext)