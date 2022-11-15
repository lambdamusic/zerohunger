#!/usr/bin/env python
# encoding: utf-8

#
from django.shortcuts import render
import requests
import json
import sys
#
from libs.myutils.lists import batches
from libs.myutils.myutils import print_json

from .utils import COUNTRIES_LIST
#
try:
    from settings import DIMENSIONS_API_KEY
except:
    print("SETTINGS NOT FOUND: DIMENSIONS_API_KEY")
    raise

DEBUG_MODE = False  # set to True to print out useful info in the console

TOPICS = [
    {
        'name': 'Undernourishment',
        'color': 'btn-primary'
    },
    {
        'name': 'Food insecurity',
        'color': 'btn-info'
    },
    {
        'name': 'Stunting',
        'color': 'btn-success'
    },
    {
        'name': 'Malnutrition',
        'color': 'btn-danger'
    },
    {
        'name': 'Agricultural productivity',
        'color': 'btn-warning'
    },
    {
        'name': 'Sustainable agriculture',
        'color': 'btn-info'
    },
    {
        'name': 'Genetic diversity',
        'color': 'btn-primary'
    },
    {
        'name': 'Expenditure flows',
        'color': 'btn-warning'
    },
    {
        'name': 'Trade restrictions',
        'color': 'btn-success'
    },
    {
        'name': 'Food commodity markets',
        'color': 'btn-danger'
    },
]

# SDG => Sustainable Development Goals
# MDG => Millennium Development Goals

#
QUERY = """
    search publications in title_abstract_only for "(%s AND SDG) OR (%s AND MDG)%s"
    where (year in [2000:2018]%s) 
    return publications [title+doi+journal+type+issue+volume+pages+doi+times_cited] sort by times_cited limit 20
    return in "facets"
    funders[name + country_name] as "entity_funder" 
    return in "facets" research_orgs[id+name] limit 20
    return in "facets" researchers[id+first_name+last_name]  limit 20
    """

COUNTRY_CLAUSE = " AND %s "

RESTRICT_CLAUSE = """ and publisher="Springer Nature" """

if DEBUG_MODE:
    print("RESTRICT_CLAUSE=", RESTRICT_CLAUSE)


def home(request, topic=None, countryname=None):
    """
    home page (and possibly the only one)
    """
    topics1, topics2 = batches(TOPICS, 2)
    res, tot, q = None, None, None
    searchterm = request.GET.get("s", "")
    country = request.GET.get("country", "")
    restrict = request.GET.get("restrict", "")
    
    if topic: # for REST urls
        searchterm = topic.replace("-", " ").title()

    if countryname:
        country = countryname.replace("-", " ").title()

    if searchterm:
        q = construct_query(searchterm, restrict, country)
        try:
            res = do_query(q)
        except Exception as e:
            print("++++ERROR =>")
            print(q)
            return render(request, 'zerohunger/error.html', {"exception": str(e)})
        tot = res['_stats']['total_count']

    context = {
        'topics1': topics1,
        'topics2': topics2,
        'search_topic': searchterm,
        'topic_id': topic,
        'restrict': restrict,
        'country': country,
        'query': q,
        'res': res,
        'tot': tot,
        'COUNTRIES_LIST': COUNTRIES_LIST,
    }

    return render(request, 'zerohunger/search.html', context)


def construct_query(s, restrict, country):
    if restrict:
        r = RESTRICT_CLAUSE
    else:
        r = ""

    if country:
        c = COUNTRY_CLAUSE % country
    else:
        c = ""

    query = QUERY % (s, s, c, r)
    return query


def do_query(query):
    """
    """
    # login = {'username': DIMENSIONS_USR, 'password': DIMENSIONS_PSW}
    login = {'key': DIMENSIONS_API_KEY}

    #   Send credentials to login url to retrieve token. Raise
    #   an error, if the return code indicates a problem.
    #   Please use the URL of the system you'd like to access the API
    #   in the example below.
    resp = requests.post('https://app.dimensions.ai/api/auth.json', json=login)
    resp.raise_for_status()

    #   Create http header using the generated token.
    headers = {'Authorization': "JWT " + resp.json()['token']}

    #   Execute DSL query.
    resp = requests.post(
        'https://app.dimensions.ai/api/dsl.json', data=query, headers=headers)

    #   Display raw result
    res = resp.json()
    if DEBUG_MODE:  # DEBUG
        print(query)
        print_json(res)
    return res
