from django.template import (
    Library, Node, VariableDoesNotExist, TemplateSyntaxError
)
from django.utils import six
from django.utils.html import escape
from easy_thumbnails.alias import aliases
from easy_thumbnails.conf import settings
from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.templatetags.thumbnail import (
    RE_SIZE, VALID_OPTIONS, split_args
)

register = Library()

VALID_OPTIONS.append("ext")


class ThumbnailNode(Node):
    """
    Copied from easy_thumbnails.templatetags.thumbnail.
    """

    def __init__(self, source_var, opts, context_name=None):
        self.source_var = source_var
        self.opts = opts
        self.context_name = context_name

    def render(self, context):
        # Note that this isn't a global constant because we need to change the
        # value for tests.
        raise_errors = settings.THUMBNAIL_DEBUG
        # Get the source file.
        try:
            source = self.source_var.resolve(context)
        except VariableDoesNotExist:
            if raise_errors:
                raise VariableDoesNotExist(
                    "Variable '%s' does not exist." % self.source_var
                )
            return self.bail_out(context)
        if not source:
            if raise_errors:
                raise TemplateSyntaxError(
                    "Variable '%s' is an invalid source." % self.source_var
                )
            return self.bail_out(context)
        # Resolve the thumbnail option values.
        try:
            opts = {}
            for key, value in six.iteritems(self.opts):
                if hasattr(value, 'resolve'):
                    value = value.resolve(context)
                opts[str(key)] = value
        except Exception:
            if raise_errors:
                raise
            return self.bail_out(context)
        # Size variable can be either a tuple/list of two integers or a
        # valid string.
        size = opts['size']
        if isinstance(size, six.string_types):
            m = RE_SIZE.match(size)
            if m:
                opts['size'] = (int(m.group(1)), int(m.group(2)))
            else:
                # Size variable may alternatively be referencing an alias.
                alias = aliases.get(size, target=source)
                if alias:
                    del opts['size']
                    opts = dict(alias, **opts)
                else:
                    if raise_errors:
                        raise TemplateSyntaxError(
                            "%r is not a valid size." % size
                        )
                    return self.bail_out(context)
        # Ensure the quality is an integer.
        if 'quality' in opts:
            try:
                opts['quality'] = int(opts['quality'])
            except (TypeError, ValueError):
                if raise_errors:
                    raise TemplateSyntaxError(
                        "%r is an invalid quality." % opts['quality']
                    )
                return self.bail_out(context)
        # Ensure the subsampling level is an integer.
        if 'subsampling' in opts:
            try:
                opts['subsampling'] = int(opts['subsampling'])
            except (TypeError, ValueError):
                if raise_errors:
                    raise TemplateSyntaxError(
                        "%r is an invalid subsampling level." %
                        opts['subsampling']
                    )
                return self.bail_out(context)
        # Check extension
        extension = opts.pop("ext", None)

        try:
            thumbnailer = get_thumbnailer(source)
            thumbnailer.thumbnail_extension = extension or "png"
            thumbnail = thumbnailer.get_thumbnail(opts)
        except Exception:
            if raise_errors:
                raise
            return self.bail_out(context)
        # Return the thumbnail file url, or put the file on the context.
        if self.context_name is None:
            return escape(thumbnail.url)
        else:
            context[self.context_name] = thumbnail
            return ''

    def bail_out(self, context):
        if self.context_name:
            context[self.context_name] = ''
        return ''


@register.tag
def icon(parser, token):
    """
    Copied from easy_thumbnails.templatetags.thumbnail.
    """
    args = token.split_contents()
    tag = args[0]

    # Check to see if we're setting to a context variable.
    if len(args) > 4 and args[-2] == 'as':
        context_name = args[-1]
        args = args[:-2]
    else:
        context_name = None

    if len(args) < 3:
        raise TemplateSyntaxError(
            "Invalid syntax. Expected "
            "'{%% %s source size [option1 option2 ...] %%}' or "
            "'{%% %s source size [option1 option2 ...] as variable %%}'" %
            (tag, tag)
        )

    opts = {}

    # The first argument is the source file.
    source_var = parser.compile_filter(args[1])

    # The second argument is the requested size. If it's the static "10x10"
    # format, wrap it in quotes so that it is compiled correctly.
    size = args[2]
    match = RE_SIZE.match(size)
    if match:
        size = '"%s"' % size
    opts['size'] = parser.compile_filter(size)

    # All further arguments are options.
    args_list = split_args(args[3:]).items()
    for arg, value in args_list:
        if arg in VALID_OPTIONS:
            if value and value is not True:
                value = parser.compile_filter(value)
            opts[arg] = value
        else:
            raise TemplateSyntaxError(
                "'%s' tag received a bad argument: "
                "'%s'" % (tag, arg)
            )
    return ThumbnailNode(source_var, opts=opts, context_name=context_name)
