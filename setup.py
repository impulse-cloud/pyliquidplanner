#/usr/bin/env python
import io
import re
from setuptools import setup


with io.open('./liquidplanner/__init__.py', encoding='utf8') as version_file:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")

try:
    with io.open('README.md', encoding='utf8') as readme:
        long_description = readme.read()
except IOError:
    long_description = None


setup(
    name='pyliquidplanner',
    version=version,
    description='Python library for accessing the REST API of the Liquid Planner project management tool',
    long_description=long_description,
    author="Gavin Hodge",
    author_email="gavin.hodge@gmail.com",
    url="https://github.com/gavinhodge/pyliquidplanner",
    download_url="https://github.com/gavinhodge/pyliquidplanner/tarball/{0}".format(version),
    packages=['liquidplanner', ],
    keywords=['liquidplanner', 'liquid', 'planner', 'project', 'management'],
    classifiers=[],
    install_requires=[
        'requests>=2.7.0',
        'python-dateutil>=2.4.2',
    ],
    tests_require=[
        'mock',
    ],
    license='MIT',
    test_suite='tests',
)
