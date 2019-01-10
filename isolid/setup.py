import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requires = ["requests","loguru","notifiers","rdflib"]    
       
setuptools.setup(
    name="isolid",
    version="0.3.1",
    author="Indira",
    author_email="indira@qxf2.com",
    description="This module allows to perform some basic Inrupt Solid operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/qxf2/py_isolid",
    packages=setuptools.find_packages(),    
    install_requires=requires,
    python_requires='>=3.6', 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)