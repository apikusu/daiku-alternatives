# daiku-alternatives

alternative anime posters and titles for some anime on anilist (for use on daiku).

[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/apix0n/daiku-alternatives/publish.yml?label=resize%20images%20%26%20publish%20on%20'alternatives'%20branch)
](https://github.com/apix0n/daiku-alternatives/actions/workflows/publish.yml) 
[![last commit](https://img.shields.io/github/last-commit/apix0n/daiku-alternatives/alternatives?label=last%20update)](https://github.com/apix0n/daiku-alternatives/commits/main)

this is a personal repository: if i don't like the cover/title anilist put, i'll replace it myself.

----------

the readme showing deployed overrides is available [here](https://github.com/apix0n/daiku-alternatives/tree/alternatives?tab=readme-ov-file#daiku-alternatives).

the .json file containing relative links for alternative covers & title overrides (if available) is available at:
```
https://raw.githubusercontent.com/apix0n/daiku-alternatives/refs/heads/alternatives/overrides.json
```

the workflow is ran at each push to the `main` branch, and creates thumbnails (`[large|medium|small].jpg`) for each `original.[jpg|jpeg|png|webp]` file using ImageMagick to the `alternatives` branch.