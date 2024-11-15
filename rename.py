import os
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3


def rename_mp3_files(media_dir):
    for filename in os.listdir(media_dir):
        full_path = os.path.join(media_dir, filename)

        if not filename.endswith(".mp3"):
            continue

        try:
            audio = MP3(full_path, ID3=EasyID3)
            title = audio.get("title", [None])[0]

            if title:
                sanitized_title = "".join(c for c in title if c.isalnum() or c in " -_").rstrip()
                new_path = os.path.join(media_dir, f"{sanitized_title}.mp3")

                if full_path == new_path:
                    print(f"File '{filename}' already has the correct name.")
                    continue

                os.rename(full_path, new_path)
                print(f"Renamed '{filename}' to '{sanitized_title}.mp3'")

            else:
                print(f"No title tag found for '{filename}', skipping.")

        except Exception as e:
            print(f"Could not process '{filename}': {e}")