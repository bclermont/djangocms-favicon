from cms.models.pluginmodel import CMSPlugin
from colorfield.fields import ColorField
from django.utils.translation import ugettext_lazy as _
from filer.fields.image import FilerImageField


class FaviconPluginModel(CMSPlugin):
    icon = FilerImageField(
        verbose_name=_("favicon"),
        help_text=_("Select an image with"),
    )

    color = ColorField(default='#000', )

    class Meta:
        verbose_name = _("FaviconPluginModel")
        verbose_name_plural = _("FaviconPluginModels")

    def __str__(self):
        return f"<Favicon name={self.icon.name}> color={self.color}"

    def clean(self):
        if self.icon.width < 350 or self.icon.height < 350:
            raise Exception("Image dimensions must be at least 350px")
        if self.icon.width != self.icon.height:
            raise Exception("Image must be have equal width and height")
