from setuptools import setup, find_packages

setup(
    name='damdda-generative-ai',
    version='0.1.0',
    description='Generative AI API for Project Description',
    packages=find_packages(include=['damdda_generative_ai', 'damdda_generative_ai.*']),
    install_requires=[
        'Flask==2.0.3',
        'requests==2.25.1'
    ],
    entry_points={
        'console_scripts': [
            'start-server=damdda_generative_ai.scripts.server:main',  # Adjust path based on actual script location
        ],
    },
    python_requires='>=3.6',
)
