from setuptools import setup

setup(
   name='myutils',
   version='0.0.2-alpha',
   description='My utils module',
   author='DerPercy',
   author_email='',
   packages=['myutils'],  #same as name
   install_requires=['openpyxl'], #external packages as dependencies
)
