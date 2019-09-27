import os

from setuptools import setup, find_packages


def _packages():
    pkg_name = 'conduit'
    packages = [f'{pkg_name}.{sub_pkg_name}' for sub_pkg_name in
                find_packages(os.path.join(os.path.dirname(__file__), pkg_name))
                ]
    packages.append(pkg_name)
    return packages


setup(name='tw2019-app-client',
      version='0.1',
      description='realworld sample app REST client',
      url='https://github.com/bbielicki/tw2019-app-client',
      author='Bartosz Bielicki',
      author_email='bartosz.bielicki@gmail.com',
      packages=_packages(),
      package_data={},
      include_package_data=True,
      install_requires=[],
      zip_safe=False,
      license='MIT'
      )
