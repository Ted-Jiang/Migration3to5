import json
import requests

from model_migration import KYLIN3, get_request_kylin3, cube_name, get_cube_desc, get_cube_model, KYLIN5, post_request_kylin5, \
    project_name
from request import IndexMigrateRequest


def get_cuboids(cube_name):
    url = KYLIN3 + '/cubes/' + cube_name + '/cuboids/export?top=20';
    res = get_request_kylin3(url)
    res = json.loads(res.text)
    return res


def set_model_indexes(project, model_req):
    url = KYLIN5 + '/index_plans/migration_index'
    res = post_request_kylin5(url, model_req)
    return res


def prepareMigrateRequest(cuboids, model_name, project, index_tables):
    after_modify = []
    for cuboid in cuboids:
        new_id = []
        for col in cuboid:
            if any(col.startswith(table) for table in index_tables):
                new_id.append(col)
            else:
                print("Col is from lookup: " + col)

        if new_id and new_id not in after_modify:
            after_modify.append(new_id)
    request = IndexMigrateRequest(project, model_name, after_modify)
    return request


if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings()

    cube_desc = get_cube_desc(cube_name)
    cube_model = get_cube_model(cube_desc.get('model_name'))
    fact_table = cube_model.get('fact_table_alias')

    index_tables = [fact_table]
    lookups = cube_model.get('lookups')
    # Notice here set all lookup table without precompute
    for lookup in lookups:
        if lookup['kind'] != 'LOOKUP':
            index_tables.append(lookup.get('alias'))
            print('precompute table is:' + lookup.get('alias'))

    print('Fact table is: ' + fact_table)
    cuboids = get_cuboids(cube_name);
    # cuboids = [['LINEITEM.L_RECEIPTDATE','LINEITEM.L_COMMENT','LINEITEM.L_RETURNFLAG'],['LINEITEM.L_COMMENT','LINEITEM.L_RECEIPTDATE','LINEITEM.L_RETURNFLAG'],['LINEITEM.L_RETURNFLAG','LINEITEM.L_COMMENT','LINEITEM.L_RECEIPTDATE']]
    req = prepareMigrateRequest(cuboids, cube_name, project_name, index_tables)
    res = set_model_indexes(project_name, req)

    print(res)
