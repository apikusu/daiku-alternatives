import requests
import os

# Read the markdown file
with open('resized/readme.md', 'r', encoding='utf-8') as f:
    markdown_content = f.read()

# Request GitHub API to convert markdown to HTML
url = 'https://api.github.com/markdown'
headers = {'Accept': 'application/vnd.github+json'}

github_token = os.getenv('GITHUB_TOKEN')
if github_token:
    headers['Authorization'] = f'Bearer {github_token}'

response = requests.post(url, json={'text': markdown_content}, headers=headers)

if response.status_code == 200:
    html_content = \
"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>apix's daiku-alternatives</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.8.1/github-markdown.min.css">
    <style>
        .markdown-body {
            box-sizing: border-box;
            min-width: 200px;
            max-width: 980px;
            margin: 0 auto;
            padding: 45px;
        }
    
        @media (max-width: 767px) {
            .markdown-body {
                padding: 15px;
            }
        }

        .anchor {
            display: none;
        }
    
        </style>
</head>
<body class="markdown-body">"""
    html_content += response.text
    html_content += \
"""</body>
</html>"""
    
    # Save the HTML content
    with open('resized/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("HTML file created successfully at resized/index.html")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
