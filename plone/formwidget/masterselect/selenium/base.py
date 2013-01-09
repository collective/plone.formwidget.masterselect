import selenium
import os
import transaction
import unittest2 as unittest

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import quickInstallProduct
from plone.app.testing import PLONE_SITE_ID
from plone.app.testing import FunctionalTesting
from plone.app.testing.layers import PLONE_FIXTURE
from plone.testing.z2 import ZServer
from zope.configuration import xmlconfig

class HostAdjustableZServer(ZServer):
    host = os.environ.get('ZSERVER_HOST', 'localhost')
    port = int(os.environ.get('ZSERVER_PORT', 55001))

HOST_ADJUSTABLE_ZSERVER_FIXTURE = HostAdjustableZServer()

class SeleniumLayer(PloneSandboxLayer):
    defaultBases = (HOST_ADJUSTABLE_ZSERVER_FIXTURE, PLONE_FIXTURE)

    # Connection parameters
    seleniumHost = os.environ.get('SELENIUM_HOST', 'localhost')
    seleniumPort = os.environ.get('SELENIUM_PORT', '4444')
    seleniumBrowser = os.environ.get('SELENIUM_BROWSER', '*firefox')

    def setUpZope(self, app, configurationContext):
        # load ZCML
        import plone.app.dexterity
        xmlconfig.file('meta.zcml', plone.app.dexterity, context=configurationContext)
        xmlconfig.file('configure.zcml', plone.app.dexterity, context=configurationContext)

        #TODO: need mete.zcml for z3c depends so I don't have to import dexterity
        import plone.formwidget.masterselect
        xmlconfig.file('configure.zcml', plone.formwidget.masterselect, context=configurationContext)

    def setUpPloneSite(self, portal):

        # Install Products
        quickInstallProduct(portal, 'plone.app.dexterity')
        quickInstallProduct(portal, 'plone.formwidget.masterselect')
        quickInstallProduct(portal, 'plone.formwidget.masterselect.demo')

        # Start up Selenium
        url = "http://%s:%s/%s" % (self['host'], self['port'], PLONE_SITE_ID)
        self['selenium'] = selenium.selenium(self.seleniumHost, self.seleniumPort, self.seleniumBrowser, url)
        self['selenium'].start()

    def tearDownPloneSite(self, portal):
        self['selenium'].stop()
        del self['selenium']

SELENIUM_FIXTURE = SeleniumLayer()
SELENIUM_TESTING = FunctionalTesting(bases=(SELENIUM_FIXTURE,), name="SeleniumTesting:Functional")


class SeleniumTestCase(unittest.TestCase):
    layer = SELENIUM_TESTING

    def setUp(self):
        self.selenium = self.layer['selenium']

    def open(self, path="/", site_name=PLONE_SITE_ID, commit=False):
        # ensure we have a clean starting point
        if commit:
            transaction.commit()

        index = 0
        if path[0] == '/':
            index = 1

        import urllib
        url = urllib.quote("/%s/%s" % (site_name, path[index:]))

        self.selenium.open(url, ignoreResponseCode=True)

    def wait(self, timeout="30000"):
        self.selenium.wait_for_page_to_load(timeout)

    def waitForElement(self, selector, timeout="30000"):
        """Continue checking for the element matching the provided CSS
        selector."""
        self.selenium.wait_for_condition("""css="%s" """ % selector, timeout)

    def waitForElementPresent(self, selector, timeout="30000"):
        """Wait for a specific element to be present."""
        self.selenium.do_command("waitForElementPresent", [selector, timeout])

##    def watchA4jRequests(self):
##        """Registers with the a4j library to record when an Ajax request
##        * finishes.
##        *
##        * Call this after the most recent page load but before any Ajax requests.
##        *
##        * Once you've called this for a page, you should call waitForA4jRequest at
##        * every opportunity, to make sure the A4jRequestFinished flag is consumed.
##        """
##        self.selenium.do_command("watchA4jRequests", [])
##
##    def waitForA4jRequest(self, timeout="30000"):
##        """/If you've set up with watchA4jRequests, this routine will wait until
##        * an Ajax request has finished and then return.
##        """
##        self.selenium.do_command("waitForA4jRequests", [timeout,])

    def waitForAjaxToComplete(self, timeout="30000"):
        """Waits for all ajax requests to complete
        """
        self.selenium.wait_for_condition(
            #"selenium.browserbot.getCurrentWindow().jQuery.active == 0",
            "selenium.browserbot.getUserWindow().jQuery.active == 0",
            timeout
        )

    def addJQueryLocator(self):
        """Add jQuery selectors for locators
        Use:  "jquery=#txtMemo"
              "jquery=table#myParentTableID > input.input-class"

        IMPORTANT:  Assumes JQuery is already available in browser code otherwise
        it needs to be added to Selenium RC (following links provide details):
        http://dev.niedermair.name/archives/155-howto-integrate-jquery-into-selenium.html
        http://stackoverflow.com/questions/2814007/how-to-i-add-a-jquery-locators-to-selenium-remote-control
        http://www.muranosoft.com/Outsourcingblog/How-To-Use-JQuery-Instead-Of-XPath-Locators-In-Selenium-Testing-Framework.aspx

        -- OR --

        Added jquery to user-extensions

        TODO:  Detect if Jquery available from path (either from user-extensions
               or manually added to jar; otherwise try to load via:
               selenium.browserbot.getUserWindow().jQuery
        """
        jQueryLocatorFunction =  """
        var loc = locator;
        var attr = null;
        var isattr = false;
        var inx = locator.lastIndexOf('@');
        if (inx != -1){
            loc = locator.substring(0, inx);
            attr = locator.substring(inx + 1);
            isattr = true;
        }
        var found = jQuery(inDocument).find(loc);
        //var found = selenium.browserbot.getUserWindow().jQuery(inDocument).find(loc);
        if (found.length >= 1) {
            if (isattr) {
                return found[0].getAttribute(attr);
            } else {
                return found[0];
            }
        } else {
            return null;
        }
        """
        self.selenium.add_location_strategy("jquery", jQueryLocatorFunction)
        self.selenium.add_location_strategy("jq", jQueryLocatorFunction)