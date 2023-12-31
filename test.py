TEST_3SSB_DESC = '''
{
  "uuid" : "5c44df30-daec-486e-af90-927bf7851057",
  "name" : "ssb",
  "description" : "",
  "dimensions" : [ {
    "name" : "SSB.PART_DERIVED",
    "table" : "SSB.PART",
    "column" : null,
    "derived" : [ "P_MFGR" ]
  }, {
    "name" : "SSB.PART_DERIVED",
    "table" : "SSB.PART",
    "column" : null,
    "derived" : [ "P_CATEGORY" ]
  }, {
    "name" : "SSB.PART_DERIVED",
    "table" : "SSB.PART",
    "column" : null,
    "derived" : [ "P_BRAND" ]
  }, {
    "name" : "C_CITY",
    "table" : "SSB.CUSTOMER",
    "column" : "C_CITY",
    "derived" : null
  }, {
    "name" : "C_REGION",
    "table" : "SSB.CUSTOMER",
    "column" : "C_REGION",
    "derived" : null
  }, {
    "name" : "C_NATION",
    "table" : "SSB.CUSTOMER",
    "column" : "C_NATION",
    "derived" : null
  }, {
    "name" : "S_CITY",
    "table" : "SSB.SUPPLIER",
    "column" : "S_CITY",
    "derived" : null
  }, {
    "name" : "S_REGION",
    "table" : "SSB.SUPPLIER",
    "column" : "S_REGION",
    "derived" : null
  }, {
    "name" : "S_NATION",
    "table" : "SSB.SUPPLIER",
    "column" : "S_NATION",
    "derived" : null
  }, {
    "name" : "D_YEAR",
    "table" : "SSB.DATES",
    "column" : "D_YEAR",
    "derived" : null
  }, {
    "name" : "D_YEARMONTH",
    "table" : "SSB.DATES",
    "column" : "D_YEARMONTH",
    "derived" : null
  }, {
    "name" : "D_YEARMONTHNUM",
    "table" : "SSB.DATES",
    "column" : "D_YEARMONTHNUM",
    "derived" : null
  }, {
    "name" : "D_WEEKNUMINYEAR",
    "table" : "SSB.DATES",
    "column" : "D_WEEKNUMINYEAR",
    "derived" : null
  } ],
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
  }, {
    "name" : "TOTAL_SUPPLYCOST",
    "function" : {
      "expression" : "SUM",
      "parameter" : {
        "type" : "column",
        "value" : "LO_SUPPLYCOST",
        "next_parameter" : null
      },
      "returntype" : "bigint"
    },
    "dependent_measure_ref" : null
  }, {
    "name" : "TOTAL_V_REVENUE",
    "function" : {
      "expression" : "SUM",
      "parameter" : {
        "type" : "column",
        "value" : "V_REVENUE",
        "next_parameter" : null
      },
      "returntype" : "bigint"
    },
    "dependent_measure_ref" : null
  } ],
  "rowkey" : {
    "rowkey_columns" : [ {
      "column" : "LO_PARTKEY",
      "encoding" : "dict"
    }, {
      "column" : "C_CITY",
      "encoding" : "dict"
    }, {
      "column" : "C_REGION",
      "encoding" : "dict"
    }, {
      "column" : "C_NATION",
      "encoding" : "dict"
    }, {
      "column" : "S_CITY",
      "encoding" : "dict"
    }, {
      "column" : "S_REGION",
      "encoding" : "dict"
    }, {
      "column" : "S_NATION",
      "encoding" : "dict"
    }, {
      "column" : "D_YEAR",
      "encoding" : "dict"
    }, {
      "column" : "D_YEARMONTH",
      "encoding" : "dict"
    }, {
      "column" : "D_YEARMONTHNUM",
      "encoding" : "dict"
    }, {
      "column" : "D_WEEKNUMINYEAR",
      "encoding" : "dict"
    } ]
  },
  "signature" : "5iV8LVYs+PmVUju8QNQ5TQ==",
  "last_modified" : 1457503036686,
  "model_name" : "ssb",
  "null_string" : null,
  "hbase_mapping" : {
    "column_family" : [ {
      "name" : "F1",
      "columns" : [ {
        "qualifier" : "M",
        "measure_refs" : [ "_COUNT_", "TOTAL_REVENUE", "TOTAL_SUPPLYCOST", "TOTAL_V_REVENUE" ]
      } ]
    } ]
  },
  "aggregation_groups" : [ {
    "includes" : [ "LO_PARTKEY", "C_CITY", "C_REGION", "C_NATION", "S_CITY", "S_REGION", "S_NATION", "D_YEAR", "D_YEARMONTH", "D_YEARMONTHNUM", "D_WEEKNUMINYEAR" ],
    "select_rule" : {
      "hierarchy_dims" : [ [ "C_REGION", "C_NATION", "C_CITY" ], [ "S_REGION", "S_NATION", "S_CITY" ], [ "D_YEARMONTH", "D_YEARMONTHNUM", "D_WEEKNUMINYEAR" ] ],
      "mandatory_dims" : [ "D_YEAR" ],
      "joint_dims" : [ ]
    }
  } ],
  "notify_list" : [ ],
  "status_need_notify" : [ ],
  "partition_date_start" : 694224000000,
  "partition_date_end" : 3153600000000,
  "auto_merge_time_ranges" : [ 604800000, 2419200000 ],
  "retention_range" : 0,
  "engine_type" : 2,
  "storage_type" : 2,
  "override_kylin_properties" : {
    "kylin.storage.hbase.compression-codec" : "lz4",
    "kylin.cube.aggrgroup.is-mandatory-only-valid" : "true"
  }
}

'''

