from setuptools import setup

setup(
    name='yahoo_ff_bot',

    packages=['yahoo_ff_bot'],

    include_package_data=True,

    version='0.1.0',

    description='Yahoo fantasy football GroupMe Bot',

    author='Rich Barton, Dean Carlson, /u/softsign',

    author_email='rbart65@gmail.com',

    install_requires=['requests>=2.0.0,<3.0.0', 'apscheduler>3.0.0', 'flake8>=3.3.0', 'oauth2','httplib2','oauth2client','simplejson', 'gunicorn', 'flask'],

    test_suite='nose.collector',

    tests_require=['nose', 'requests_mock'],

    url='https://github.com/softsign/yahoo_ff_bot',

    classifiers=[
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
