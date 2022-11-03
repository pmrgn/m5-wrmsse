from setuptools import setup, find_packages
    

with open('README.md', 'r') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name = 'm5-wrmsse',
    version = '1.0.0',
    description = 'WRMSSE score for the M5 dataset',
    long_description = readme,
    author = 'Paul Morgan',
    author_email = '',
    url = 'https://github.com/pmrgn/m5-wrmsse',
    install_requires = [
        'numpy>=1.23',
        'pandas>=1.4',
    ],
    license = license,
    packages = find_packages(where='src'),
    package_dir = {'':'src'},
    package_data = {'m5_wrmsse': ['data/*.csv.gz']},
)