TEST_3SSB_MODEL = '''
{
  "uuid" : "cd92588f-b987-4a12-b90f-e32c44345c64",
  "version" : "2.1",
  "name" : "ssb",
  "description" : "",
  "lookups" : [ {
    "table" : "SSB.PART",
    "join" : {
      "type" : "left",
      "primary_key" : [ "P_PARTKEY" ],
      "foreign_key" : [ "LO_PARTKEY" ]
    }
  }, {
    "table" : "SSB.CUSTOMER",
    "join" : {
      "type" : "left",
      "primary_key" : [ "C_CUSTKEY" ],
      "foreign_key" : [ "LO_CUSTKEY" ]
    }
  }, {
    "table" : "SSB.SUPPLIER",
    "join" : {
      "type" : "left",
      "primary_key" : [ "S_SUPPKEY" ],
      "foreign_key" : [ "LO_SUPPKEY" ]
    }
  }, {
    "table" : "SSB.DATES",
    "join" : {
      "type" : "left",
      "primary_key" : [ "D_DATEKEY" ],
      "foreign_key" : [ "LO_ORDERDATE" ]
    }
  } ],
  "dimensions" : [ {
    "table" : "P_LINEORDER",
    "columns" : [ "LO_COMMITDATE", "LO_PARTKEY", "LO_CUSTKEY", "LO_ORDERDATE", "LO_SUPPKEY" ]
  }, {
    "table" : "PART",
    "columns" : [ "P_MFGR", "P_CATEGORY", "P_BRAND", "P_PARTKEY" ]
  }, {
    "table" : "CUSTOMER",
    "columns" : [ "C_CITY", "C_NATION", "C_REGION", "C_CUSTKEY" ]
  }, {
    "table" : "SUPPLIER",
    "columns" : [ "S_CITY", "S_NATION", "S_REGION", "S_SUPPKEY" ]
  }, {
    "table" : "DATES",
    "columns" : [ "D_YEAR", "D_YEARMONTHNUM", "D_YEARMONTH", "D_WEEKNUMINYEAR", "D_DATEKEY" ]
  } ],
  "metrics" : [ "LO_REVENUE", "LO_SUPPLYCOST", "V_REVENUE" ],
  "last_modified" : 1457444314662,
  "fact_table" : "SSB.P_LINEORDER",
  "filter_condition" : "",
  "partition_desc" : {
    "partition_date_column" : "SSB.P_LINEORDER.LO_COMMITDATE",
    "partition_time_column" : null,
    "partition_date_start" : 0,
    "partition_date_format" : "yyyyMMdd",
    "partition_time_format" : "HH:mm:ss",
    "partition_type" : "APPEND",
    "partition_condition_builder" : "org.apache.kylin.metadata.model.PartitionDesc$DefaultPartitionConditionBuilder"
  }
}
'''
