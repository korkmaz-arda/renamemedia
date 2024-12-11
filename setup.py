from setuptools import setup, find_packages

setup(
    name="renamemedia",
    version="1.0.0",
    description="Renames media files based on their metadata.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Arda Korkmaz",
    url="https://github.com/korkmaz-arda/renamemedia",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "mutagen>=1.45",
    ],
    entry_points={
        "console_scripts": [
            "renamemedia=renamemedia.rename:rename_media_files",
        ],
    },
    python_requires=">=3.6",
)
