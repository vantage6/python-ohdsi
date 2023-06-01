import rpy2.robjects as robjs
import rpy2.robjects as robjects
from rpy2.robjects import default_converter
from rpy2.robjects.conversion import Converter


# def _none2null(none_obj):
#     return robjs.r("NULL")

# none_converter = Converter("None converter")


# @none_converter.py2rpy(type(None))
# def _none2null(none_obj: None) -> robjs.NULL:
#     return robjs.NULL


# conversion_rules = default_converter + none_converter
# @robjects.default_converter.rpy2py.register(robjs.NULL)
# def _r_null_to_none(r_obj):
#     return None


@robjects.default_converter.py2rpy.register(type(None))
def _py_none_to_null(r_obj):
    return robjs.NULL
