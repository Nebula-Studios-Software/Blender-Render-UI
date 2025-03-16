from setuptools import setup, find_packages

setup(
    name='blender-render-ui',
    version='0.1.0',
    author='Nebula Studios',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires='>=3.8',
    install_requires=[
        'PyQt5>=5.15.11',
        'PyQt5-Qt5>=5.15.2',
        'PyQt5-sip>=12.11.0',
        'regex'
    ],
    entry_points={
        'console_scripts': [
            'blender-render-ui=src.main:main',
        ],
    },
)