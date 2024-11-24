import os
import sys
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.aiff import AIFF
from mutagen.ogg import OggFileType
from mutagen.asf import ASF
from mutagen.mp4 import MP4
from mutagen.wave import WAVE


def rename_media_files(media_dir, supported_formats=['mp3', 'mp4', 'flac', 'aiff', 'ogg', 'opus', 'wma', 'wav']):
    renamed_files = {}
    
    for filename in os.listdir(media_dir):
        full_path = os.path.join(media_dir, filename)
        file_extension = filename.split('.')[-1].lower()

        if file_extension not in supported_formats:
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
            elif file_extension == "wav":
                audio = WAVE(full_path)
            else:
                print(f"Skipping unsupported file format '{filename}'")
                continue

            title = audio.get("title", [None])[0]

            if title:
                sanitized_title = "".join(c for c in title if c.isalnum() or c in " -_").rstrip()
                new_path = os.path.join(media_dir, f"{sanitized_title}.{file_extension}")

                base_title = sanitized_title
                counter = 1
                while new_path in renamed_files:
                    counter += 1
                    sanitized_title = f"{base_title}_{counter}"
                    new_path = os.path.join(media_dir, f"{sanitized_title}.{file_extension}")

                renamed_files[new_path] = counter

                if full_path == new_path:
                    print(f"File '{filename}' already has the correct name.")
                    continue

                os.rename(full_path, new_path)
                print(f"Renamed '{filename}' to '{sanitized_title}.{file_extension}'")
            else:
                print(f"No title tag found for '{filename}', skipping.")

        except Exception as e:
            print(f"Could not process '{filename}': {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("The script needs a target directory to work on.")
        print("Usage: python rename.py /path/to/media/directory")
        sys.exit(1)

    media_dir = sys.argv[1]

    if not os.path.isdir(media_dir):
        print(f"The specified directory does not exist: {media_dir}")
        sys.exit(1)

    rename_media_files(media_dir)