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

def run_bitbucket_search(api_url, search_query, extension):
    """
    Run the Bitbucket API search with given search query
    Get the items from the response content and Return
    params: api_url - string - Bitbucket Search API url
    params: search_query - string - Search keyword
    params: extension - string - Search extension
    returns: search_response - list
    """
    logger.debug("<<<< 'Current Executing Function' >>>>")

    response = bitbucket_api_get_params(
        api_url + '/rest/search/1.0/search', (search_query + "+extension:" + extension)
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


def bitbucket_api_get_params(api_url, search_query):
    """
    For the given Bitbucket API url and search query, call the api
    Get and return the response
    ### Need Bitbucket Credential as Env variable named "BITBUCKET_USER" & "BITBUCKET_PASS"

    params: api_url - string
    params: search_query - string
    returns: response - dict
    """
    logger.debug("<<<< 'Current Executing Function' >>>>")

    logger.info(f"apiurl '{api_url}', search_query: '{search_query}'")

    try:

        #TODO: parameterize the json
        response = requests.post(
            api_url,
            json={
                'query':'auth extension:txt',
                'entities': {'code':{}},
                'limits': {'primary':100,'secondary':0}
            },
            headers={'Content-Type': "application/json"},
            auth=HTTPBasicAuth(os.getenv("BITBUCKET_USER"), os.getenv("BITBUCKET_PASS")),
        )

        return response

    except Exception as e:
        logger.error(f"Github API call Error: {e}")

    return {}

def bitbucket_url_content_get(api_url):
    """
    For the given bitbucket url, call the api
    Get and return the response

    params: api_url - string
    returns: response - string
    """
    logger.info(f"here")
    logger.debug("<<<< 'Current Executing Function' >>>>")

    token_var = "GITHUB_TOKEN"
    if not os.getenv(token_var):
        logger.error(
            f"GitHub API Token Environment variable '{token_var}' not set. API Search will fail/return no results. Please Setup and retry"
        )
        sys.exit(1)

    try:
        response = requests.get(
            api_url,
            auth=HTTPBasicAuth(os.getenv("BITBUCKET_USER"), os.getenv("BITBUCKET_PASS")),
            timeout=10,
        )
        return response
    except Exception as e:
        logger.error(f"Github API file content get Error: {e}")

    return {}
