import requests

from ModelConverter import prepareBasicModelRequest
from build import get_cube_storage, build_model
from index_migrate import get_cuboids, prepareMigrateRequest, set_model_indexes
from model_migration import get_cube_desc, cube_name, get_cube_model, set_model_to_project, project_name

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

    # 2
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
    req = prepareMigrateRequest(cuboids, cube_name, project_name, index_tables)
    res = set_model_indexes(project_name, req)

    # 3
    ss = get_cube_storage(cube_name)

    for s in ss:
        start = s.get('dateRangeStart')
        end = s.get('dateRangeEnd')
        res = build_model(cube_name, start, end)
        print(res)