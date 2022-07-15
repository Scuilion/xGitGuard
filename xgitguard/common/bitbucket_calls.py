"""
Copyright 2021 Comcast Cable Communications Management, LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

SPDX-License-Identifier: Apache-2.0
"""
from email.headerregistry import ContentTypeHeader
import logging
import os
import sys
import time
import requests

from requests.auth import HTTPBasicAuth

#TODO: remove two lines, only for debugging
#from http.client import HTTPConnection
#HTTPConnection.debuglevel = 1

logger = logging.getLogger("xgg_logger")

class BitbucketCalls:

    def __init__(
        self,
        base_url,
        username,
        password,
        commits_api_url,
        throttle_time=2
    ):
        assert base_url is not None, "base_url must be present"
        assert username is not None, "username must be present"
        assert password is not None, "password must be present"
        assert commits_api_url is not None, "commits_api_url must be present"
        self._base_url = base_url
        self._username = username
        self._password = password
        self._commits_api_url = commits_api_url
        self._throttle_time = throttle_time

    def run_bitbucket_search(self, search_query, extension):
        """
        Run the Bitbucket API search with given search query
        Get the items from the response content and Return
        params: search_query - string - Search keyword
        params: extension - string - Search extension
        returns: search_response - list
        """
        logger.debug("<<<< 'Current Executing Function' >>>>")
        time.sleep(self._throttle_time)
        response = self.__bitbucket_api_get_params(
            (search_query + " extension:" + extension)
        )
        if response:
            if response.status_code == 200:
                content = response.json()
                search_response = content["code"]["values"]
                return search_response
            else:
                logger.error(f"Search Response code: {response.status_code}. Continuing...")
        else:
            logger.error(
                f"Search '{search_query}' api call failed as {response}. Continuing..."
            )
        return []

    def get_bitbucket_public_commits(self, url):
        """
        For the given Bitbucket details, call the api and get commit details
        Get and return the response
        returns: response - string
        """
        logger.debug("<<<< 'Current Executing Function' >>>>")

        try:
            time.sleep(self._throttle_time)
            response = requests.get(
                url,
                params= {'blame': 'true'},
                auth=HTTPBasicAuth(self._username, self._password),
                timeout=25,
            )
            return response
        except Exception as e:
            logger.error(f"Bitbucket API commit content get Error:", exc_info=e)
        return {}

    def __bitbucket_api_get_params(self, search_query):
        """
        For the given Bitbucket API url and search query, call the api
        Get and return the response
        ### Need Bitbucket Credential as Env variable named "BITBUCKET_USER" & "BITBUCKET_PASS"

        params: search_query - string
        returns: response - dict
        """
        logger.debug("<<<< 'Current Executing Function' >>>>")

        try:
            response = requests.post(
                self._base_url + '/rest/search/1.0/search',
                json={
                    # 'query': 'auth extension:txt project:~KONEAL',
                    'query': search_query,
                    'entities': {'code':{}},
                    'limits': {'primary':100,'secondary':0}
                },
                headers={'Content-Type': "application/json"},
                auth=HTTPBasicAuth(self._username, self._password),
            )

            return response

        except Exception as e:
            logger.error(f"Bitbucket API call Error: {e}")

        return {}

    def bitbucket_url_content_get(self, file_url):
        """
        For the given bitbucket url, call the api
        Get and return the response

        returns: response - string
        """
        logger.debug("<<<< 'Current Executing Function' >>>>")

        try:
            response = requests.get(
                file_url,
                auth=HTTPBasicAuth(self._username, self._password),
                timeout=10,
            )
            return response
        except Exception as e:
            logger.error(f"Bitbucket API file content get Error: {e}")

        return {}
