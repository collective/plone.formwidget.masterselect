import copy

from Acquisition import aq_inner, aq_parent

from zope.component import adapter
from zope.interface import implements, implementer
from zope.schema.interfaces import IContextSourceBinder, IBool
from zope.schema.interfaces import IVocabularyTokenized
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.browser.interfaces import IBrowserView
from zope.i18n import translate

from z3c.form import interfaces
from z3c.form.widget import FieldWidget
from z3c.form.browser import select, checkbox, radio

from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView

from plone.formwidget.masterselect.interfaces import IMasterSelectField
from plone.formwidget.masterselect.interfaces import IMasterSelectBoolField
from plone.formwidget.masterselect.interfaces import IMasterSelectRadioField
from plone.formwidget.masterselect.interfaces import IMasterSelectWidget
from plone.formwidget.masterselect.interfaces import IMasterSelectBoolWidget
from plone.formwidget.masterselect.interfaces import IMasterSelectRadioWidget

try:
    # python 2.6
    import json
except:
    # plone 3.3
    import simplejson as json


BINDERS = dict(
    vocabulary= "jQuery('%(masterID)s').bindMasterSlaveVocabulary(%(json)s);",
    value     = "jQuery('%(masterID)s').bindMasterSlaveValue(%(json)s);",
    attr      = "jQuery('%(masterID)s').bindMasterSlaveAttr(%(json)s);",
    toggle    = "jQuery('%(masterID)s').bindMasterSlaveToggle(%(json)s);"
)

JQUERY_ONLOAD = """\
jQuery(document).ready(function()
{
%s

    jQuery(document).bind('loadInsideOverlay', function(e, pbajax, responseText, errorText, api){
        var interval_timeline = setInterval(function(){
            var el = jQuery(pbajax);
            var pbo = el.closest('.overlay-ajax').data('pbo');
            if (jQuery('#' + pbo.nt + ' .pb-ajax').length > 0){
                clearInterval(interval_timeline);
                el.find('.field').each(function() {
                    $(this).find('.masterselect-widget:first').change();
                })
            }
        },200);
    });
});
"""


def boolean_value(value):
    return value in (1, '1', 'true', 'True', True)


class MasterSelect(object):
    """Methods required for widgets
    """

    def getSlaves(self):
        slaves = (getattr(self.field, 'slave_fields', None)
                or getattr(self.field.value_type, 'slave_fields', ()))
        for slave in slaves:
            yield slave.copy()

    def renderJS(self):
        url = '/'.join(self.request.physicalPathFromURL(self.request.getURL()))
        widgetURL = url + '/++widget++%s/@@masterselect-jsonvalue' % self.__name__

        for slave in self.getSlaves():
            if not 'slaveID' in slave:
                # Try to get it from widget
                widget = self.form.widgets.get(slave['name'])
                if widget is not None and getattr(widget, 'id', None) is not None:
                    slave['slaveID'] = '#' + widget.id
                else:
                    # Try our best to create one; won't work for checkboxes, so
                    # better to provide a slaveID in the schema in that case or
                    # sometimes to increase the scope beyond the field
                    prefix = '-'.join(self.id.split('-')[:-1])
                    slave['slaveID'] = '#%s-%s' % (prefix, slave['name'])

            slave['url'] = widgetURL
            slave['masterID'] = slave.get(
                'masterSelector',
                '#' + slave.get('masterID', self.id)
                )
            slave['siblings'] = slave.get('siblings', False)
            slave['empty_length'] = int(slave.get('empty_length', 0))
            slave.setdefault('control_param', 'master_value')

            if 'hide_values' in slave:
                values = slave['hide_values']
                if not isinstance(values, (tuple, list)):
                    values = [values]
                if IBool.providedBy(self.field):
                    values = [boolean_value(v) for v in values]
                #else:
                #    values = [str(v) for v in values]
                slave['values'] = values

            js_template = BINDERS.get(slave.get('action')) or BINDERS['toggle']

            # Remove some things from slave we don't need
            slave.pop('vocab_method', None)
            slave.pop('hide_values', None)
            slave.pop('control_param', None)

            settings = {'masterID': slave['masterID'],
                        'json': json.dumps(slave)
                       }
            yield js_template % settings

    def getInlineJS(self):
        """render javascript"""
        return JQUERY_ONLOAD % '\n'.join(self.renderJS())


class MasterSelectWidget(select.SelectWidget, MasterSelect):
    """Master Select Widget
    """
    implements(IMasterSelectWidget)

    klass = u'masterselect-widget'


