import os
import sys
import argparse

import ffmpeg

from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.aiff import AIFF
from mutagen.ogg import OggFileType
from mutagen.asf import ASF
from mutagen.wave import WAVE


MUTAGEN_MAP = {
    "mp3": lambda path: MP3(path, ID3=EasyID3),
    "mp4": MP4,
    "m4a": MP4,
    "alac": MP4,
    "flac": FLAC,
    "aiff": AIFF,
    "ogg": OggFileType,
    "opus": OggFileType,
    "wma": ASF,
    "wav": WAVE,
}

MUTAGEN_FORMATS = ['mp3', 'mp4', 'm4a', 'alac', 'flac', 'aiff', 'ogg', 'opus', 'wma', 'wav']
FFMPEG_FORMATS = ['mkv', 'mka']


def sanitize_title(title, allowed_chars=None):
    if allowed_chars is None:
        allowed_chars = " -_."
    return "".join(c for c in title if c.isalnum() or c in allowed_chars).rstrip()


def get_title_ffmpeg(file_path):
    meta = ffmpeg.probe(full_path)
    return meta.get("format", {}).get("tags", {}).get("title")


def rename_media(
    media_dir, 
    format_filter=None, 
    dry_run=False
):
    if format_filter is None:
        format_filter = [*MUTAGEN_FORMATS, *FFMPEG_FORMATS]

    renamed_files = {}
    
    for filename in os.listdir(media_dir):
        full_path = os.path.join(media_dir, filename)
        
        _, ext = os.path.splitext(filename)
        file_ext = ext.lstrip('.').lower()

        if file_ext not in format_filter:
            print(f"Format not supported: '.{file_ext}' ({filename})")
            continue

        try:
            if file_ext in FFMPEG_FORMATS:
                title = get_title_ffmpeg(full_path)
            else:
                file_map = MUTAGEN_MAP.get(file_ext)
                if not file_map:
                    print(f"Skipping: '{filename}'")
                    continue
                media = file_map(full_path)
                title = media.tags.get("title", [None])[0] if media.tags else None

            if title:
                sanitized_title = sanitize_title(title)
                new_path = os.path.join(media_dir, f"{sanitized_title}.{file_ext}")

                base_title = sanitized_title
                counter = renamed_files.get(new_path, 1)
                while new_path in renamed_files:
                    counter += 1
                    sanitized_title = f"{base_title}_{counter}"
                    new_path = os.path.join(media_dir, f"{sanitized_title}.{file_ext}")

                renamed_files[new_path] = counter

                if full_path == new_path:
                    print(f"File '{filename}' already has the correct name.")
                    continue

                if dry_run:
                    print(f"[DRY-RUN] Would rename '{filename}' to '{sanitized_title}.{file_ext}'")
                else:
                    os.rename(full_path, new_path)
                    print(f"Renamed '{filename}' to '{sanitized_title}.{file_ext}'")
            else:
                print(f"No title tag found for '{filename}', skipping.")

        except Exception as e:
            print(f"Could not process '{filename}': {e}")
