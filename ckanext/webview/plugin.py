#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-webview
# Created by the Natural History Museum in London, UK

from ckan.plugins import SingletonPlugin, implements, interfaces, toolkit
from ckanext.webview.logic.validators import is_valid_url, not_datastore

ignore_empty = toolkit.get_validator('ignore_empty')


class WebviewPlugin(SingletonPlugin):
    """
    A CKAN extension that adds a view for displaying generic/arbitrary URLs.
    """

    implements(interfaces.IConfigurer, inherit=True)
    implements(interfaces.IResourceView, inherit=True)

    ## IConfigurer
    def update_config(self, config):
        toolkit.add_template_directory(config, u'theme/templates')
        toolkit.add_resource(u'theme/assets', u'ckanext-webview')

    ## IResourceView
    def info(self):
        return {
            'name': 'web_view',
            'title': 'Web',
            'icon': 'globe',
            'always_available': True,
            'iframed': False,
            'schema': {'web_url': [not_datastore, ignore_empty, str, is_valid_url]},
        }

    def can_view(self, data_dict):
        return True

    def setup_template_variables(self, context, data_dict):
        # defaults to the resource URL but can be overridden
        web_url = data_dict['resource_view'].get('web_url') or data_dict[
            'resource'
        ].get('url')

        return {'web_url': web_url}

    def view_template(self, context, data_dict):
        '''
        :param context:
        :param data_dict:
        '''
        return 'views/web_view.html'

    def form_template(self, context, data_dict):
        '''
        :param context:
        :param data_dict:
        '''
        return 'views/web_view_form.html'
