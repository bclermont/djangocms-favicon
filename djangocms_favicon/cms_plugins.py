from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from .models import FaviconPluginModel


@plugin_pool.register_plugin
class FaviconPlugin(CMSPluginBase):
    model = FaviconPluginModel
    render_template = "favicon.html"
    cache = False
