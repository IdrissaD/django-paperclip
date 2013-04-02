import mimetypes

from django.template import Library, Node, Variable
from django.core.urlresolvers import reverse

from caminae.paperclip.forms import AttachmentForm
from caminae.paperclip.views import add_url_for_obj
from caminae.paperclip.models import Attachment


register = Library()


@register.filter
def icon_name(value):
    mimetype = value.mimetype
    if not mimetype or mimetype == ('application', 'octet-stream'):
        return 'bin'
    ext = mimetypes.guess_extension('/'.join(mimetype))
    return ext[1:] if ext else 'bin'


@register.inclusion_tag('paperclip/add_form.html', takes_context=True)
def attachment_form(context, obj):
    """
    Renders a "upload attachment" form.
    """
    return {
        'attachment_form': AttachmentForm(context['request']),
        'attachment_form_url': add_url_for_obj(obj),
        'next': context['request'].build_absolute_uri(),
    }


@register.inclusion_tag('paperclip/delete_link.html', takes_context=True)
def attachment_delete_link(context, attachment):
    """
    Renders a html link to the delete view of the given attachment. Returns
    no content if the request-user has no permission to delete attachments.
    """
    return {
        'next': context['request'].build_absolute_uri(),
        'delete_url': reverse('delete_attachment', kwargs={'attachment_pk': attachment.pk})
    }


class AttachmentsForObjectNode(Node):
    def __init__(self, obj, var_name):
        self.obj = obj
        self.var_name = var_name

    def resolve(self, var, context):
        """Resolves a variable out of context if it's not in quotes"""
        if var[0] in ('"', "'") and var[-1] == var[0]:
            return var[1:-1]
        else:
            return Variable(var).resolve(context)

    def render(self, context):
        obj = self.resolve(self.obj, context)
        var_name = self.resolve(self.var_name, context)
        context[var_name] = Attachment.objects.attachments_for_object(obj)
        return ''


@register.tag
def get_attachments_for(parser, token):
    """
    Resolves attachments that are attached to a given object. You can specify
    the variable name in the context the attachments are stored using the `as`
    argument. Default context variable name is `attachments`.

    Syntax::

        {% get_attachments_for obj %}
        {% for att in attachments %}
            {{ att }}
        {% endfor %}

        {% get_attachments_for obj as "my_attachments" %}

    """
    def next_bit_for(bits, key, if_none=None):
        try:
            return bits[bits.index(key)+1]
        except ValueError:
            return if_none

    bits = token.contents.split()
    args = {
        'obj': next_bit_for(bits, 'get_attachments_for'),
        'var_name': next_bit_for(bits, 'as', '"attachments"'),
    }
    return AttachmentsForObjectNode(**args)
