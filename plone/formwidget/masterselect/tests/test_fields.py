"""Tests of package fields."""
from plone.formwidget.masterselect import MasterSelectBoolField
from plone.formwidget.masterselect import MasterSelectField
from plone.formwidget.masterselect import MasterSelectRadioField
from plone.formwidget.masterselect.interfaces import IMasterSelectField
from zope.schema.interfaces import IBool
from zope.schema.interfaces import IChoice
from zope.schema.interfaces import IField
from zope.schema.interfaces import IObject

import unittest


class TestFields(unittest.TestCase):
    """Test that plone.formwidget.masterselect fields is working."""

    def test_ifield_providedby_masterselectfield(self):
        self.assertTrue(
            IField.providedBy(
                MasterSelectField(slave_fields=(), values=()),
            )
        )

    def test_ichoice_providedby_masterselectfield(self):
        self.assertTrue(
            IChoice.providedBy(
                MasterSelectField(slave_fields=(), values=()),
            )
        )

    def test_imasterselectfield_providedby_masterselectfield(self):
        self.assertTrue(
            IMasterSelectField.providedBy(
                MasterSelectField(slave_fields=(), values=()),
            )
        )

    def test_iobject_not_providedby_masterselectfield(self):
        self.assertFalse(
            IObject.providedBy(
                MasterSelectField(slave_fields=(), values=()),
            )
        )

    def test_ifield_providedby_masterselectboolfield(self):
        self.assertTrue(
            IField.providedBy(
                MasterSelectBoolField(),
            )
        )

    def test_ibool_providedby_masterselectboolfield(self):
        self.assertTrue(
            IBool.providedBy(
                MasterSelectBoolField(),
            )
        )

    def test_imasterselectfield_providedby_masterselectboolfield(self):
        self.assertTrue(
            IMasterSelectField.providedBy(
                MasterSelectBoolField(),
            )
        )

    def test_ifield_providedby_masterselectradiofield(self):
        self.assertTrue(
            IField.providedBy(
                MasterSelectRadioField(slave_fields=(), values=()),
            )
        )

    def test_ichoice_providedby_masterselectradiofield(self):
        self.assertTrue(
            IChoice.providedBy(
                MasterSelectRadioField(slave_fields=(), values=()),
            )
        )

    def test_imasterselectfield_providedby_masterselectradiofield(self):
        self.assertTrue(
            IMasterSelectField.providedBy(
                MasterSelectRadioField(slave_fields=(), values=()),
            )
        )

    def test_ibool_not_providedby_masterselectradiofield(self):
        self.assertFalse(
            IBool.providedBy(
                MasterSelectRadioField(slave_fields=(), values=()),
            )
        )
