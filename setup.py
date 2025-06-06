from setuptools import setup

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='mic-icon',
    version='1.0',
    packages=['mic_icon'],
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'mic-icon=mic_icon.__main__:main',
        ],
    },
)
