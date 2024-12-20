from .rename import rename_media_files
import argparse
import sys
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rename media files based on their metadata.")
    parser.add_argument(
        "media_dir",
        type=str,
        help="Path to the directory containing media files."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate renaming without making changes."
    )
    parser.add_argument(
        "--extensions",
        nargs="+",
        help="Filter files by extensions (e.g., mp3 flac). Defaults to all supported formats."
    )

    args = parser.parse_args()

    media_dir = args.media_dir
    if not os.path.isdir(media_dir):
        print(f"The specified directory does not exist: {media_dir}")
        sys.exit(1)

    rename_media_files(media_dir, dry_run=args.dry_run)
