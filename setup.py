from setuptools import setup

setup(
    name='mic-icon',
    version='1.0',
    packages=['mic_icon'],
    install_requires=[
        'pulsectl',
        'pygobject'
    ],
    entry_points={
        'console_scripts': [
            'mic-icon=mic_icon:main',
        ],
    },
)
