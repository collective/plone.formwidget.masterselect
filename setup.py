# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup


version = '2.0.1'

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
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 5.2',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: JavaScript',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Widget Sets',
    ],
    keywords='plone widget',
    author='Jason Mehring',
    author_email='nrgaway@yahoo.com',
    url='https://github.com/collective/plone.formwidget.masterselect',
    license='GPL',
    packages=find_packages("src", exclude=['ez_setup']),
    namespace_packages=['plone', 'plone.formwidget'],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'plone.supermodel',
        'plone.z3cform',
        'Products.CMFPlone',
        'setuptools',
        'z3c.form',
        'zope.component',
        'zope.schema',
    ],
    extras_require={
        'test': [
            'plone.app.dexterity',
            'plone.app.robotframework',
            'plone.app.testing [robot] >= 4.2.2',
            'plone.registry',
            'Products.GenericSetup',
        ],
    },
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
