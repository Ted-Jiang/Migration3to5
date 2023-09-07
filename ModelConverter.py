import json
import unittest

from request import SimplifiedDimension, SimplifiedMeasure, ParameterDesc

MODEL_REQUEST_TEMPLATE = '''
{
    "project": "",
    "last_modified": 1665664472185,
    "create_time": 1665661809266,
    "version": "4.0.0.0",
    "alias": "",
    "owner": "ADMIN",
    "config_last_modifier": null,
    "config_last_modified": 0,
    "description": "",
    "fact_table": "",
    "fact_table_alias": null,
    "management_type": "MODEL_BASED",
    "join_tables": [],
    "filter_condition": "",
    "partition_desc":  {
        "partition_date_column" : null,
        "partition_date_start" : 0,
        "partition_date_format" : "yyyyMMdd",
        "partition_type" : "APPEND",
        "partition_condition_builder" : "org.apache.kylin.metadata.model.PartitionDesc$DefaultPartitionConditionBuilder"
      },
    "capacity": "MEDIUM",
    "segment_config": {
        "auto_merge_enabled": null,
        "auto_merge_time_ranges": null,
        "volatile_range": null,
        "retention_range": null,
        "create_empty_segment_enabled": false
    },
    "data_check_desc": null,
    "semantic_version": 0,
    "storage_type": 0,
    "model_type": "BATCH",
    "all_named_columns": [
       
    ],
    "all_measures": [
       
    ],
    "recommendations_count": 0,
    "computed_columns": [],
    "canvas": {
        "coordinate": {
            "TEST_SITES": {
                "x": 642.6111178927953,
                "y": 147.83333672417538,
                "width": 220,
                "height": 200
            }
        },
        "zoom": 9
    },
    "multi_partition_desc": null,
    "multi_partition_key_mapping": null,
    "fusion_id": null,

    "simplified_measures": [],
    "simplified_dimensions": []
}
'''


def prepareBasicModelRequest(cube_desc, cube_model, project):
    model = json.loads(MODEL_REQUEST_TEMPLATE)
    print("model_tem", model)
    model['alias'] = cube_desc.get('name')
    model['project'] = project
    lookups = cube_model.get('lookups')

    precompute_look_up_table = []
    # Notice here set all lookup table without precompute
    for lookup in lookups:
        if lookup['kind'] == 'LOOKUP':
            lookup['flattenable'] = 'normalized'
        else:
            precompute_look_up_table.append(lookup.get('alias'))

    model['join_tables'] = lookups
    model['fact_table'] = cube_model.get('fact_table')

    if cube_model.get('partition_desc').get('partition_date_column') is not None:
        partition_date_column = cube_model.get('partition_desc').get('partition_date_column')
        partition_date_format = cube_model.get('partition_desc').get('partition_date_format')
        model['partition_desc']['partition_date_column'] = partition_date_column
        model['partition_desc']['partition_date_format'] = partition_date_format
    else:
        model['partition_desc'] = None

    (simplified_measures, topn_col) = convertMeasureDescToSimplifiedMeasure(cube_desc.get('measures'))

    (simplified_dimensions, other_dimensions) = convertDimensionDescToNamedColumn(cube_desc.get('dimensions'),
                                                                                  precompute_look_up_table, topn_col)

    model['simplified_measures'] = simplified_measures
    model['simplified_dimensions'] = simplified_dimensions
    model['other_columns'] = other_dimensions
    model['with_base_index'] = True

    # Here we need put join columns in fact table in to dimensions if absent
    dims_cols = []
    for d in simplified_dimensions:
        dims_cols.append(d.column)

    for lookup in lookups:
        join_cols = lookup['join']['foreign_key']
        for join_col in join_cols:
            if join_col not in dims_cols:
                t = join_col.split(".")
                dim = {'name': t[0] + '_' + t[1], 'column': t[0] + '.' + t[1]}
                simplified_dimensions.append(dim)

    print("after model", model)
    return model


def convertMeasureName(name):
    if name == '_COUNT_':
        return 'COUNT_ALL'
    else:
        return name


