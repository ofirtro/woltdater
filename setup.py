from setuptools import setup, find_packages

setup(
    name='woltdater',
    version='1.0.0',
    packages=find_packages(),
    description='Telepytgram Wolt updater bot',
    install_requires=['emoji', 'aiogram', 'aiohttp', 'click'],
    python_requires=">=3.6",
    license='GPLv3',
    author='Ofir Troushinsky',
    entry_points={
        'console_scripts': [
            'run_woltdater = woltdater.main:main'
        ]
    }
)
