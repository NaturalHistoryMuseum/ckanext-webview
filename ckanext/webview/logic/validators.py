#!/usr/bin/env python
# encoding: utf-8
#
# This file is part of ckanext-webview
# Created by the Natural History Museum in London, UK

import re

from ckan.plugins import toolkit


def is_valid_url(value, context):
    """
    Validate URL pattern.

    :param value:
    :param context:
    :returns:
    """
    # from https://urlregex.com
    pattern = (
        'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    if re.search(pattern, value, re.IGNORECASE):
        return value

    raise toolkit.Invalid(toolkit._('Not a valid URL'))


def not_datastore(key, data, errors, context):
    data_dict = {k[0]: v for k, v in data.items()}
    value = data.get(key)
    if value is None or value == '':
        resource = toolkit.get_action('resource_show')(
            context, {'id': data_dict.get('resource_id')}
        )
        value = resource.get('url')
    if value.endswith('_datastore_only_resource'):
        raise toolkit.Invalid(toolkit._('Cannot use a datastore URL.'))
    return data.get(key)
