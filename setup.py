from setuptools import setup, find_packages

setup(
    name='dztr_param',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'requests',
    ],
    author='Fuad Yassin',
    author_email='fuad.yassin@usask.ca',
    description='DZTR Parameter Processing Library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/fuadyassin/dztr_param',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
