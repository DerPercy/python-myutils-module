from setuptools import setup

setup(
   name='myutils',
   version='0.0.16',
   description='My utils module',
   author='DerPercy',
   author_email='',
   packages=['myutils','myutils.storage'],  #same as name
   install_requires=['openpyxl','markdown'], #external packages as dependencies
)
