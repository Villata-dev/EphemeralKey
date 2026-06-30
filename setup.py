from setuptools import setup, find_packages

setup(
    name='ephemeralkey',
    version='3.1.0',
    description='Suite de Privacidad, Generacion de Credenciales y Buzones Efimeros',
    author='Francisco Villa',
    packages=find_packages(),
    install_requires=[
        'requests>=2.31.0',
        'Flask>=2.3.2',
        'Flask-Limiter>=3.3.1',
        'customtkinter>=5.2.0'
    ],
    entry_points={
        'console_scripts': [
            'ephemeralkey=cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Security',
        'Programming Language :: Python :: 3.11',
    ],
)
