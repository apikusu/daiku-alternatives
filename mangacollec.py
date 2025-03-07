import json
import os

dir = "mangacollec"

series_dir = os.path.join(dir, "series")
series_files = [f.replace('.json', '') for f in os.listdir(series_dir) if f.endswith('.json')]

editions_dir = os.path.join(dir, "editions")
editions_files = [f.replace('.json', '') for f in os.listdir(editions_dir) if f.endswith('.json')]

data = {}

if len(series_files) > 0:
    data["series"] = {}
    for series in series_files:
        data["series"][series] = {}
        with open(os.path.join(series_dir, series + ".json"), "r") as overrides_file:
            overrides = json.load(overrides_file)
            if overrides["title"]:
                data["series"][series]["title"] = overrides["title"]

if len(editions_files) > 0:
    data["editions"] = {}
    for edition in editions_files:
        data["editions"][edition] = {}
        with open(os.path.join(editions_dir, edition + ".json"), "r") as overrides_file:
            overrides = json.load(overrides_file)
            if "series" in overrides:
                data["editions"][edition]["series"] = overrides["series"]

with open(f'resized/mangacollec.json', 'w') as f:
        f.write(json.dumps(data, indent=2))