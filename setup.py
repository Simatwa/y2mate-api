from setuptools import setup
from y2mate_api import __version__, __author__, __repo__, __info__

setup(
    name="y2mate-api",
    packages=["y2mate_api"],
    version=__version__,
    license="MIT",
    author=__author__,
    maintainer=__author__,
    author_email="smartwacaleb@gmail.com",
    description=__info__,
    url=__repo__,
    project_urls={"Bug Report": f"{__repo__}/issues/new"},
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
