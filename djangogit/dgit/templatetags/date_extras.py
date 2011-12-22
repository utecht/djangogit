import datetime
import stat

from django import template

register = template.Library()

@register.filter
def date_from_unix(value):
    return datetime.datetime.fromtimestamp(long(value)) #.strftime('%Y-%m-%d %H:%M:%S')

@register.filter
def short_message(value):
    """grab the short version of a commit message"""
    try:
        return value[:value.find('\n')]
    except:
        return "***failed to shorten message :("
    
@register.filter
def pretty_perm(perm):
    def get_perm(permission, masks):
        def letter_gen():
            for l in "rwx":
                yield l
        
        l = letter_gen()
        ret = ""   
        for mask in masks:
            
            if permission & mask:
                ret += l.next()
            else:
                ret += "-"
                
        return ret
    
    if perm & stat.S_IFDIR:
        dir_ = "d"
    else:
        dir_ = "-"
    
    return "{}{}{}{}".format(dir_,
                           get_perm(perm, (stat.S_IRUSR, stat.S_IWUSR, stat.S_IXUSR)),
                           get_perm(perm, (stat.S_IRGRP, stat.S_IWGRP, stat.S_IXGRP)),
                           get_perm(perm, (stat.S_IROTH, stat.S_IWOTH, stat.S_IXOTH)))