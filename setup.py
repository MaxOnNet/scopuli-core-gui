from setuptools import setup, find_packages
from os.path import join, dirname
from datetime import datetime

now = datetime.now()

setup(
    name='scopuli_core_gui',
    author='Viktor Tatarnikov',
    author_email='viktor@tatarnikov.org',
    namespace_packages=['Scopuli'],  # line 8
    platforms='any',
    zip_safe=False,
    version='0.1.{0}.{1}.{2}.{3}.{4}'.format(now.year, now.month, now.day, now.hour, now.minute),
    license="Apache",
    url="https://scopuli.tatarnikov.org",
    packages=find_packages(exclude=["tests"]),
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    include_package_data=True
)