class MasterSelectBoolWidget(checkbox.SingleCheckBoxWidget, MasterSelect):
    """MasterSelectBoolWidget
    """
    implements(IMasterSelectBoolWidget)

    klass = u'masterselect-widget'


class MasterSelectRadioWidget(radio.RadioWidget, MasterSelect):
    """MasterSelectRadioWidget
    """
    implements(IMasterSelectRadioWidget)

    klass = u'masterselect-widget'


@implementer(interfaces.IFieldWidget)
@adapter(IMasterSelectField, interfaces.IFormLayer)
def MasterSelectFieldWidget(field, request):
    return FieldWidget(field, MasterSelectWidget(request))


@implementer(interfaces.IFieldWidget)
@adapter(IMasterSelectBoolField, interfaces.IFormLayer)
def MasterSelectBoolFieldWidget(field, request):
    return FieldWidget(field, MasterSelectBoolWidget(request))


@implementer(interfaces.IFieldWidget)
@adapter(IMasterSelectRadioField, interfaces.IFormLayer)
def MasterSelectRadioFieldWidget(field, request):
    return FieldWidget(field, MasterSelectRadioWidget(request))


class MasterSelectJSONValue(BrowserView):
    """JSON vocabulary or value for the given slave field"""

    def __init__(self, context, request):
        self.context = aq_inner(context)
        self.request = request

        # in some cases the context is the view, so lets walk up
        # and search the real context
        context = self.context
        while IBrowserView.providedBy(context):
            context = aq_parent(aq_inner(context))
        self.widget = context

        # TODO: Test with deco to see if we need to do this
        # Disable transform on request since it is a json response and we
        # want to make sure it is not wrapped in xml
        #from plone.transformchain.interfaces import DISABLE_TRANSFORM_REQUEST_KEY
        #request.environ[DISABLE_TRANSFORM_REQUEST_KEY] = True

    def createVocaabulary(self, value):
        """Create a simple vocubulary from provided value, list or tuple
        """
        terms = []
        for token in value:
            title = token
            if isinstance(token, (tuple, list)) and len(token) == 2:
                title = token[1]
                token = token[0]
            terms.append(SimpleTerm(value=token, title=title))
        return SimpleVocabulary(terms)

    def getVocabulary(self, slave, value, default=None):
        kw = {slave['control_param']: value}
        vocabulary = slave.get('vocab_method', None)
        if vocabulary is None:
            return default
        return vocabulary(**kw)

    def __call__(self):
        self.request.response.setHeader(
            'Content-Type', 'application/json; charset=utf-8')

        field = self.request['field']
        slavename = self.request['name']
        slaveid = self.request['slaveID']
        masterid = self.request['masterID']
        value = self.request['value']

        for slave in self.widget.getSlaves():
            # Loop until we find the slave we want
            if slave['name'] != slavename:
                continue

            action = slave.get('action')
            if action not in ['vocabulary', 'value', 'attr']:
                continue

            # --- VALUE --------------------------------------------------------
            if action == 'value':
                value = self.getVocabulary(slave, value, '')
                return json.dumps(translate(value, self.request))

            # --- ATTR- --------------------------------------------------------
            if action == 'attr':
                result = self.getVocabulary(slave, value, None)
                if isinstance(result, dict) and 'attr' in result and 'value' in result:
                    return json.dumps(result)
                else:
                    raise ValueError('Bad attr dictionary for %s.' % slavename)

            # --- VOCABULARY ---------------------------------------------------
            vocabulary = self.getVocabulary(slave, value)

            if isinstance(vocabulary, (tuple, list)):
                vocabulary = self.createVocaabulary(vocabulary)

            widget = self.widget.form.widgets.get(slave['name'])
            if widget is None:
                raise ValueError('Can not find widget: %s' % slave['name'])

            if (IContextSourceBinder.providedBy(vocabulary)
                or IVocabularyTokenized.providedBy(vocabulary)):

                widget.field = copy.copy(widget.field)
                if hasattr(widget.field, 'value_type'):
                    widget.field.value_type.vocabulary = vocabulary
                else:
                    widget.field.vocabulary = vocabulary
                widget.terms = None
                widget.updateTerms()
                widget.update()
                # widget may define items as a property or as a method
                items = widget.items if not callable(widget.items) else widget.items()
                # translate if possible. content can be a Message, a string, a unicode
                for item in items:
                    item['content'] = translate(safe_unicode(item['content']), context=self.request)
                responseJSON = {'items': items}

                # disable select box if term length = 'disable_length'
                #if len(widget.terms) == slave.get('disable_length', None):
                #    responseJSON['disabled'] = True

                return json.dumps(responseJSON)

        raise ValueError('No such master-slave combo')
