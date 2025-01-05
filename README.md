# daiku-alternatives

alternative anime posters and titles for some anime on anilist (for use on daiku).
this is a personal repository / if i don't like the cover/title anilist put, i'll replace it myself.

[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/apix0n/anilist-alternative-posters/publish.yml?label=resize%20images%20%26%20publish%20on%20'covers'%20branch)
](https://github.com/apix0n/anilist-alternative-posters/actions/workflows/publish.yml) 
[![last commit](https://img.shields.io/github/last-commit/apix0n/anilist-alternative-posters/covers)](https://github.com/apix0n/anilist-alternative-posters/commits/main)

the .json file containing relative links for alternative covers is available at 
```
https://raw.githubusercontent.com/apix0n/anilist-alternative-posters/refs/heads/alternatives/overrides.json
```

the workflow is ran at each push to the `main` branch, and creates thumbnails for each `original.[jpg|jpeg|png]` file using ImageMagick.
