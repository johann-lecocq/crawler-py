from setuptools import setup

setup(
    name='crawler-py',
    version='2.0.5',
    url='http://johann-lecocq.fr/informatique-detail---bibliotheque--crawlerpy.html',
    license='GNU GPL 2',
    author='Johann Lecocq',
    author_email='git-jo@johann-lecocq.fr',
    description='A web Crawler for DTC(dans ton chat), VDM(vie de merde) and SCMB(se coucher moins bete)',
    long_description=open('README_en.md').read(),
    long_description_content_type='text/markdown',
    packages=['crawlerpy'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'beautifulsoup4==4.7.1',
        'requests==2.21.0'
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
