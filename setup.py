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
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
