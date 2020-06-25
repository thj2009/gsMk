import setuptools

with open('README.md', 'r') as fh:
	long_description = fh.read()

setuptools_info = {
	'name': 'gsMk',
	'version': '0.1.0',
	'author': 'Huijie Tian',
	'author_email': 'hut216@lehigh.edu',
	'description': 'Hlobal Sensitivity anslysis of Microkinetic Modeling (gsMk)',
	'long_description': long_description,
	'zip_safe': True,
	'url': '',
	'packages': setuptools.find_packages(),
	'install_requires': [
		'scikit-learn',
		'numpy',
		'scipy'],
	'classifiers': [
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		"Intended Audience :: Science/Research",
		"Topic :: Scientific/Engineering :: Chemistry",
	    ],
}


setuptools.setup(**setuptools_info)
