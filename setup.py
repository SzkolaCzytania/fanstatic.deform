from setuptools import setup, find_packages
import sys, os

version = '0.1a1'

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

setup(name='fanstatic.deform',
      version=version,
      description="A library to tell fanstatic which resources a deform form needs",
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Intended Audience :: Developers",
          "Programming Language :: Python",
          ],
      keywords='deform fanstatic',
      author='Patrick Gerken',
      author_email='do3cc@patrick-gerken.de',
      url='',
      license='BSD-derived (http://www.repoze.org/LICENSE.txt)',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      test_suite="fanstaticdeform.tests.Tests",
      tests_require=['js.extjs'],
      install_requires=[
            'deform',
            'fanstatic',
            'js.jquery',
            'js.jqueryui',
            'js.tinymce'
          # -*- Extra requirements: -*-
      ],
      entry_points={
      'fanstatic.libraries': [
          'deform = fanstaticdeform:deform_library',
          ],
      },
)
