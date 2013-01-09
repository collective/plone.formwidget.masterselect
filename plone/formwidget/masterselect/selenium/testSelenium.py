from plone.formwidget.masterselect.selenium.base import SeleniumTestCase
from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD, TEST_USER_ROLES, SITE_OWNER_NAME, SITE_OWNER_PASSWORD
import time

class OverlayTestCase(SeleniumTestCase):

    def test_login_overlay(self):

        # Add JQuery locator
        self.addJQueryLocator()

        self.open("/", commit=True)
        self.wait()
        self.selenium.click('link=Log in')
        self.waitForElementPresent('id=login_form')

        #self.selenium.type("__ac_name", SITE_OWNER_NAME)
        #self.selenium.type("__ac_password", SITE_OWNER_PASSWORD)
        self.selenium.type("jquery=#__ac_name", SITE_OWNER_NAME)
        self.selenium.type("jq=#__ac_password", SITE_OWNER_PASSWORD)
        self.selenium.click("submit")
        self.wait()
        self.failUnless(self.selenium.is_text_present("Log out"))

        # Install MasterSelect Demo
        self.open("/portal_setup/manage_importSteps")
        self.wait()
        self.selenium.select("context_id", "label=MasterSelect z3cform Widget Demo")
        self.selenium.wait_for_page_to_load("30000")
        self.selenium.click("manage_importAllSteps:method")
        self.selenium.wait_for_page_to_load("30000")

        # Load Master Select Demo page
        self.open("/++add++plone.formwidget.masterselect.demo")
        self.wait()

        #time.sleep(30)

        # Test 1 (master 1)
        self.selenium.select("form-widgets-masterField", "label=2")
        self.waitForAjaxToComplete()
        self.failIf(self.selenium.is_visible("id=formfield-form-widgets-slaveField2"))

        self.selenium.select("form-widgets-masterField", "label=3")
        self.waitForAjaxToComplete()

        self.selenium.select("form-widgets-masterField", "label=4")
        self.waitForAjaxToComplete()
        self.failIf(self.selenium.is_visible("id=formfield-form-widgets-slaveField2"))

        self.selenium.select("form-widgets-masterField", "label=5")
        self.waitForAjaxToComplete()
        time.sleep(1000)
        self.assertEqual('true', self.selenium.get_attribute("jq=#form-widgets-slaveField3-0@disabled"))

        self.selenium.select("form-widgets-masterField", "label=6")
        self.waitForAjaxToComplete()
        self.failIf(self.selenium.is_visible("id=formfield-form-widgets-slaveField1"))

        self.selenium.select("form-widgets-masterField", "label=1")
        self.waitForAjaxToComplete()
        self.assertEqual('true', self.selenium.get_attribute("jq=#form-widgets-slaveField3-0@disabled"))

        ########################################################################

        # Test 2 (master 2)
        self.selenium.select("jq=#form-widgets-masterField2", "label=b")
        self.waitForAjaxToComplete()
        self.selenium.select("jq=#form-widgets-slaveMasterField", "index=0")
        self.assertEqual("c", self.selenium.get_selected_value("jq=#form-widgets-slaveMasterField"))

        self.selenium.select("jq=#form-widgets-masterField2", "label=c")
        self.waitForAjaxToComplete()
        self.selenium.select("jq=#form-widgets-slaveMasterField", "index=0")
        self.assertEqual("d", self.selenium.get_selected_value("jq=#form-widgets-slaveMasterField"))

        self.selenium.select("jq=#form-widgets-masterField2", "label=d")
        self.waitForAjaxToComplete()
        self.selenium.select("jq=#form-widgets-slaveMasterField", "index=0")
        self.assertEqual("e", self.selenium.get_selected_value("jq=#form-widgets-slaveMasterField"))

        self.selenium.select("jq=#form-widgets-masterField2", "label=e")
        self.waitForAjaxToComplete()
        self.selenium.select("jq=#form-widgets-slaveMasterField", "index=0")
        self.assertEqual("f", self.selenium.get_selected_value("jq=#form-widgets-slaveMasterField"))

        self.selenium.select("jq=#form-widgets-masterField2", "label=f")
        self.waitForAjaxToComplete()
        self.selenium.select("jq=#form-widgets-slaveMasterField", "index=0")
        self.assertEqual("g", self.selenium.get_selected_value("jq=#form-widgets-slaveMasterField"))

        #debug = True
        #while debug:
        #    self.wait("3000000")
