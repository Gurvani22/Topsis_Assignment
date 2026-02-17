from setuptools import setup, find_packages

setup(
    name="Topsis-Gurvani-102317080",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "openpyxl"
    ],
    entry_points={
        'console_scripts': [
            'topsis=topsis_package.topsis:main'
        ],
    },
    author="Gurvani",
    description="TOPSIS implementation",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
