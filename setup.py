from setuptools import setup

setup(
   name='myutils',
   version='0.0.4-alpha',
   description='My utils module',
   author='DerPercy',
   author_email='',
   packages=['myutils'],  #same as name
   include_dirs=['storage'],
   install_requires=['openpyxl'], #external packages as dependencies
)
