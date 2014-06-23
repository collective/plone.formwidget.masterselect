.. image:: https://travis-ci.org/collective/plone.formwidget.masterselect.svg
    :target: https://travis-ci.org/collective/plone.formwidget.masterselect

.. image:: https://coveralls.io/repos/collective/plone.formwidget.masterselect/badge.png
    :target: https://coveralls.io/r/collective/plone.formwidget.masterselect

MasterSelectWidget
==================

This is a z3cform widget based on the orginal n Archetypes widget which
controls the vocabulary or display of other fields on an edit page. It
needs to be given information about which fields to control and how to control
them.

Feel free to help edit this document to help expain things better!


Example
=======

For more complex examples see ``demo.py`` in pacakge directory.

::
    from zope import schema
    from plone.supermodel import model
    from plone.formwidget.masterselect import _
    from plone.formwidget.masterselect import MasterSelectBoolField
    from plone.formwidget.masterselect import MasterSelectField


    class IMasterSelectDemo(model.Schema):
        """ MasterSelect Demo to demonstrate all options available to
            use and to allow the test modules a content type to work
            with.
        """

        masterField = MasterSelectField(
            title=_(u"MasterField"),
            description=_(u"This field controls the vocabulary of slaveField1,"
                          "the available values in slaveField1 will be equal "
                          "to the numbers between the selected number and 10. "
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
            ),
            required=True,
        )

        slaveField1 = schema.Set(
            title=_(u"SlaveField1"),
            description=_(u"This field's vocabulary is controlled by the value "
                          "selected in masterField. The values available here "
                          "will be the numbers between the number selected in "
                          "masterField and 10. The field will be hidden when 6 "
                          "is selected in the masterField."),
            value_type=schema.Choice(values=(1, 2, 3, 4, 5, 6)),
            required=False,
        )


Parameters
==========

All the magic happens in the slave_fields parameter which should be a
sequence of mappings. Each mapping is a description of a field controlled
by this master field:


name
----

The name of the field to control on when the selection changes. The
controlled field/widget may be of any type unless the 'vocabulary' or
'value' action is used. When the action is 'vocabulary', the field must
use either a MultiSelectionWidget, a SelectionWidget, or a
MasterSelectWidget any of which must have the 'format' parameter set
to 'select' (this is the default only for MasterSelectWidget). For
'value', the widget must be simple enough to change the current value
using element.value or elem.selectedIndex (StringWidget, SelectionWidget,
AutoCompleteWidget, maybe others).


masterID
--------

This is optional and will automatically be calculated if omited.  It can
be used to speicify the exact master field is that is rendered in the html
document.  Normally you will only need to set this for checkbox masters
since their id has a -0 added like this: #form-widgets-checkboxfield-0.
Note that this is a jQuery ID selector.

masterSelector
--------------

This is optional and will default to master ID if not defined.
It has the same usage as masterID but allows to specify any JQuery selector (not
just an ID).

slaveID
-------

This is optional and will automatically be calculated if omited.  It can
be used to speicify the exact slave field name to control in the html form.
Note that this is a jQuery ID selector, so something use something
like this: #form-widgets-field


action
------

The type of action to perform on the slave field.  This can be:

``vocabulary``
    which alters the vocabulary of the slave field using an
    XMLHttpRequest call. To use the ``vocabulary`` action, the slave
    field must meet the widget requirements stated above.

``enable`` or ``disable``
    toggle which marks the target widget as enabled or disabled; To use the
    ``enable / disable`` actions, the field must use a HTML widget that can be
    enabled/disabled.

``show`` or ``hide``
    toggle which marks the target widget as show or hide.

``value``
    which alters the value of another simple widget (StringWidget) on
    selection change using an XMLHttpRequest call.

``attr``
    which alters the value of a DOM element, specified by slaveID

``jquery``
    **NOT YET IMPLEMENTED**
    a complete jquery startment that will be sent back to the DOM to be
    executed.


vocab_method
------------

The name of a method to call to retrieve the dynamic vocabulary for
the slave field, or the value for the slave field when 'value' is used.
For 'vocabulary', this must return a DisplayList. For 'value, it must
return a string or msg_id.  The method must accept a parameter which
will be used to pass the new value selected in the master widget. The
name of this parameter defaults to 'master_value', but any name may be
used as long as it is specified using the control_param element. Used
only with 'action':'vocabulary' or 'action':'value'.

control_param
-------------

As described above, this is the name of the paramter used when
calling the vocab_method. Used only with 'action':'vocabulary',
'action':'value', 'action':'attr' and 'action':'jquery'.

hide_values
-----------

A sequence of values which when selected in the master widget cause
the slave field/widget to be hidden, shown or disabled. The method
used is determined by the 'action' element. Used only with
'action':'hide', 'action':'enable', 'action':'disable' or
'action':'show'. The value '()' (dont use quotes) will trigger on
anything.

siblings
--------

Boolean value to indictate the siblings of the slave field should be
selected as well as the slave field itself.  This field can only be used
with 'action':'hide' or 'action':'show' and is useful for hidng the label
as well the slave field.

empty_length
------------

The position in the slave slave field to start deleting entries from the
selection box when the selection box gets refreshed with new data.  The
selection box options are deleted before the Ajax call so it can not be
used until the call is complete.  This can be useful to prevent a small
select box from appearing is the first option is '-------------'. This
field is optional and can only be used with 'action':'vocabulary'.
This value is also crecked before initating an ajax request.  The ajax
request will not be executed if the master select length is equal to or less
than this number to help prevent slave widgets executing out of order.
Default value is 0.

prevent_ajax_values
-------------------

A sequence of values which when selected in the master widget prevent the
widget from iniating an ajax request. Use ('') as the value to prevent an
ajax call if the select option value is ''.  The default is ().

initial_trigger
---------------

Boolean indicated if the master widget should initally be triggered on
load.  Default is true for everythin except vocabulary in which case it is
false to prevent an itital ajax call which usually will not be needed.

A single MasterSelectWidget may control any number of slave fields, new
fields are controlled by adding new mappings to the slave_fields list/tuple.
A field which is the target of a MasterSelectWidget action may itself use
a MasterSelectWidget to control other fields.

The MasterSelectDemo type includes a number of master and slave widgets in
different configurations. It is disabled by default, but you may import it
through portal_setup tool and test it by checking the "implicitly addable"
checkbox for it in the MasterSelectDemo entry in the portal_types tool.

Enjoy!
