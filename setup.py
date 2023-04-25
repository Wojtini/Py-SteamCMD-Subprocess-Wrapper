import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="interactive-py-steamcmd-wrapper",
    version="0.1.1",
    author="Wojciech Maziarz",
    author_email="whitem200@gmail.com",
    description="Interactive python wrapper for SteamCMD",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wmaziarz/py_interactivesteamcmdwrapper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    python_requires='>=3.9',
    install_requires=['requests'],
)
