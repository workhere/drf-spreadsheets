import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="drf-spreadsheets",
    version="1.0.3",
    author="Joe Paavola",
    author_email="joe@workhere.com",
    description="A Django REST Framework package allowing views to be rendered as CSV or XLSX",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/workhere/drf-spreadsheets",
    packages=setuptools.find_packages(),
    install_requires=["Django>=3.1", "djangorestframework>=3.6", "openpyxl>=2.4", "google-api-python-client>=1.12.1",
                      "google-auth-httplib2>=0.0.4", "google-auth-oauthlib>=0.4.1", ],
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Framework :: Django :: 3.1",
        "Development Status :: 3 - Alpha"
    ],
    python_requires='>=3.6',

)
