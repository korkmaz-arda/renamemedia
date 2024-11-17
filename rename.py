import os
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.aiff import AIFF
from mutagen.ogg import OggFileType
from mutagen.asf import ASF
from mutagen.mp4 import MP4


def rename_media_files(media_dir, accepted_formats=['mp3', 'mp4', 'flac', 'aiff', 'ogg', 'opus', 'wma']):
    for filename in os.listdir(media_dir):
        full_path = os.path.join(media_dir, filename)
        file_extension = filename.split('.')[-1].lower()

        if file_extension not in accepted_formats:
            continue

        try:
            if file_extension == "mp3":
                audio = MP3(full_path, ID3=EasyID3)
            elif file_extension == "mp4":
                audio = MP4(full_path)
            elif file_extension == "flac":
                audio = FLAC(full_path)
            elif file_extension == "aiff":
                audio = AIFF(full_path)
            elif file_extension in ["ogg", "opus"]:
                audio = OggFileType(full_path)
            elif file_extension == "wma":
                audio = ASF(full_path)
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
