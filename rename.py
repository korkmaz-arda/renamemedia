import os
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC


def rename_media_files(media_dir, accepted_formats=['mp3', 'flac']):
    for filename in os.listdir(media_dir):
        full_path = os.path.join(media_dir, filename)

        file_extension = filename.split('.')[-1].lower()

        if file_extension not in accepted_formats:
            continue

        try:
            if file_extension == "mp3":
                audio = MP3(full_path, ID3=EasyID3)
            elif file_extension == "flac":
                audio = FLAC(full_path)
            else:
                print(f"Skipping unsupported file format '{filename}'")
                continue

            title = audio.get("title", [None])[0]

            if title:
                sanitized_title = "".join(c for c in title if c.isalnum() or c in " -_").rstrip()
                new_path = os.path.join(media_dir, f"{sanitized_title}.{file_extension}")

                if full_path == new_path:
                    print(f"File '{filename}' already has the correct name.")
                    continue

                os.rename(full_path, new_path)
                print(f"Renamed '{filename}' to '{sanitized_title}.{file_extension}'")

            else:
                print(f"No title tag found for '{filename}', skipping.")

        except Exception as e:
            print(f"Could not process '{filename}': {e}")