from zope.interface import implements
from zope.schema import Choice, Bool

from plone.formwidget.masterselect.widget import MasterSelectWidget
from plone.formwidget.masterselect.widget import MasterSelectFieldWidget
from plone.formwidget.masterselect.widget import MasterSelectBoolFieldWidget
from plone.formwidget.masterselect.widget import MasterSelectRadioFieldWidget

from plone.formwidget.masterselect.interfaces import IMasterSelectField
from plone.formwidget.masterselect.interfaces import IMasterSelectBoolField
from plone.formwidget.masterselect.interfaces import IMasterSelectRadioField

from zope.i18nmessageid import MessageFactory
_ = MessageFactory("plone.formwidget.masterselect")


class MasterSelectField(Choice):
    """MasterSelectField that provides additional properties for widget
    (extends schema.Choice)
    """

    implements(IMasterSelectField)

    slave_fields = ()

    def __init__(self,
        slave_fields=(),
        **kw
    ):
        self.slave_fields = slave_fields
        super(MasterSelectField, self).__init__(**kw)


class MasterSelectBoolField(Bool):
    """MasterSelectBoolField that provides addtional properties for widget
    (extends schema.Bool)
    """

    implements(IMasterSelectBoolField)

    slave_fields = ()

    def __init__(self,
        slave_fields=(),
        **kw
    ):
        self.slave_fields = slave_fields
        super(MasterSelectBoolField, self).__init__(**kw)


class MasterSelectRadioField(Choice):
    """MasterSelectRadioField that provides additional properties for widget
    (extends schema.Choice)
    """

    implements(IMasterSelectRadioField)

    slave_fields = ()

    def __init__(self,
        slave_fields=(),
        **kw
    ):
        self.slave_fields = slave_fields
        super(MasterSelectRadioField, self).__init__(**kw)