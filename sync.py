import os
from yt_dlp import YoutubeDL

REPO_URL = "https://github.com/yutyityu546/Tracks.git"
SEARCH_QUERIES = [
    "ytsearch3: Пошлая Молли новинки",
    "ytsearch3: русский рэп новинки",
    "ytsearch3: mylancore remix"
]

# Получаем список уже существующих файлов в папке
existing_files = set()
for f in os.listdir("."):
    if f.endswith(".mp3"):
        existing_files.add(f[:-4].lower().strip())

ydl_opts = {
    "format": "bestaudio/best",
    "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
    "outtmpl": "%(title)s.%(ext)s",
    "quiet": True,
}

downloaded_any = False

with YoutubeDL(ydl_opts) as ydl:
    for query in SEARCH_QUERIES:
        try:
            info = ydl.extract_info(query, download=False)
            for entry in info.get("entries", [info]):
                title = entry.get("title")
                clean_title = title.replace("/", "_").replace("\\", "_").strip()
                if clean_title.lower() in existing_files:
                    continue
                
                print(f"Скачиваем: {clean_title}")
                ydl.download([entry.get("webpage_url")])
                downloaded_any = True
                existing_files.add(clean_title.lower())
        except Exception as e:
            print(f"Ошибка поиска: {e}")

# Если скачались новые треки, просто заливаем их через стандартные git-команды
if downloaded_any:
    os.system("git config --global user.name 'GitHub Action Bot'")
    os.system("git config --global user.email 'action@github.com'")
    os.system("git add *.mp3")
    os.system("git commit -m 'Auto-add new music tracks'")
    os.system(f"git push https://x-access-token:{os.environ.get('GITHUB_TOKEN')}@github.com/yutyityu546/Tracks.git main")
    print("Все треки успешно улетели на GitHub!")
else:
    print("Новых треков для скачивания не найдено.")
