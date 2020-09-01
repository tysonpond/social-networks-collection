import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = f.readlines()

setuptools.setup(
    name="social-networks-collection",
    version="0.0.1",
    author="Tyson C. Pond",
    author_email="pondtyson@gmail.com",
    description="A collection of social and information networks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tysonpond/social-networks-collection",
    python_requires="~=3.6",
    install_requires=requirements,
    packages=setuptools.find_packages(),
    include_package_data=True,
    keywords=[
        "networks",
        "network science",
        "computational social science",
        "data science",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)