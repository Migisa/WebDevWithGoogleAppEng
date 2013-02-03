try: 
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
	'description': 'Coursework for WebDevelopment course at Udacity',
	'author': 'Aleksandra Iljina',
	'url': 'TBC',
	'download_url': 'TBC',
	'author_email' : 'alexandra.iljina@gmail.com',
	'version': '0.1',
	'install_requires': ['nose'],
	'packages': ['WebBlog'],
	'scripts':[],
	'name': 'WebDevelopment with Google App Engine'
}

setup(**config)
