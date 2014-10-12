# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


readme = open('README.md').read()
# history = open('HISTORY.rm').read()

setup(
    name='GTD-Warrior',
    version='0.1',
    description=('Making Task-Warrior GTD-Ready'),
    long_description=readme,
    author='Romain Endelin',
    author_email='romain.endelin@gmail.com',
    url='https://github.com/RomainEndelin/gtd-warrior',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
    ],
    entry_points = {
        'console_scripts': ['gtd-warrior=gtdwarrior.gtdwarrior:main'],
    },
    license='GPLv3',
    zip_safe=True,  # To be verified
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Office/Business :: Scheduling',
    ],
)
