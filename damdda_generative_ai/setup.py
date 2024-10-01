from setuptools import setup, find_packages

setup(
    name='damdda_generative_ai',  # The name of your package
    version='1.0',  # Version of your package
    packages=find_packages(),  # Automatically find and include all packages in the project
    include_package_data=True,  # Include additional files specified in MANIFEST.in
    install_requires=[
        'Flask',  # Web framework
        'requests'  # HTTP requests library
    ],
    entry_points={
        'console_scripts': [
            # Define a command-line script `run-server` that runs the `main` function in run.py
            'run-server=damdda_generative_ai.run:main',
        ],
    },
)
