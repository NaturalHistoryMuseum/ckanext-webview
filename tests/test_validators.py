from unittest.mock import MagicMock

import pytest
from ckanext.webview.logic.validators import is_valid_url, not_datastore

from ckan.plugins import toolkit


class TestIsValidURL(object):
    def test_valid_https(self):
        url = 'https://data.nhm.ac.uk'
        assert is_valid_url(url, MagicMock())

    def test_valid_http(self):
        url = 'http://data.nhm.ac.uk'
        assert is_valid_url(url, MagicMock())

    def test_invalid_not_http(self):
        url = 'ftp://something.com'
        with pytest.raises(toolkit.Invalid):
            is_valid_url(url, MagicMock())

    def test_invalid_not_url(self):
        url = 'testing testing'
        with pytest.raises(toolkit.Invalid):
            is_valid_url(url, MagicMock())


class TestNotDatastore(object):
    def test_valid_url(self):
        url = 'https://data.nhm.ac.uk'
        key = ('web_url',)
        data = {key: url, ('resource_id',): 'not-a-real-resource-id'}
        assert not_datastore(key, data, {}, MagicMock())

    def test_valid_similar_datastore(self):
        url = 'http://_datastore_only_resource.com'
        key = ('web_url',)
        data = {key: url, ('resource_id',): 'not-a-real-resource-id'}
        assert not_datastore(key, data, {}, MagicMock())

    def test_invalid_datastore(self):
        url = 'http://_datastore_only_resource'
        key = ('web_url',)
        data = {key: url, ('resource_id',): 'not-a-real-resource-id'}
        with pytest.raises(toolkit.Invalid):
            not_datastore(key, data, {}, MagicMock())
