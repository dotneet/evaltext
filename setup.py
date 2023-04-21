from os import path

from setuptools import setup, find_packages

root_dir = path.abspath(path.dirname(__file__))


def _requirements():
    return [name.rstrip() for name in open(path.join(root_dir, 'requirements.txt')).readlines()]


def _test_requirements():
    return [name.rstrip() for name in open(path.join(root_dir, 'test-requirements.txt')).readlines()]


setup(
    name='evaltext',
    version='0.1.0',
    license='MIT',
    description='prompt evaluation tool.',
    author='Shinji Yamada',
    author_email='dotneet@gmail.com',
    url='https://github.com/dotneet/evaltext',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=_requirements(),
    tests_require=_test_requirements(),
)
