from setuptools import setup

version = "0.0.8"
info = "Download youtube videos and audios by title or link"
author = "Smartwa"
repo = "https://github.com/Simatwa/y2mate-api"

setup(
    name="y2mate-api",
    packages=["y2mate_api"],
    version=version,
    license="MIT",
    author=author,
    maintainer=author,
    author_email="smartwacaleb@gmail.com",
    description=info,
    url=repo,
    project_urls={"Bug Report": f"{repo}/issues/new"},
    install_requires=[
        "argparse>=1.1",
        "requests>=2.0.2",
        "tqdm==4.65.0",
        "colorama==0.4.6",
        "appdirs==1.4.4",
        "getch==1.0",
    ],
    python_requires=">=3.8",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: Free For Home Use",
        "Intended Audience :: Customer Service",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    entry_points={
        "console_scripts": [
            ("y2mate = y2mate_api.console:main"),
        ]
    },
    keywords=["y2mate", "videos", "video-api", "youtube"],
)
