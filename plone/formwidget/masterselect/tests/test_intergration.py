# -*- coding: utf-8 -*-
from Testing import ZopeTestCase as ztc
from plone.formwidget.masterselect.testing import \
    PLONE_FORMWIDGET_MASTERSELECT_INTEGRATION
import unittest


class DecoUITestCase(unittest.TestCase):

    layer = PLONE_FORMWIDGET_MASTERSELECT_INTEGRATION

    def setUp(self):
        ztc.utils.setupCoreSessions(self.app)

    # def test_exporter(self):
    #     client = self.wm

    #     # Create a new page with the title 'Page'
    #     client.open(url=u'/plone')
    #     client.waits.forPageLoad(timeout=u'20000')
        #client.execJS(js=u"$('.deco-plone\\\\.app\\\\.standardtiles\\\\.' + \
        #                     'title-tile h1').html('Page')")
        #client.mouseDown(jquery=u'(".deco-button-save")[0]')
        #client.waits.forPageLoad(timeout=u'20000')

        # Edit the newly created page
        #client.click(jquery=u'("#contentview-edit a")[0]')
        #client.waits.forPageLoad(timeout=u'20000')


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
