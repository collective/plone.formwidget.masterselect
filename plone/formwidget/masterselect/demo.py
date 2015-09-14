# -*- coding: utf-8 -*-
from plone.formwidget.masterselect import MasterSelectBoolField
from plone.formwidget.masterselect import MasterSelectField
from plone.formwidget.masterselect import _
from plone.supermodel import model
from zope import schema


def getSlaveVocab(master):
    """Vocab function that returns a vocabulary consisting of the numbers
    between the input number and 10.

    The displayed value has 'num: ' prepended.
    """
    results = range(int(master) + 1, 10)
    results = [(str(a), 'num: ' + str(a)) for a in results]
    return results


def getSlaveVocab2(master):
    """Vocab function that returns a vocabulary consisting of the five
    letters after the selected letter.

    The displayed value will be capitalized, the stored value lowercase.
    """
    numeric = ord(master)
    results = range(numeric + 1, numeric + 6)
    results = [(chr(a), chr(a).upper()) for a in results]
    return results


def getSlaveVocab3(master):
    return [master]


def getSlaveValue(master):
    """Value function that returns ROT13 transformed input."""
    numeric = ord(master)
    result = chr(numeric + 13)
    return result


class IMasterSelectDemo(model.Schema):
    """MasterSelect Demo to demonstrate all options available to use and to
    allow the test modules a content type to work with.
    """

    masterField = MasterSelectField(
        title=_(u'MasterField'),
        description=_(u'This field controls the vocabulary of slaveField1,'
                      u'the available values in slaveField1 will be equal '
                      u'to the numbers between the selected number and 10. '
                      u'When the value 2 or 4 is selected, slaveField2 will '
                      u'be hidden. When the value 1 or 5 is selected, '
                      u'slaveField3 will be disabled. When value 6 is '
                      u'selected, slaveField one will be hidden.'),
        values=(1, 2, 3, 4, 5, 6),
        slave_fields=(
            # Controls the vocab of slaveField1
            {'name': 'slaveField1',
             'action': 'vocabulary',
             'vocab_method': getSlaveVocab,
             'control_param': 'master',
             },
            # Controls the visibility of slaveField1 also
            {'name': 'slaveField1',
             'action': 'hide',
             'hide_values': ('6',),
             'siblings': True,
             },
            # Controls the visibility of slaveField2
            {'name': 'slaveField2',
             'action': 'hide',
             'hide_values': ('2', '4'),
             'siblings': True,
             },
            # Disables slaveField3
            {'name': 'slaveField3',
             'slaveID': '#form-widgets-slaveField3-0',
             'action': 'disable',
             'hide_values': ('1', '5'),
             'siblings': True,
             },
        ),
        required=True,
    )

    slaveField1 = schema.Set(
        title=_(u'SlaveField1'),
        description=_(u'This field\'s vocabulary is controlled by the value '
                      u'selected in masterField. The values available here '
                      u'will be the numbers between the number selected in '
                      u'masterField and 10. The field will be hidden when 6 '
                      u'is selected in the masterField.'),
        value_type=schema.Choice(values=(1, 2, 3, 4, 5, 6)),
        required=False,
    )

    slaveField2 = schema.Choice(
        title=_(u'SlaveField2'),
        description=_(u'This field\'s visibility is controlled by the value '
                      u'selected in masterField. It will become invisible '
                      u'when the values 2 or 4 are selected.'),
        values=('10', '20', '30', '40', '50'),
        required=False,
    )

    slaveField3 = schema.Bool(
        title=_(u'SlaveField3'),
        description=_(u'This field\'s availability is controlled by the value '
                      u'selected in masterField. It will be deactivated when '
                      u'the values 1 or 5 are selected.'),
        required=False,
    )

    masterField2 = MasterSelectField(
        title=_(u'MasterField2'),
        description=_(u'This field controls the vocabulary of '
                      u'slaveMasterField, the available values in '
                      u'slaveMasterField will be the 5 letters after the '
                      u'selected letter. It also controls the current value '
                      u'of the field SlaveValueField, which contains the '
                      u'ROT13 transformed value of the selection.'),
        values=('a', 'b', 'c', 'd', 'e', 'f'),
        slave_fields=(
            # Controls the vocab of slaveMasterField
            {'name': 'slaveMasterField',
             'action': 'vocabulary',
             'vocab_method': getSlaveVocab2,
             'control_param': 'master',
             },
            # Controls the value of slaveValueField
            {'name': 'slaveValueField',
             'action': 'value',
             'vocab_method': getSlaveValue,
             'control_param': 'master',
             },
        ),
        required=True,
    )

    slaveMasterField = MasterSelectField(
        title=_(u'SlaveMasterField'),
        description=_(u'This field\'s vocabulary is controlled by the value '
                      u'selected in masterField2. The values available here '
                      u'will be the 5 letters after the selected letter. '
                      u'This field also controls the visibility of '
                      u'slaveField4. If the values c or g are selected '
                      u'slaveField4 will be hidden. Only the input field will '
                      u'be hidden while the title and description will remain '
                      u'visible'),
        values=(1, 2, 3, 4, 5, 6),
        slave_fields=(
            # Controls the visibility of slaveField4
            {'name': 'slaveField4',
             'action': 'hide',
             'hide_values': ('c', 'g'),
             'siblings': False,
             },
        ),
        required=True,
    )

    slaveField4 = schema.Choice(
        title=_(u'SlaveField4'),
        description=_(u'This field\'s visibility is controlled by the value '
                      u'selected in slaveMasterField. It will become '
                      u'invisible when the values c or g are selected. Notice '
                      u'only the form field disappears while the label and '
                      u'description remain (siblings set to False'),
        values=('10', '20', '30', '40', '50'),
        required=False,
    )

    slaveValueField = schema.TextLine(
        title=_(u'SlaveValueField'),
        description=_(u'This field\'s value is controlled by the value '
                      u'selected in MasterField2. It will display the ROT13 '
                      u'transformation of the value selected. The field\'s '
                      u'availability is controlled by the value selected in '
                      u'masterField3. It only will be activated when the '
                      u'values "one" is selected.'),
        required=False,
    )

    masterField3 = MasterSelectField(
        title=_(u'MasterField3'),
        description=_(u'This field controls the visibility of slaveField5. '
                      u'It will become visible only when the value "other" '
                      u'is selected. It also controls the availability of'
                      u'slaveValueField. It will be enabled when the value '
                      u'"one" is selected.'),
        values=('one', 'two', 'three', 'other'),
        slave_fields=(
            # Controls the visibility of slaveField5
            {'name': 'slaveField5',
             'action': 'show',
             'hide_values': ('other',),
             'siblings': True,
             },
            # Enable slaveValueField
            {'name': 'slaveValueField',
             'action': 'enable',
             'hide_values': ('one',),
             },
        ),
        required=True,
    )

    slaveField5 = schema.TextLine(
        title=_(u'SlaveField5'),
        description=_(u'This field\'s visibility is controlled by the value '
                      u'selected in masterField3. It will become visible '
                      u'only when the value "other" is selected.'),
        required=False,
    )

    masterBoolean = MasterSelectBoolField(
        title=_(u'MasterBoolean'),
        description=_(u'This field controls the visibility of slaveField6, '
                      u'which will only become visible when this checkbox is '
                      u'checked.'),
        slave_fields=(
            {'masterID': 'form-widgets-masterBoolean-0',
             'name': 'slaveField6',
             'action': 'show',
             'hide_values': 1,
             'siblings': True,
             },
        ),
        required=True,
    )

    slaveField6 = schema.TextLine(
        title=_(u'SlaveField6'),
        description=_(u'This field\'s visibility is controlled by the value '
                      u'selected in masterBoolean. It will become visible '
                      u'only when that checkbox is checked.'),
        required=False,
    )

    masterField4 = MasterSelectField(
        title=_(u'MasterField 4'),
        description=_(u'This field controls the vocabulary of slaveField7.'
                      u'The selected value becomes the value of slaveField7.'),
        values=('ok', 'nok'),
        slave_fields=(
            {'name': 'slaveField7',
             'action': 'vocabulary',
             'vocab_method': getSlaveVocab3,
             'control_param': 'master',
             },
        ),
        required=True,
    )

    slaveField7 = schema.Choice(
        title=_(u'SlaveField7'),
        description=_(u'This field\'s value is controlled by the value '
                      u'selected in masterBoolean.'),
        required=False,
        values=('ok', 'nok')
    )
