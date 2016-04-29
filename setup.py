from setuptools import setup

setup(
    name='Crawler-py',
    version='1.3.2',
    url='https://github.com/johann-lecocq/crawler-py/',
    license='GNU GPL 2',
    author='Johann Lecocq',
    author_email='github@johann-lecocq.fr',
    description='A web Crawler',
    long_description=__doc__,
    packages=['crawlerpy','crawlerpy.objet','crawlerpy.parser'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'beautifulsoup4>=4.4.1'
    ],
    classifiers=[
    	'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    entry_points=""
)
