
from setuptools import setup

setup(
        name='YML2',
        version='5.5',
        description='YML2',
        author="Volker Birk",
        author_email="vb@pep.foundation",
        packages=["yml2"],
        install_requires=['lxml'],
        package_data = {
            '': ['gpl-2.0.txt'],
            'yml2': ['*.css', '*.yml2', '*.yhtml2', '*.ysl2'],
        },
        entry_points = {
            'console_scripts': [
                'yml2c=yml2.yml2c:main',
                'yml2proc=yml2.yml2proc:main'
            ],
        }
    )

