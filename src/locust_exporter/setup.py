# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='locust_exporter',
    version='1.1.0',
    description="Website load testing framework",
    long_description="""Locust is a python utility for doing easy, distributed load testing of a web site""",
    classifiers=[
        "License :: OSI Approved :: Apache 2",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
    ],
    keywords='',
    author='Arthur Halet',
    author_email='',
    license='Apache 2.0',
    packages=['locust_exporter'],
    include_package_data=True,
    zip_safe=False,
    install_requires=["prometheus_client>=0.7.1", "requests>=2.9.1"],
    entry_points={
        'console_scripts': [
            'locust_exporter = locust_exporter.locust_exporter:main',
        ]
    },
)
