# encoding: utf-8
import logging
from functools import partial

from sqlalchemy import Column, Boolean

from ckan import __version__ as ckan__version__
from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IConfigurer, ITemplateHelpers, IRoutes
import ckan.plugins.toolkit as toolkit


try:
    import ckanext.user_ext
except ImportError:
    raise RuntimeError("UserOptIn Plugin relies on the UserExt plugin.")

from ckanext.user_ext.interfaces import IUserExt, IUserExtension
from controller import UserOptInController
from model import UserOptInModel
from util import version

ckan_version = version.parse(ckan__version__)

log = logging.getLogger(__name__)


def get_current_user_id():
    c = toolkit.c
    try:
        user_obj = c.userobj
        user_id = user_obj.id
        return user_id
    except (TypeError, AttributeError):
        return None

def is_user_opted_in(controller):
    _id = get_current_user_id()
    return controller.is_opted_in(_id)


def is_user_opted_out(controller):
    _id = get_current_user_id()
    return controller.is_opted_out(_id)


def is_user_opted_in_unknown(controller):
    _id = get_current_user_id()
    return controller.is_opted_in_unknown(_id)


def is_ckan_2_8_0():
    if ckan_version >= version.parse("2.8.0"):
        return True
    return False


def is_bootstrap_2():
    config = toolkit.config
    try:
        base_templates = config["ckan.base_templates_folder"]
    except (KeyError, AttributeError, IndexError):
        base_templates = None
    try:
        base_public = config["ckan.base_public_folder"]
    except (KeyError, AttributeError, IndexError):
        base_public = None
    if (base_public and "bs2" in base_public) or \
            (base_templates and "bs2" in base_templates):
        return True
    if base_templates is None and base_public is None:
        # CKAN 2.8.0 defaults to bootstrap3
        return not bool(is_ckan_2_8_0())
    return False


class UserOptInPlugin(SingletonPlugin):
    implements(IUserExt)
    implements(IUserExtension)
    implements(IConfigurer)
    implements(ITemplateHelpers)
    implements(IRoutes)

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.controller = UserOptInController()


    #UserExtension
    def get_table_columns(self):
        u'''Returns the Columns we want to put in the table'''
        opted_in = Column('opted_in', Boolean)
        return [opted_in]
    def get_model_classes(self):
        u'''Returns the Models to register against the table'''
        return [UserOptInModel]

    #Configurer
    def update_config(self, config):
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        # 'templates' is the path to the templates dir, relative to this
        # plugin.py file.

        # first defined templates are higher priority
        if is_bootstrap_2():
            # override some parts with bootstrap2 templates if needed
            toolkit.add_template_directory(config, 'bs2-templates')
        else:
            toolkit.add_template_directory(config, 'bs3-templates')

        # This is the template code shared between bs2 and bs3.
        toolkit.add_template_directory(config, 'templates')

        # Add this plugin's public dir to CKAN's extra_public_paths, so
        # that CKAN will use this plugin's custom static files.
        toolkit.add_public_directory(config, 'public')

        # Register this plugin's fanstatic directory with CKAN.
        # Here, 'fanstatic' is the path to the fanstatic directory
        # (relative to this plugin.py file), and 'example_theme' is the name
        # that we'll use to refer to this fanstatic directory from CKAN
        # templates.
        toolkit.add_resource('fanstatic', 'user_opt_in')

    # Routes
    def after_map(self, map):
        u'''
        Called after routes map is set up. ``after_map`` can be used to
        add fall-back handlers.

        :param map: Routes map object
        :returns: Modified version of the map object
        '''
        controller = "ckanext.user_opt_in.controller:UserOptInController"
        map.connect('/api/action/user_opt_in/set', controller=controller,
                    action='set')
        return map

    def before_map(self, map):
        u'''
        Called before the routes map is generated. ``before_map`` is before any
        other mappings are created so can override all other mappings.

        :param map: Routes map object
        :returns: Modified version of the map object
        '''
        return map

    # TemplateHelpers
    def get_helpers(self):
        return {
            'is_bootstrap_2': is_bootstrap_2,
            'is_ckan_2_8_0': is_ckan_2_8_0,
            'is_user_opted_in': partial(is_user_opted_in, self.controller),
            'is_user_opted_out': partial(is_user_opted_out, self.controller),
            'is_user_opted_in_unknown': partial(is_user_opted_in_unknown, self.controller)
        }
