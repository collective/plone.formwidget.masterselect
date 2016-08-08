# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = '1.5.3.dev0'

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])

setup(
    name='plone.formwidget.masterselect',
    version=version,
    description='A z3c.form widget that controls the vocabulary or '
                'display of other fields on an edit page',
    long_description=long_description,
    # Get more strings from
    # http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='',
    author='Jason Mehring',
    author_email='nrgaway@yahoo.com',
    url='http://svn.plone.org/svn/plone/plone.formwidget.masterselect',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['plone', 'plone.formwidget'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'z3c.form',
        'setuptools',
        'plone.supermodel',
        'plone.z3cform',
        'simplejson',
        # -*- Extra requirements: -*-
    ],
    extras_require={
        'test': [
            'plone.app.testing [robot] >= 4.2.2',
            'plone.app.robotframework',
            'plone.app.dexterity',
        ],
    },
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
