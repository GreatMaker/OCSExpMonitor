from setuptools import setup

config = {
        'description': 'Monitor application for EXP files from OCS GmbH',
        'author': 'Andrea Visinoni - FKV Srl',
        'url': 'URL',
        'download_url': 'WHERE TO DOWNLOAD IT',
        'author_email': 'a.visinoni@fkv.it',
        'version': '0.0.1',
        'install_requires': [],
        'packages': ['monitor'],
        'scripts': [],
        'name': 'OCSExpMonitor'
}

# Add in any extra build steps for cython, etc.

setup(**config)