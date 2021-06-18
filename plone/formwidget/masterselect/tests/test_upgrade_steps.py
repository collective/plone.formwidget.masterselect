# -*- coding: utf-8 -*-
""" Upgrade steps tests. """

from plone.app.testing import applyProfile
from plone.formwidget.masterselect.testing import (
    PLONE_FORMWIDGET_MASTERSELECT_INTEGRATION,
)
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.interfaces import IBundleRegistry
from zope.component import getUtility

import unittest


class UpgradeTestCaseBase(unittest.TestCase):

    layer = PLONE_FORMWIDGET_MASTERSELECT_INTEGRATION

    def setUp(self, from_version, to_version):
        self.portal = self.layer['portal']
        self.setup = self.portal['portal_setup']
        self.profile_id = 'plone.formwidget.masterselect:default'
        self.from_version = from_version
        self.to_version = to_version

    def _get_upgrade_step(self, title):
        """Get one of the upgrade steps.
        Keyword arguments:
        title -- the title used to register the upgrade step
        """
        self.setup.setLastVersionForProfile(self.profile_id, self.from_version)
        upgrades = self.setup.listUpgrades(self.profile_id)
        steps = [s for s in upgrades[0] if s['title'] == title]
        return steps[0] if steps else None

    def _do_upgrade_step(self, step):
        """Execute an upgrade step.
        Keyword arguments:
        step -- the step we want to run
        """
        request = self.layer['request']
        request.form['profile_id'] = self.profile_id
        request.form['upgrades'] = [step['id']]
        self.setup.manage_doUpgrades(request=request)

    def _how_many_upgrades_to_do(self):
        self.setup.setLastVersionForProfile(self.profile_id, self.from_version)
        upgrades = self.setup.listUpgrades(self.profile_id)
        return len(upgrades[0])


class Upgrade4to5TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, '4', '5')

    def test_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self._how_many_upgrades_to_do(), 1)

    def test_fix_resource_not_found(self):
        title = 'Fix resource not found (GS profile)'
        step = self._get_upgrade_step(title)
        self.assertIsNotNone(step)

        registry = getUtility(IRegistry)
        bundle = registry.forInterface(
            IBundleRegistry,
            prefix='plone.bundles/masterselectScript',
        )

        # Simulate preview state.
        applyProfile(self.portal, 'plone.formwidget.masterselect:testupgrades')

        self.assertIn(
            'plone.formwidget.masterselect/master-compiled.css',
            self.portal(),
        )
        self.assertEqual(['masterselect'], bundle.resources)
        self.assertTrue(bundle.compile)

        self._do_upgrade_step(step)

        self.assertNotIn(
            'plone.formwidget.masterselect/master-compiled.css',
            self.portal(),
        )
        self.assertEqual([], bundle.resources)
        self.assertFalse(bundle.compile)
