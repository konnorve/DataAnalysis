import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CassiopeaDataAnalysis", # Replace with your own username
    version="0.0.1",
    author="Konnor von Emster + jelly dreamers",
    author_email="kve@berkeley.edu",
    description="data analysis pipeline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/konnorve/DataAnalysis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)