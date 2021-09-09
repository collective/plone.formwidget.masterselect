# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone.formwidget.masterselect.setuphandlers import HiddenProfiles
from plone.formwidget.masterselect.testing import PLONE_FORMWIDGET_MASTERSELECT_INTEGRATION  # noqa: E501
from Products.CMFPlone.utils import get_installer
from Products.GenericSetup.upgrade import listUpgradeSteps


import unittest


class TestSetup(unittest.TestCase):
    """Test that plone.formwidget.masterselect is properly installed."""

    layer = PLONE_FORMWIDGET_MASTERSELECT_INTEGRATION

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = get_installer(self.portal, self.layer['request'])
        self.setup = self.portal['portal_setup']

    def test_product_installed(self):
        """Test if plone.formwidget.masterselect is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'plone.formwidget.masterselect'))

    def _get_profiles_upgrades(self):
        """Return the list o profiles of upgrade steps."""
        profiles_upgrades = []
        profile_id = 'plone.formwidget.masterselect:default'
        upgrades = listUpgradeSteps(self.setup, profile_id, '')
        for upgrade in upgrades:
            for step in upgrade:
                import_profile = step['step'].import_profile
                if import_profile:
                    profiles_upgrades.append(import_profile)
        return profiles_upgrades

    def test_upgrade_seteps_hidden(self):
        """Test if profiles of upgrade steps are hidden."""
        hidden_profiles_obj = HiddenProfiles()
        hidden_profiles = hidden_profiles_obj.getNonInstallableProfiles()
        profiles_upgrades = self._get_profiles_upgrades()
        for profile in profiles_upgrades:
            self.assertIn(
                profile,
                hidden_profiles,
                '{0} not in plone.formwidget.masterselect.setuphandlers.'
                'HiddenProfiles.getNonInstallableProfiles'.format(profile),
            )
