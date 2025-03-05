# renamemedia
A simple tool that renames media files based on their metadata.

Say goodbye to messy, cryptic file names! 'renamemedia' is the perfect tool for organizing media files downloaded from your RSS feed or other sources.


## Installation
Install `renamemedia` directly from GitHub:
```
pip install git+https://github.com/korkmaz-arda/renamemedia.git
```


## Requirements
- `mutagen >= 1.45`
- `ffmpeg-python >= 0.2.0`


## Usage
To rename your media files in `/to/path/`:
```
python -m renamemedia /to/path/
```


To perform a dry run without making actual changes:
```
python -m renamemedia --dry-run /to/path/
```

To limit the operation to specific file extensions:
```
python -m renamemedia --dry-run /to/path/ --extensions mp3
python -m renamemedia --dry-run /to/path/ --extensions mp3 mp4 flac
```
