import os
import sys
import argparse
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.aiff import AIFF
from mutagen.ogg import OggFileType
from mutagen.asf import ASF
from mutagen.mp4 import MP4
from mutagen.wave import WAVE

SUPPORTED_FORMATS = ['mp3', 'mp4', 'flac', 'aiff', 'ogg', 'opus', 'wma', 'wav', 'aac']


def rename_media_files(media_dir, formats=SUPPORTED_FORMATS, dry_run=False):
    if formats is None:
        formats = SUPPORTED_FORMATS

    renamed_files = {}
    
    for filename in os.listdir(media_dir):
        full_path = os.path.join(media_dir, filename)
        file_extension = filename.split('.')[-1].lower()
                
        if file_extension not in formats:
            print(f"Unsupported file format: '{file_extension}' ({filename})")
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

            title = audio.tags.get("title", [None])[0]

            if title:
                sanitized_title = "".join(c for c in title if c.isalnum() or c in " -_").rstrip()
                new_path = os.path.join(media_dir, f"{sanitized_title}.{file_extension}")

                base_title = sanitized_title
                counter = renamed_files.get(new_path, 1)
                while new_path in renamed_files:
                    counter += 1
                    sanitized_title = f"{base_title}_{counter}"
                    new_path = os.path.join(media_dir, f"{sanitized_title}.{file_extension}")

                renamed_files[new_path] = counter

                if full_path == new_path:
                    print(f"File '{filename}' already has the correct name.")
                    continue

                if dry_run:
                    print(f"[DRY-RUN] Would rename '{filename}' to '{sanitized_title}.{file_extension}'")
                else:
                    os.rename(full_path, new_path)
                    print(f"Renamed '{filename}' to '{sanitized_title}.{file_extension}'")
            else:
                print(f"No title tag found for '{filename}', skipping.")

        except Exception as e:
            print(f"Could not process '{filename}': {e}")
