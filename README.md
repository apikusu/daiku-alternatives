# anilist-alternative-posters

alternative anime posters for some anime from anilist (for use on daiku)

[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/apix0n/anilist-alternative-posters/publish.yml?label=resize%20images%20%26%20publish%20on%20'covers'%20branch)
](https://github.com/apix0n/anilist-alternative-posters/actions/workflows/publish.yml) 
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/apix0n/anilist-alternative-posters/covers)

the .json file containing relative links for alternative covers is available at 
```
https://raw.githubusercontent.com/apix0n/anilist-alternative-posters/refs/heads/covers/posters.json
```

the workflow is ran at each push to the `main` branch, and creates thumbnails for each `original.[jpg|jpeg|png]` file using ImageMagick.
