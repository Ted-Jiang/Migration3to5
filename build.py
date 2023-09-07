import json
import requests

from model_migration import KYLIN3, get_request_kylin3, cube_name, KYLIN5, post_request_kylin5, \
    project_name


def get_cube_storage(cubename):
    url = KYLIN3 + '/cubes/' + cubename + '/hbase'
    res = get_request_kylin3(url)
    # assume only one result
    res = json.loads(res.text)
    return res


def build_model(model_name, start, end):
    url = KYLIN5 + '/models/' + model_name + '/model_segments/' + str(start) + '/' + str(end) + '/' + project_name
    res = post_request_kylin5(url, '')
    return res


# 1682208000000
if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings()

    ss = get_cube_storage(cube_name)
    len = str(len(ss))
    print("Total " + len + " jobs")
    for s in ss:
        start = s.get('dateRangeStart')
        end = s.get('dateRangeEnd')
        res = build_model(cube_name, start, end)
        print(res)
