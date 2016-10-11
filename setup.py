# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = '1.6'

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
        'Framework :: Plone :: 4.2',
        'Framework :: Plone :: 4.3',
        'Framework :: Plone :: 5.0',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: JavaScript',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Widget Sets',
    ],
    keywords='plone widget',
    author='Jason Mehring',
    author_email='nrgaway@yahoo.com',
    url='https://github.com/collective/plone.formwidget.masterselect',
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
