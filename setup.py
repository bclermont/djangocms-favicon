import os

from setuptools import setup, find_packages

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

REQUIREMENTS = [
    'django-cms>=3.4.5',
    'django-colorfield>=0.1.15',
    'django-filer>=1.2.4',
]

setup(
    name="djangocms-favicon",
    version="0.0.1",
    packages=find_packages(exclude=["settings.py"]),
    scripts=['say_hello.py'],
    install_requires=REQUIREMENTS,
    include_package_data=True,

    # metadata to display on PyPI
    author="Wei Jian Gan",
    author_email="weijian.gan@blabs.asia",
    description="A django CMS favicon plugin",
    license="Bruno",
    keywords="favicon icon",
    url=
    "https://git.tools.robotinfra.com/blabs/djangocms-favicon",  # project home page, if any
    project_urls={
        "Bug Tracker":
            "https://git.tools.robotinfra.com/blabs/djangocms-favicon/issues",
        # "Documentation": "https://docs.example.com/HelloWorld/",
        "Source Code":
            "https://git.tools.robotinfra.com/blabs/djangocms-favicon",
    },
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Bruno License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
    ],
    # could also include long_description, download_url, classifiers, etc.
)