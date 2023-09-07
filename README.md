# Migration3to5

A tool to create Kylin5 model base on Kylin3 cube


1. [model_migration.py](model_migration.py) : Convert kylin3 (model + cube) to kylin5 model
2. [index_migrate.py](index_migrate.py) : Convert kylin3 (cuboid) to kylin5 (index) 
   1. "/cuboids/export?top=10" here change 10 to X to migrate x indexes.  
3. [build.py]( build.py): Build all indexes of kylin5 model according to the kylin3 segments range.