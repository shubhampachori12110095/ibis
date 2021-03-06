import pytest
from pytest import param

import numpy as np

import ibis.tests.util as tu


@pytest.mark.parametrize(
    ('result_func', 'expected_func'),
    [
        param(
            lambda t, where: t.bool_col.count(where=where),
            lambda t, where: len(t.bool_col[where].dropna()),
            id='bool_col_count'
        ),
        param(
            lambda t, where: t.bool_col.any(),
            lambda t, where: t.bool_col.any(),
            id='bool_col_any'
        ),
        param(
            lambda t, where: t.bool_col.notany(),
            lambda t, where: ~t.bool_col.any(),
            id='bool_col_notany'
        ),
        param(
            lambda t, where: -t.bool_col.any(),
            lambda t, where: ~t.bool_col.any(),
            id='bool_col_any_negate'
        ),
        param(
            lambda t, where: t.bool_col.all(),
            lambda t, where: t.bool_col.all(),
            id='bool_col_all'
        ),
        param(
            lambda t, where: t.bool_col.notall(),
            lambda t, where: ~t.bool_col.all(),
            id='bool_col_notall'
        ),
        param(
            lambda t, where: -t.bool_col.all(),
            lambda t, where: ~t.bool_col.all(),
            id='bool_col_all_negate'
        ),
        param(
            lambda t, where: t.double_col.sum(),
            lambda t, where: t.double_col.sum(),
            id='double_col_sum',
        ),
        param(
            lambda t, where: t.double_col.mean(),
            lambda t, where: t.double_col.mean(),
            id='double_col_mean',
        ),
        param(
            lambda t, where: t.double_col.min(),
            lambda t, where: t.double_col.min(),
            id='double_col_min',
        ),
        param(
            lambda t, where: t.double_col.max(),
            lambda t, where: t.double_col.max(),
            id='double_col_max',
        ),
        param(
            lambda t, where: t.double_col.approx_median(),
            lambda t, where: t.double_col.median(),
            id='double_col_approx_median',
            marks=pytest.mark.xfail,
        ),
        param(
            lambda t, where: t.double_col.std(how='sample'),
            lambda t, where: t.double_col.std(ddof=1),
            id='double_col_std',
        ),
        param(
            lambda t, where: t.double_col.var(how='sample'),
            lambda t, where: t.double_col.var(ddof=1),
            id='double_col_var',
        ),
        param(
            lambda t, where: t.double_col.std(how='pop'),
            lambda t, where: t.double_col.std(ddof=0),
            id='double_col_std_pop',
        ),
        param(
            lambda t, where: t.double_col.var(how='pop'),
            lambda t, where: t.double_col.var(ddof=0),
            id='double_col_var_pop',
        ),
        param(
            lambda t, where: t.string_col.approx_nunique(),
            lambda t, where: t.string_col.nunique(),
            id='string_col_approx_nunique',
            marks=pytest.mark.xfail,
        ),
        param(
            lambda t, where: t.string_col.group_concat(','),
            lambda t, where: ','.join(t.string_col),
            id='string_col_group_concat',
            marks=pytest.mark.xfail,
        ),
    ],
)
@pytest.mark.parametrize(
    ('ibis_cond', 'pandas_cond'),
    [
        (lambda t: None, lambda t: slice(None)),
        (
            lambda t: t.string_col.isin(['1', '7']),
            lambda t: t.string_col.isin(['1', '7']),
        )
    ]
)
@tu.skip_if_invalid_operation
@pytest.mark.backend
def test_aggregation(
    backend, alltypes, df, result_func, expected_func, ibis_cond, pandas_cond
):
    expr = result_func(alltypes, ibis_cond(alltypes))
    result = expr.execute()
    expected = expected_func(df, pandas_cond(df))
    np.testing.assert_allclose(result, expected)
