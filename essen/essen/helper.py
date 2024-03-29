import re
from urllib.parse import urlparse


class reify:
    """Use as a class method decorator.  It operates almost exactly like the
    Python ``@property`` decorator, but it puts the result of the method it
    decorates into the instance dict after the first call, effectively
    replacing the function it decorates with an instance variable.  It is, in
    Python parlance, a non-data descriptor.  The following is an example and
    its usage:

    .. doctest::

        >>> from pyramid.decorator import reify

        >>> class Foo:
        ...     @reify
        ...     def jammy(self):
        ...         print('jammy called')
        ...         return 1

        >>> f = Foo()
        >>> v = f.jammy
        jammy called
        >>> print(v)
        1
        >>> f.jammy
        1
        >>> # jammy func not called the second time; it replaced itself with 1
        >>> # Note: reassignment is possible
        >>> f.jammy = 2
        >>> f.jammy
        2
    """

    def __init__(self, wrapped):
        self.wrapped = wrapped
        self.__doc__ = wrapped.__doc__

    def __get__(self, inst, objtype=None):
        if inst is None:
            return self
        val = self.wrapped(inst)
        # reify is a non-data-descriptor which is leveraging the fact
        # that it is not invoked if the equivalent attribute is defined in the
        # object's dict, so the setattr here effectively hides this descriptor
        # from subsequent lookups
        setattr(inst, self.wrapped.__name__, val)
        return val


URL_REGEX = re.compile(
    r"(((https?:\/\/(www\.)?)|www\.)[-a-zA-Z0-9@:%._\+~#=]{3,256}(?<!\.)\.[a-zA-Z]{2,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*))"
    r"|([-a-zA-Z0-9@:%._\+~#=]{3,256}(?<!\.)\.(com|net|org|uk|de|ca|us|ch|recipes)\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*))",
    flags=re.UNICODE | re.IGNORECASE,
)


def replace_url_with_link(text, link_template='<a href="{}">{}</a>'):
    def replace(match):
        match = match.group(0)
        url = urlparse(match, scheme="http").geturl()
        return link_template.format(url, match)

    return re.sub(URL_REGEX, replace, text)
