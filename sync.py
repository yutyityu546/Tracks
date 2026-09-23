import os
from github import Github
from github import Auth
from yt_dlp import YoutubeDL

token = os.environ.get("GH_PAT")
if not token:
    raise ValueError("Токен не найден!")

auth = Auth.Token(token)
g = Github(auth=auth)

REPO_NAME = "yutyityu546/Tracks"
SEARCH_QUERIES = [
    "ytsearch3: Пошлая Молли новинки",
    "ytsearch3: русский рэп новинки",
    "ytsearch3: mylancore remix"
]

repo = g.get_repo(REPO_NAME)
existing_files = set()

try:
    for f in repo.get_contents(""):
        if f.name.endswith(".mp3"):
            existing_files.add(f.name[:-4].lower().strip())
except Exception as e:
    print(f"Ошибка чтения репозитория: {e}")

ydl_opts = {
    "format": "bestaudio/best",
    "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
    "outtmpl": "%(title)s.%(ext)s",
    "quiet": True,
}

with YoutubeDL(ydl_opts) as ydl:
    for query in SEARCH_QUERIES:
        try:
            info = ydl.extract_info(query, download=False)
            for entry in info.get("entries", [info]):
                title = entry.get("title")
                clean_title = title.replace("/", "_").replace("\\", "_").strip()
                if clean_title.lower() in existing_files:
                    continue
                
                ydl.download([entry.get("webpage_url")])
                filename = f"{clean_title}.mp3"
                if os.path.exists(filename):
                    with open(filename, "rb") as f:
                        repo.create_file(path=filename, message=f"Auto-add: {filename}", content=f.read(), branch="main")
                    os.remove(filename)
                    existing_files.add(clean_title.lower())
        except Exception as e:
            print(f"Ошибка поиска: {e}")
