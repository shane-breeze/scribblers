from setuptools import setup, find_packages

import versioneer

setup(
    name = 'scribblers',
    version = versioneer.get_version(),
    cmdclass = versioneer.get_cmdclass(),
    description = 'Framework independent producers of event attributes',
    author = 'Tai Sakuma',
    author_email = 'tai.sakuma@gmail.com',
    url = 'https://github.com/TaiSakuma/scribblers',
    packages = find_packages(exclude=['docs', 'images', 'tests']),
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ]
)
