*** Settings ***
Resource        plone/app/robotframework/selenium.robot
Resource        plone/app/robotframework/keywords.robot
Library         Remote    ${PLONE_URL}/RobotRemote
Library         String
Variables       plone/app/testing/interfaces.py
Test Setup      Open Test Browser
Test Teardown   Close All browsers


*** Test cases ***
Scenario: Master field controls slave fields visibility and vocabulary
    Given I am on the masterselect demo page as a Manager
     When I select '1' on master field 'form-widgets-masterField'
     Then Slave field '1' should be visible
      And Slave field '1' vocabulary should have values 2,3,4,5,6,7,8,9
      And Slave field '1' should be visible
      And Slave field '3' should be visible
     When I select '2' on master field 'form-widgets-masterField'
     Then Slave field '1' should be visible
      And Slave field '1' vocabulary should have values 3,4,5,6,7,8,9
      And Slave field '2' should not be visible
      And Slave field '3' should be visible
     When I select '3' on master field 'form-widgets-masterField'
     Then Slave field '1' should be visible
      And Slave field '1' vocabulary should have values 4,5,6,7,8,9
      And Slave field '2' should be visible
      And Slave field '3' should be visible
     When I select '4' on master field 'form-widgets-masterField'
     Then Slave field '1' should be visible
      And Slave field '1' vocabulary should have values 5,6,7,8,9
      And Slave field '2' should not be visible
      And Slave field '3' should be visible
     When I select '5' on master field 'form-widgets-masterField'
     Then Slave field '1' should be visible
      And Slave field '1' vocabulary should have values 6,7,8,9
      And Slave field '2' should be visible
      And Slave field '3' should be visible
     When I select '6' on master field 'form-widgets-masterField'
     Then Slave field '1' should not be visible
      And Slave field '2' should be visible
      And Slave field '3' should be visible

Scenario: Master field can controls slavemaster which controls slave fields
    Given I am on the masterselect demo page as a Manager
     When I select 'a' on master field 'form-widgets-masterField2'
     Then Slave master field should be visible
      And Slave master field default selected value should be 'b'
      And Slave field '4' should be visible
      And Slave value field should be enabled
     When I select 'c' on master field 'form-widgets-slaveMasterField'
      And Slave field '4' should be visible
      And Slave field's widget '4' should not be visible

Scenario: Master field disables slave field
    Given I am on the masterselect demo page as a Manager
     When I select 'one' on master field 'form-widgets-masterField3'
     Then Slave value field should be enabled
     When I select 'two' on master field 'form-widgets-masterField3'
     Then Slave value field should be disabled
     When I select 'one' on master field 'form-widgets-masterField3'
     Then Slave value field should be enabled

Scenario: Master boolean field toggles visibility of slave field
    Given I am on the masterselect demo page as a Manager
     When I select the master boolean checkbox field
     Then Slave field '6' should be visible
     When I unselect the master boolean checkbox field
     Then Slave field '6' should not be visible

Scenario: Master select field controls slave field vocabulary. Check if value is well translated.
    Set default language  fr
    Given I am on the masterselect demo page as a Manager
     Then Slave field '7' vocabulary should '' have text values Aucune valeur,ok,nok
     When I select 'nok' on master field 'form-widgets-masterField4'
     Then Slave field '7' vocabulary should '' have text values Aucune valeur,nok
     And Slave field '7' vocabulary should 'not' have text values ok


*** Keywords ***
I am on the masterselect demo page as a ${role}
    Enable Autologin As     ${role}
    Set Autologin Username  ${TEST_USER_NAME}
    Go To    ${PLONE_URL}/++add++plone.formwidget.masterselect.demo

I select '${value}' on master field '${id}'
    Select From List    css=#${id}    ${value}

Slave field '${id}' should be visible
    Element should become visible    css=#formfield-form-widgets-slaveField${id}

Slave field '${id}' should not be visible
    Element should not remain visible    css=#formfield-form-widgets-slaveField${id}

Slave field's widget '${id}' should be visible
    Element should become visible    css=#form-widgets-slaveField${id}

Slave field's widget '${id}' should not be visible
    Element should not remain visible    css=#form-widgets-slaveField${id}

Slave field '${id}' vocabulary should have values ${possible_values}
    @{ITEMS} =    Split String    ${possible_values}    ,
    :FOR    ${i}    in    @{ITEMS}
    \   Page Should Contain Element    xpath=//select[@id='form-widgets-slaveField${id}']/option[@value='${i}']

Slave field '${id}' vocabulary should '${not}' have text values ${possible_values}
    @{ITEMS} =    Split String    ${possible_values}    ,
    :FOR    ${i}    in    @{ITEMS}
    \   Run keyword    Page Should ${not} Contain Element    xpath=//select[@id='form-widgets-slaveField${id}']/option[text()='${i}']

Slave master field should be visible
    Element should become visible    css=#formfield-form-widgets-slaveMasterField

Slave master field should not be visible
    Element should not remain visible    css=#formfield-form-widgets-slaveMasterField

Slave master field default selected value should be '${want}'
    ${have} =    Get Selected List Value    css=#form-widgets-slaveMasterField
    Should be Equal    ${have}    ${want}

Slave value field should be enabled
    Element Should Be Enabled    css=#form-widgets-slaveValueField

Slave value field should be disabled
    Element Should Be Disabled    css=#form-widgets-slaveValueField

I select the master boolean checkbox field
    Select Checkbox    css=#form-widgets-masterBoolean-0

I unselect the master boolean checkbox field
    Unselect Checkbox    css=#form-widgets-masterBoolean-0
