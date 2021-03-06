import versioneer
commands = versioneer.get_cmdclass().copy()

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name='ngenix-test',
    version=versioneer.get_version(),
    packages=find_packages(),
    url='https://github.com/adalekin/ngenix-test',
    license='MIT',
    author='Aleksey Dalekin',
    author_email='adalekin@gmail.com',
    description='A te.',
    long_description=open('README.md', 'rt').read(),
    package_dir={'ngenix_test': 'ngenix_test'},
    include_package_data=True,
    install_requires=[
    ],
    cmdclass=commands,
    entry_points='''
        [console_scripts]
        nginx-test=nginx_test.run:main
    '''
)
