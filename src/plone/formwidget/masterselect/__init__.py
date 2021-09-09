from plone.formwidget.masterselect.interfaces import IMasterSelectBoolField
from plone.formwidget.masterselect.interfaces import IMasterSelectField
from plone.formwidget.masterselect.interfaces import IMasterSelectRadioField
from plone.formwidget.masterselect.widget import MasterSelectBoolFieldWidget
from plone.formwidget.masterselect.widget import MasterSelectFieldWidget
from plone.formwidget.masterselect.widget import MasterSelectRadioFieldWidget
from plone.formwidget.masterselect.widget import MasterSelectWidget
from zope.i18nmessageid import MessageFactory
from zope.interface import implementer
from zope.schema import Bool
from zope.schema import Choice
from zope.schema.interfaces import IChoice


_ = MessageFactory("plone.formwidget.masterselect")


@implementer(IMasterSelectField, IChoice)
class MasterSelectField(Choice):
    """MasterSelectField that provides additional properties for widget
    (extends schema.Choice)
    """
    slave_fields = ()

    def __init__(self, slave_fields=(), **kw):
        self.slave_fields = slave_fields
        super(MasterSelectField, self).__init__(**kw)


@implementer(IMasterSelectBoolField)
class MasterSelectBoolField(Bool):
    """MasterSelectBoolField that provides addtional properties for widget
    (extends schema.Bool)
    """
    slave_fields = ()

    def __init__(self, slave_fields=(), **kw):
        self.slave_fields = slave_fields
        super(MasterSelectBoolField, self).__init__(**kw)


@implementer(IMasterSelectRadioField)
class MasterSelectRadioField(Choice):
    """MasterSelectRadioField that provides additional properties for widget
    (extends schema.Choice)
    """
    slave_fields = ()

    def __init__(self, slave_fields=(), **kw):
        self.slave_fields = slave_fields
        super(MasterSelectRadioField, self).__init__(**kw)
