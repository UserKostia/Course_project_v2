from setuptools import setup, find_packages


setup(
    name='pythonflet',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'flet'
    ],
    entry_points={
        'console_scripts': [
            'project_name = src.main:main',
        ],
    },
    # Additional metadata
    author='MAVERIC',
    author_email='kostastriletski@gmail.com',
    license='MIT',
)
