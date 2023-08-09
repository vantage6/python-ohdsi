from __future__ import annotations
import re
import rpy2.robjects as ro

from copy import deepcopy
from typing import Any
from rpy2.robjects import pandas2ri
from rpy2.robjects.vectors import ListVector
from rpy2.robjects import RS4
from rpy2.robjects.conversion import localconverter
from pandas import DataFrame, to_datetime
from rpy2.robjects.packages import importr

pattern = re.compile(r'(?<!^)(?=[A-Z])')

base_r = importr('base')


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
    elif ('plot' in name
          and isinstance(item, ro.vectors.ListVector)
          and reserve_plots):
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


def convert_to_r(item: Any) -> Any:
    result = item
    if isinstance(item, dict):
        items = []
        for k, v in item.items():
            safe_ = convert_to_r(v)
            items.append((k, safe_))
        result = ro.vectors.ListVector(items)
    elif isinstance(item, tuple):
        result = ro.vectors.ListVector(item)
    elif isinstance(item, list):
        items = []
        for i in item:
            items.append(convert_to_r(i))
        result = ro.vectors.ListVector.from_iterable(items)
    elif isinstance(item, DataFrame):
        with localconverter(ro.default_converter + pandas2ri.converter):
            result = ro.conversion.py2rpy(item)
    elif isinstance(item, str):
        result = ro.vectors.StrVector([item])
    elif isinstance(item, float):
        result = ro.vectors.FloatVector([item])
    elif isinstance(item, bool):
        result = ro.vectors.BoolVector([item])
    elif isinstance(item, int):
        result = ro.vectors.IntVector([item])
    return result


class ListVectorExtended(ListVector):
    """
    Extended ListVector class to support the additional features:
    - Python style snake case attributes
    - Pythonic setters and getters
    - as_dict() representation
    - __repr__ and _repr_html_ methods
    """
    def __init__(self):
        for name in self.names:
            setattr(self, to_snake_case(name),
                    convert_from_r(self.rx2(name)))
        self.initialized = True

    @classmethod
    def from_list_vector(cls, list_vector: ListVector) -> ListVectorExtended:
        new_list_vector = deepcopy(list_vector)
        new_list_vector.__class__ = cls
        new_list_vector.__init__()
        return new_list_vector

    @property
    def keys(self) -> list[str]:
        return [to_snake_case(n) for n in self.names]

    @property
    def mapping(self) -> dict:
        return {to_snake_case(n): n for n in self.names}

    def as_dict(self) -> dict:
        return {k: convert_from_r(self.__getattr__(k)) for k in self.keys}

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name in self.keys and hasattr(self, 'initialized'):
            try:
                self.rx2[self.mapping[__name]] = convert_to_r(__value)
            except NotImplementedError:
                pass
        else:
            dict.__setattr__(self, __name, __value)

    def __getattr__(self, __name: str) -> Any:
        if __name in self.keys:
            return convert_from_r(self.rx2[self.mapping[__name]])
        else:
            return super().__getattr__(__name)

    def __str__(self):
        r_class = convert_from_r(base_r.attr(self, 'class'))
        return f"<ListVectorExtended of R class '{r_class}'>"

    def __repr__(self):
        lines = [f'{k}: {v}' for k, v in self.as_dict().items()]
        return '{' + '\n'.join(lines) + '}'

    def _repr_html_(self) -> str:
        html = '<table>'
        html += '<tr><th>Attribute</th><th>Value</th><tr>'
        for key, value in self.as_dict().items():
            html += f'<tr><td>{key}</td><td>{value}</td></tr>'
        html += '</html>'
        return html


class RS4Extended(RS4):
    pass