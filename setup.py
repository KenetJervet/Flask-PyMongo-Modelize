from setuptools import setup, find_packages

setup(
    name='Flask-PyMongo-Modelize',
    version='0.0.1',
    packages=['tests', 'flask_pymongo_modelize'],
    url='https://github.com/KenetJervet/Flask-PyMongo-Modelize',
    license='BSD',
    author="Savor d'Isavano",
    author_email='anohig_isavay@163.com',
    description='Adds model support for Flask-PyMongo',
    packages=find_packages(),
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
    ]
)
