from __future__ import annotations
import os
import re
import pandas as pd
import rpy2.robjects as ro

from copy import deepcopy
from typing import Any
from rpy2.robjects import pandas2ri
from rpy2.robjects.vectors import ListVector
from rpy2.robjects import RS4
from rpy2.robjects.conversion import localconverter
from rpy2.robjects.pandas2ri import rpy2py_dataframe
from rpy2.robjects.packages import importr

pattern = re.compile(r'(?<!^)(?=[A-Z])')

if os.environ.get('IGNORE_R_IMPORTS', False):
    base_r = None
    fe_r = None
else:
    base_r = importr('base')
    fe_r = importr("FeatureExtraction")


def to_snake_case(name: str) -> str:
    return pattern.sub('_', name).lower()


# https://medium.com/appsflyerengineering/running-r-model-in-a-python-environment-7e8971dfe5f9
def convert_df_dates_from_r(df: pd.DataFrame, date_cols: 'list[str]' = None) \
        -> pd.DataFrame:
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
            result[col] = pd.to_datetime(
                result[col], unit='D', origin='1970-1-1').dt.tz_localize('UTC')

    return result


def convert_bool_from_r(bool_vector: ro.vectors.BoolVector) -> bool:
    return tuple(bool_vector)[0]


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
    elif isinstance(item, pd.DataFrame):
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


def andromeda_to_df(andromeda_table: RS4) -> pd.DataFrame:
    r_df = base_r.data_frame(andromeda_table)
    return rpy2py_dataframe(r_df)


class RS4Extended(RS4):

    @property
    def attributes(self) -> list[str]:
        return convert_from_r(base_r.attributes(self))

    def attr(self, attribute: str) -> Any:
        return convert_from_r(base_r.attr(self, attribute))

    @property
    def r_class(self) -> str:
        return str(self.slots['class'][0])

    @property
    def properties(self) -> list[str]:
        return list(self.names)

    def extract(self, property: str) -> Any:
        return base_r.__dict__["$"](self, property)

    def as_RS4(self) -> RS4:
        self_copy = deepcopy(self)
        self_copy.__class__ = RS4
        return self_copy

    @classmethod
    def from_RS4(cls, rs4: RS4) -> RS4Extended:
        rs4.__class__ = cls
        return rs4

    def __str__(self):
        return f"<RS4Extended of R class '{self.r_class}'>"

    def __repr__(self):
        return self.__str__()


class CovariateData(RS4Extended):

    def summary(self):
        fe_r = importr("FeatureExtraction")
        print(fe_r.summary(self))

    @classmethod
    def from_RS4(cls, rs4: RS4) -> CovariateData:
        rs4.__class__ = cls
        for prop in rs4.properties:
            setattr(
                rs4,
                to_snake_case(prop),
                andromeda_to_df(rs4.extract(prop))
            )
        return rs4

    def __str__(self):
        return f"<CovariateData of R class '{self.r_class}'>"


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

    def as_list_vector(self) -> ListVector:
        self_copy = deepcopy(self)
        self_copy.__class__ = ListVector
        return self_copy

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
