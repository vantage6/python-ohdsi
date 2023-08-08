import re
import rpy2.robjects as ro

from typing import Any
from rpy2.robjects import pandas2ri
from rpy2.robjects.vectors import ListVector
from rpy2.robjects.conversion import localconverter
from pandas import DataFrame, to_datetime, Series

pattern = re.compile(r'(?<!^)(?=[A-Z])')


def to_snake_case(name: str) -> str:
    return pattern.sub('_', name).lower()


# https://medium.com/appsflyerengineering/running-r-model-in-a-python-environment-7e8971dfe5f9
def convert_df_dates_from_r(df: DataFrame, date_cols: 'list[str]' = None) \
        -> DataFrame:
    """ convert given date columns into pandas datetime with UTC timezone

    Args:
        df (pd.DataFrame): The pandas dataframe
        date_cols (list[str], optional): _description_. Defaults to None.

    Returns:
        pd.DataFrame: The dataframe with the converted
    """
    result = df.copy()
    if date_cols is not None:
        for col in (set(date_cols) & set(result.columns)):
            result[col] = to_datetime(
                result[col], unit='D', origin='1970-1-1').dt.tz_localize('UTC')


def convert_from_r(item: Any, date_cols: 'list[str]' = None, name: str = '',
                   reserve_plots: bool = True) -> Any:
    result = item
    remove_list: bool = True
    if item == ro.vectors.NULL:
        return None
    elif 'plot' in name and isinstance(item, ro.vectors.ListVector) and reserve_plots:
        return item
    elif isinstance(item, (ro.environments.Environment,
                           ro.Formula)):
        return None
    elif isinstance(item, ro.vectors.DataFrame):
        with localconverter(ro.default_converter + pandas2ri.converter):
            result = ro.conversion.rpy2py(item)
        result = convert_df_dates_from_r(result, date_cols)
        remove_list = False
    elif isinstance(item, (ro.vectors.StrVector,
                           ro.vectors.FloatVector,
                           ro.vectors.BoolVector,
                           ro.vectors.IntVector)):
        result = tuple(item)
    elif isinstance(item, ro.vectors.ListVector):
        result = {}
        remove_list = False

        if item.names == ro.vectors.NULL:
            if len(item) > 0:
                result = [convert_from_r(i, date_cols) for i in item]
            else:
                result = []

        elif len(item) > 0:
            result = dict(zip(item.names, list(item)))
            for k, v in result.items():
                result[k] = convert_from_r(v, date_cols, name=k)

    if '__len__' in result.__dir__() and len(result) == 1 and remove_list:
        result = result[0]

    return result


class ListVectorWrapper:
    """
    Wrapper class for R ListVector objects

    Properties
    ----------
    r_obj_in : ListVector
        The R ListVector object

    Methods
    -------
    properties
        Returns the listed properties of the R object

    mapping
        Returns the mapping between the R object and the python object


    """

    def __init__(self, r_obj_in: ListVector) -> None:
        # self.__class__ = CovariateSettings
        self.r_obj = r_obj_in
        # print(r_obj_in)

        # assign the R properties to the python object, with snake case
        for name in self.r_keys:
            setattr(self, to_snake_case(name),
                    convert_from_r(self.r_obj.rx2(name)))

        self.initialized = True

    @property
    def keys(self):
        # check if the r_obj has been set
        if 'r_obj' not in self.__dict__:
            return []

        return [to_snake_case(n) for n in self.r_obj.names]

    @property
    def r_keys(self):
        if 'r_obj' not in self.__dict__:
            return []

        return self.r_obj.names

    @property
    def properties(self):
        if 'initialized' not in self.__dict__:
            return {}

        properties = self.__dict__.copy()

        # remove class properties
        properties.pop('r_obj')
        properties.pop('initialized')

        return properties

    @property
    def mapping(self):
        return {to_snake_case(n): n for n in self.r_obj.names}

    def __setattr__(self, __name: str, __value: Any) -> None:

        if 'initialized' not in self.__dict__:
            dict.__setattr__(self, __name, __value)

        elif __name in self.keys:
            r_var = self.mapping[__name]
            self.r_obj.rx2[r_var] = __value
            super().__setattr__(__name, __value)
        else:
            dict.__setattr__(self, __name, __value)

    def __repr__(self) -> str:
        return Series(self.properties).__repr__()
