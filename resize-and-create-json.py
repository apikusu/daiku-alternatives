import json
import os
import subprocess
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed

indirs = ['anilist', 'tmdb']
quality = "90"
max_workers = os.cpu_count() or 4

# Cache for input image dimensions
dimension_cache = {}

def resize_image_task(input_path, output_path_base):
    sizes = [("large", 500), ("medium", 250), ("small", 100)]

    if input_path not in dimension_cache and shutil.which("sips"):
        result = subprocess.run(
            ["sips", "-g", "pixelWidth", "-g", "pixelHeight", input_path],
            capture_output=True, text=True, check=True
        )
        lines = result.stdout.splitlines()
        width = int(lines[1].split(":")[1].strip())
        height = int(lines[2].split(":")[1].strip())
        dimension_cache[input_path] = (width, height)

    for label, target_width in sizes:
        output_path = f"{output_path_base}{label}.jpg"

        if shutil.which("sips"):
            target_height = int((height / width) * target_width)
            temp_path = output_path + ".tmp.jpg"
            subprocess.run([
                "sips", "-z", str(target_height), str(target_width),
                input_path, "--out", temp_path
            ], check=True)
            os.rename(temp_path, output_path)
            print(f"Created: {output_path}")

        elif shutil.which("magick"):
            subprocess.run([
                "magick", input_path,
                "-resize", f"{target_width}x",
                "-quality", quality,
                output_path
            ], check=True)
            print(f"Created: {output_path}")

        else:
            raise RuntimeError("Neither 'sips' nor 'magick convert' found on this system.")

def collect_resize_jobs():
    jobs = []
    for inputdir in indirs:
        outdir = os.path.join('resized', inputdir)
        os.makedirs(outdir, exist_ok=True)

        for d in os.listdir(inputdir):
            subdir = os.path.join(inputdir, d)
            if not os.path.isdir(subdir):
                continue
            for f in os.listdir(subdir):
                if f in ('original.jpg', 'original.png', 'original.jpeg', 'original.webp'):
                    os.makedirs(f'{outdir}/{d}', exist_ok=True)
                    input_path = f'{inputdir}/{d}/{f}'
                    output_path_base = f'{outdir}/{d}/'
                    jobs.append((input_path, output_path_base))
    return jobs

def build_metadata():
    for inputdir in indirs:
        outdir = os.path.join('resized', inputdir)
        data = {}
        for id in os.listdir(inputdir):
            if os.path.isdir(os.path.join(inputdir, id)):
                data[id] = {}
                try:
                    covers = {
                        os.path.splitext(file)[0]: f'{id}/{file}'
                        for file in os.listdir(f'{outdir}/{id}')
                        if file.endswith('.jpg')
                    }
                except:
                    covers = None
                info_path = f'{inputdir}/{id}/infos.json'
                if os.path.exists(info_path):
                    with open(info_path, 'r') as info_file:
                        info = json.load(info_file)
                        data[id]["title"] = info.get('title')
                        data[id]["airingEpisodesOffset"] = info.get("airingEpisodesOffset")
                        data[id]["accentColor"] = info.get("accentColor")
                        data[id]["releaseTime"] = info.get("releaseTimeUTC")
                if covers:
                    data[id]["covers"] = covers
        with open(f'{outdir}/overrides.json', 'w') as f:
            json.dump({k: data[k] for k in sorted(data, key=int)}, f, indent=2)

if __name__ == "__main__":
    jobs = collect_resize_jobs()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(resize_image_task, inp, out) for inp, out in jobs]
        for future in as_completed(futures):
            future.result()  # raise exceptions if any

    build_metadata()
