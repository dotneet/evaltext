from setuptools import setup, find_packages

setup(
    name='evaltext',
    version='0.1.0',
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
    install_requires=[
        'numpy',
        'pandas',
        'openai',
        'cohere',
        'python-dotenv',
        'tiktoken'
    ]
)
