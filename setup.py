from setuptools import setup, find_packages

setup(
    name='Flask-PyMongo-Modelize',
    version='0.0.1',
    packages=find_packages(),
    url='https://github.com/KenetJervet/Flask-PyMongo-Modelize',
    license='BSD',
    author="Savor d'Isavano",
    author_email='anohig_isavay@163.com',
    description='Adds model support for Flask-PyMongo',
    install_requires=[
        'Flask >= 0.10',
        'pymongo >= 2.7',
        'Flask-PyMongo >= 0.3'
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    setup_requires=[
        'nose'
    ],
    tests_require=[
        'nose',
        'coverage'
    ],
    test_suite='tests',
)
