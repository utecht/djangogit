import md5
import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def gravatarURL(email):
    m = re.match(r"(.*) <(.*)>", email.strip())
    name = m.group(1)
    emailAddr = m.group(2)
    ret = '<img src=\"http://www.gravatar.com/avatar/{}?s=25\" /> <span>{} &lt;{}&gt;</span>'.format(md5.new(emailAddr.lower()).hexdigest(), email, emailAddr)
    return mark_safe(ret)
