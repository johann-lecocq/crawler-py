from setuptools import setup

setup(
    name='crawler-py',
    version='1.3.8',
    url='http://johann-lecocq.fr/informatique-detail---bibliotheque--crawlerpy.html',
    license='GNU GPL 2',
    author='Johann Lecocq',
    author_email='git-jo@johann-lecocq.fr',
    description='A web Crawler for DTC(dans ton chat), VDM(vie de merde) and SCMB(se coucher moins bete)',
    long_description=open('README').read(),
    packages=['crawlerpy','crawlerpy.objet','crawlerpy.parser'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'beautifulsoup4>=4.4.1'
    ],
    classifiers=[
        'Operating System :: OS Independent',
        "Programming Language :: Python",
        'Programming Language :: Python :: 3',
        'Natural Language :: French',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)'
    ],
    entry_points=""
)
