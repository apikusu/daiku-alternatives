import json
import os
import subprocess

os.makedirs('./resized', exist_ok=True)

target_size = "250x"
quality = "90%"
target_name = "medium.jpg"

for d in os.listdir('./anime'):
    files = os.listdir('./anime/' + d)
    for f in files:
        if f == 'original.jpg' or f == 'original.png' or f == 'original.jpeg':
            os.makedirs(f'./resized/{d}', exist_ok=True)
            input_path = f'./anime/{d}/{f}'
            output_path = f'./resized/{d}/{target_name}'
            subprocess.run(['convert', input_path, '-resize', target_size, '-quality', quality, output_path])
            print(f'converted {input_path} to {output_path}')

data = {id: f'../{id}/medium.jpg' for id in os.listdir('./resized')}
with open('resized/posters.json', 'w') as f:
    f.write(json.dumps(data, sort_keys=True, indent=2))