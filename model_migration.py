# This is a sample Python script.
import argparse
from getpass import getpass

import requests
import json

from ModelConverter import prepareBasicModelRequest
from request import TableLoadRequest

user = input("Username: ")
cube_name = input("CubeName: ")
project_name = input("Project Name: ")
pwd = getpass("Password (Bin + Yubikey): ")

http_proxy_url = "http://" + user + ":" + pwd + "@xxxxm:8080"
https_proxy_url = "https://" + user + ":" + pwd + "@xxx:8443"

proxies = {
    "http": http_proxy_url,
    "https": https_proxy_url
}


KYLIN3 = 'http://kylin.rno.corp.xxx.com/kylin/api'


KYLIN5 = 'https://kylin-qa.vip.xxx.com/kylin/api'

# KYLIN5 = 'http://localhost:8080/kylin/api'
# KYLIN5_AUTH_MD5 = 'Basic QURNSU46S1lMSU4='

kylin3headers = {
    "Authorization": KYLIN3_AUTH_MD5,
    "Content-Type": "application/json",
}

kylin5headers = {
    "Authorization": KYLIN5_AUTH_MD5,
    "Content-Type": "application/json",
}


def get_request_kylin3(url):
    print(url)
    res = requests.get(url, headers=kylin3headers, proxies=proxies)
    if res.status_code != 200:
        print(url + 'request fail')
    return res


def get_request_kylin4(url):
    print(url)
    res = requests.get(url, headers=kylin5headers, proxies=proxies)
    if res.status_code != 200:
        print(url + 'request fail')
    return res


def post_request_kylin5(url, req):
    print(url)
    print(json.dumps(req, default=lambda obj: obj.__dict__))
    res = requests.post(url, headers=kylin5headers, data=json.dumps(req, default=lambda obj: obj.__dict__), proxies=proxies)
    if res.status_code != 200:
        print(url + ' request fail. code: %s', res.status_code)
    print(res.text)
    return res


def post_request_kylin4_without_json_dump(url, req):
    print(url)
    res = requests.post(url, headers=kylin5headers, data=req, proxies=proxies)
    if res.status_code != 200:
        print(url + ' request fail. code: %s', res.status_code)
    print(res.text)
    return res


def get_tables_from_project(project):
    url = KYLIN3 + '/tables?ext=true&page_size=1000000&project=' + project
    res = get_request_kylin3(url)
    res = json.loads(res.text)
    database_list = [(item.get('database') + '.' + item.get('name')) for item in res]
    print("load tables from project: " + project)
    print(database_list)
    return database_list


def set_tables_to_project(project, tables):
    def chunks(lst, size):
        # Helper function to divide the list into chunks
        for i in range(0, len(lst), size):
            yield lst[i:i + size]

    def process_chunk(chunk):
        url = KYLIN5 + '/tables'
        req = TableLoadRequest(project, chunk)
        res = post_request_kylin5(url, req)
        return res

    chunk_size = 50
    results = []

    for chunk in chunks(tables, chunk_size):
        result = process_chunk(chunk)
        results.append(result)

    return results


def set_model_to_project(project, model_req):
    url = KYLIN5 + '/models'
    res = post_request_kylin5(url, model_req)
    return res


def get_cube_desc(cubename):
    url = KYLIN3 + '/cube_desc/' + cubename
    res = get_request_kylin3(url)
    # assume only one result
    res = json.loads(res.text)[0]
    return res


def get_cube_model(model_name):
    url = KYLIN3 + '/model/' + model_name
    res = get_request_kylin3(url)
    res = json.loads(res.text)
    return res


# this function will load all tables from
def root_migrate_table_3_to_5(project):
    res = get_tables_from_project(project)
    wait = set_tables_to_project(project, res)
    return wait


if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings()

    cube_desc = get_cube_desc(cube_name)
    print("cube_desc: %s", cube_desc)
    cube_model = get_cube_model(cube_desc.get('model_name'))
    print("cube_model: %s", cube_model)

    model_req = prepareBasicModelRequest(cube_desc, cube_model, project_name)
    res = set_model_to_project(project_name, model_req)
    if res.status_code == 200:
        print("MIGRATE SUCCESS")
    else:
        print("MIGRATE FAIL")

    # Use this function to migrate whole project table
    # root_migrate_table_3_to_5(project_name)
