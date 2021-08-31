from z3c.form.i18n import MessageFactory as _
from zope.interface import Interface
from zope.schema import Tuple
from zope.schema.interfaces import IBool
from zope.schema.interfaces import IChoice
from zope.schema.interfaces import IField


class IMasterSelectWidget(Interface):
    """Marker interface for the multi select widget.
    """


class IMasterSelectBoolWidget(Interface):
    """Marker interface for the multi select widget.
    """


class IMasterSelectRadioWidget(Interface):
    """Marker interface for the radio button widget.
    """


class IMasterSelectField(IField):
    """
    Additional Fields for MasterSelect
    """
    slave_fields = Tuple(
        title=_(
            "title_slave_fields",
            default="Fields controlled by this field,",
        ),
        description=_(
            "description_slave_fields",
            default="Fields controlled by this field, if control_type "
            "# is vocabulary only the first entry is used",
        ),
        default=(),
        required=False,
    )


class IMasterSelectBoolField(IMasterSelectField, IBool):
    """
    Additional Fields for MasterSelect
    """


class IMasterSelectRadioField(IMasterSelectField, IChoice):
    """
    MasterSelect radio button widget
    """
