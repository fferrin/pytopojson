import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytopojson",
    version="0.0.4",
    author="Facundo Ferrín",
    author_email="facundo.ferrin@gmail.com",
    description="An extension to GeoJSON that encodes topology",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fferrin/pytopojson",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
      'numpy >= 1.15.0',
    ],
    python_requires='>=3.7.3',
)