from setuptools import setup
setup(
	name='upgrade-fw',
	version='1.0.0',
	py_modules=[
		'paramiko',
	],
	include_package_data=True,
	install_requires=[
		'ssh',
	],
	entry_points="""
		[console_scripts]
		upgrade_fw = upgrade_fw:main
	""",
)

