from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='i2c_emu',
    version='0.1.0',
    description='Provides an emulator for Adafruit_GPIO/I2C',
    long_description=readme,
    author='Pip Jones',
    author_email='code@scipilot.org',
    url='https://github.com/scipilot/i2c_emu',
    license=license,
    packages=['i2c_emu']
)
