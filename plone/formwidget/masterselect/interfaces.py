from zope.interface import Interface
from zope.schema import Tuple
from zope.schema.interfaces import IObject

from z3c.form.i18n import MessageFactory as _


class IMasterSelectWidget(Interface):
    """Marker interface for the multi select widget.
    """


class IMasterSelectBoolWidget(Interface):
    """Marker interface for the multi select widget.
    """


class IMasterSelectRadioWidget(Interface):
    """Marker interface for the radio button widget.
    """


class IMasterSelectField(IObject):
    """
    Additional Fields for MasterSelect
    """
    slave_fields = Tuple(
        title=_(u"title_slave_fields", default=u"Fields controlled by this field,"),
        description=_(u"description_slave_fields", default=u"Fields controlled by this field, if control_type "
                      "# is vocabulary only the first entry is used"),
        default=(),
        required=False
    )

class IMasterSelectBoolField(IMasterSelectField):
    """
    Additional Fields for MasterSelect
    """

class IMasterSelectRadioField(IMasterSelectField):
    """
    MasterSelect radio button widget
    """
