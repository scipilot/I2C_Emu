from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='IC2_Emu',
    version='0.1.0',
    description='IC2_Emu Provides an emulator for Adafruit_GPIO/I2C',
    long_description=readme,
    author='Pip Jones',
    author_email='code@scipilot.org',
    url='https://github.com/scipilot/IC2_Emu',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
