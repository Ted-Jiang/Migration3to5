class TableLoadRequest:
    def __init__(self, project, tables):
        self.project = project
        self.tables = tables
        self.databases = []
        self.needSampling = False
        self.samplingRows = 200000
        self.priority = 3
        self.yarnQueue = None
        self.tag = None


class ModelRequest:
    def __init__(self, simplifiedMeasures, simplifiedDimensions, project):
        self.project = project
        self.simplifiedMeasures = simplifiedMeasures
        self.simplifiedDimensions = simplifiedDimensions
        self.start = ''
        self.end = ''


class SimplifiedMeasure:
    def __init__(self, id, expression, name, returnType):
        self.id = id
        self.expression = expression
        self.name = name
        self.returnType = returnType
        self.comment = ''
        # Assume no parameterValue
        self.parameter_value = []
        self.column = ''


class SimplifiedDimension:
    def __init__(self, name, column):
        self.name = name
        self.column = column


class ParameterDesc:
    def __init__(self, type, value):
        self.type = type
        self.value = value


class IndexMigrateRequest:
    def __init__(self, project, model_name, col_orders):
        self.project = project
        self.model_name = model_name
        self.col_orders = col_orders
