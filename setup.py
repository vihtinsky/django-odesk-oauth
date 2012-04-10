from setuptools import setup, find_packages

version = __import__('django_odesk').get_version()

setup(name='django-odesk',
      version=version,
      description='oDesk API integration for Django using oAuth keys',
      long_description='',
      author='Oleksiy Solyanyk',
      author_email='solex@odesk.com',
      packages = find_packages(),
      install_requires = ['setuptools','python-odesk>=0.4.1'],
      classifiers=['Development Status :: 1 - Alpha',
                   'Environment :: Web Environment',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Topic :: Utilities'],)