def convertDimensionDescToNamedColumn(dimensions, precompute_table, topn_col):
    res_simplified_dimensions = []
    res_other_dimensions = []
    fact_table_name = dimensions[0].get('table')

    precompute_table.append(fact_table_name)

    for dim in dimensions:
        # If exit lookup table, we make all of them not pre-calculate in kylin5.
        if dim.get('table') in precompute_table:
            col = dim.get('column')
            columnName = dim.get('table') + '_' + col
            aliasDotColumn = dim.get('table') + '.' + col
            res_simplified_dimensions.append(SimplifiedDimension(columnName, aliasDotColumn))
        else:
            col = dim.get('name')
            columnName = dim.get('table') + '_' + col
            aliasDotColumn = dim.get('table') + '.' + col
            res_other_dimensions.append(SimplifiedDimension(columnName, aliasDotColumn))

    for col in topn_col:
        t = col.split(".")
        sd = SimplifiedDimension(t[0] + '_' + t[1], col)
        if sd not in res_other_dimensions:
            res_simplified_dimensions.append(sd)
    # res = json.dumps(res, default=lambda obj: obj.__dict__)
    if len(res_other_dimensions) > 0:
        print("\033[1;32m This cube has derived dimesions!!  \n")
    return (res_simplified_dimensions, res_other_dimensions)


def convertMeasureDescToSimplifiedMeasure(measures):
    res = []
    # MEASURE start with 100000
    i = 100000

    topn_col = []

    for mea in measures:
        new_name = convertMeasureName(mea.get('name'))
        function = mea.get('function')

        if function.get('expression') == 'TOP_N':
            old_parameter = function.get('parameter')
            res_mea = SimplifiedMeasure(i, 'SUM', new_name, 'bigint')
            parameterValues = []
            parameterValues.append(ParameterDesc(old_parameter.get('type'), old_parameter.get('value')))
            res_mea.parameter_value = parameterValues
            while old_parameter.get('next_parameter') is not None:
                old_parameter = old_parameter.get('next_parameter')
                if old_parameter.get('value') not in topn_col:
                    topn_col.append(old_parameter.get('value'))

        else:
            old_parameter = function.get('parameter')
            res_mea = SimplifiedMeasure(i, function.get('expression'), new_name, function.get('returntype'))
            if old_parameter is not None:
                parameterValues = []
                while old_parameter is not None:
                    parameterValues.append(ParameterDesc(old_parameter.get('type'), old_parameter.get('value')))
                    old_parameter = old_parameter.get('next_parameter')
                    res_mea.parameter_value = parameterValues
        res.append(res_mea)
        i += 1

    return (res, topn_col)


class Test(unittest.TestCase):
    STR3 = '''{
     "measures" : [ {
    "name" : "_COUNT_",
    "function" : {
      "expression" : "COUNT",
      "parameter" : {
        "type" : "constant",
        "value" : "1",
        "next_parameter" : null
      },
      "returntype" : "bigint"
    },
    "dependent_measure_ref" : null
  }, {
    "name" : "TOTAL_REVENUE",
    "function" : {
      "expression" : "SUM",
      "parameter" : {
        "type" : "column",
        "value" : "LO_REVENUE",
        "next_parameter" : null
      },
      "returntype" : "bigint"
    },
    "dependent_measure_ref" : null
  },
  {
      "name": "SELLER_FORMAT_HLL",
      "function": {
        "expression": "COUNT_DISTINCT",
        "parameter": {
          "type": "column",
          "value": "TEST_KYLIN_FACT.LSTG_FORMAT_NAME",
          "next_parameter": {
            "type": "column",
            "value": "TEST_KYLIN_FACT.SELLER_ID"
          }
        },
        "returntype": "hllc(10)"
      }
    }
  ]
    }'''

    STR5 = '''{
     "all_measures": [
        {
            "name": "COUNT_ALL",
            "function": {
                "expression": "COUNT",
                "parameters": [
                    {
                        "type": "constant",
                        "value": "1"
                    }
                ],
                "returntype": "bigint"
            },
            "column": null,
            "comment": null,
            "id": 100000,
            "type": "NORMAL",
            "internal_ids": []
        },
        {
            "name": "LO_REVENUE_SUM",
            "function": {
                "expression": "SUM",
                "parameters": [
                    {
                        "type": "column",
                        "value": "LINEORDER.LO_REVENUE"
                    }
                ],
                "returntype": "bigint"
            },
            "column": null,
            "comment": "",
            "id": 100001,
            "type": "NORMAL",
            "internal_ids": []
        }
        ]
        }'''

    def test_change_measure_name(self):
        j3 = json.loads(self.STR3).get('measures')
        print(j3)
        j5 = json.loads(self.STR5).get('all_measures')
        print(j5)
        res = convertMeasureDescToSimplifiedMeasure(j3)
        print(res)
