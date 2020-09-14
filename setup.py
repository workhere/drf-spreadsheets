import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="drf-spreadsheets-jpaavola",
    version="1.0.0",
    author="Joe Paavola",
    author_email="joepaavola@gmail.com",
    description="A Django REST Framework package allowing views to be rendered as CSV or XLSX",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jpaav/drf-spreadsheets",
    packages=setuptools.find_packages(),
    install_requires=["Django>=3.1", "djangorestframework>=3.6", "openpyxl>=2.4"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django",
    ],
    python_requires='>=3.6',

)