# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.testing import z2
from zope.configuration import xmlconfig


class MasterSelectLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.formwidget.masterselect
        xmlconfig.file(
            'testing.zcml',
            plone.formwidget.masterselect,
            context=configurationContext
        )

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plone.formwidget.masterselect:demo')

PLONE_FORMWIDGET_MASTERSELECT = MasterSelectLayer()
PLONE_FORMWIDGET_MASTERSELECT_INTEGRATION = IntegrationTesting(
    name='plone.formwidget.masterselect:Integration',
    bases=(PLONE_FORMWIDGET_MASTERSELECT, ))
PLONE_FORMWIDGET_MASTERSELECT_FUNCTIONAL = FunctionalTesting(
    name='plone.formwidget.masterselect:Functional',
    bases=(PLONE_FORMWIDGET_MASTERSELECT, ))
PLONE_FORMWIDGET_MASTERSELECT_ROBOT = FunctionalTesting(
    name='plone.formwidget.masterselect:Robot',
    bases=(REMOTE_LIBRARY_BUNDLE_FIXTURE,
           PLONE_FORMWIDGET_MASTERSELECT,
           z2.ZSERVER_FIXTURE))
