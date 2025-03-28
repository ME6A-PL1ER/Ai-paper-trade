from setuptools import setup, find_packages

setup(
    name='ai-paper-trade',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A neural network-based paper trading simulation project.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'yfinance',
        'numpy',
        'pandas',
        'tensorflow',  # or 'torch' depending on the framework you choose
        'matplotlib',   # for visualization
        'scikit-learn'  # for any additional ML utilities
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)