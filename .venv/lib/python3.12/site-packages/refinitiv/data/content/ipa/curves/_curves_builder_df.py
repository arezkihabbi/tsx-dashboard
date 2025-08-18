from itertools import product

import pandas as pd
from ...._tools import convert_df_columns_to_datetime, convert_dtypes, convert_df_columns_to_datetime_by_idx


def bond_curve_build_df(raw, **kwargs):
    """
    Parameters
    ----------
    raw : dict

    Returns
    -------
    DataFrame

    Examples
    -------
    >>> raw
    ... {
    ...     "data": [
    ...         {
    ...             "error": {
    ...                 "id": "b6f9797d-72c8-4baa-84eb-6a079fc40ec5/b6f9797d-72c8-4baa-84eb-6a079fc40ec5",
    ...                 "code": "QPS-Curves.6",
    ...                 "message": "Invalid input: curveDefinition is missing",
    ...             }
    ...         },
    ...         {
    ...             "curveTag": "test_curve",
    ...             "curveParameters": {
    ...                 "interestCalculationMethod": "Dcb_Actual_Actual",
    ...                 "priceSide": "Mid",
    ...                 "calendarAdjustment": "Calendar",
    ...                 "calendars": ["EMU_FI"],
    ...                 "compoundingType": "Compounded",
    ...                 "useConvexityAdjustment": True,
    ...                 "useSteps": False,
    ...                 "valuationDate": "2022-02-09",
    ...             },
    ...             "curveDefinition": {
    ...                 "availableTenors": ["OIS", "1M", "3M", "6M", "1Y"],
    ...                 "availableDiscountingTenors": ["OIS", "1M", "3M", "6M", "1Y"],
    ...                 "currency": "EUR",
    ...                 "mainConstituentAssetClass": "Swap",
    ...                 "riskType": "InterestRate",
    ...                 "indexName": "EURIBOR",
    ...                 "source": "Refinitiv",
    ...                 "name": "EUR EURIBOR Swap ZC Curve",
    ...                 "id": "9d619112-9ab3-45c9-b83c-eb04cbec382e",
    ...                 "discountingTenor": "OIS",
    ...                 "ignoreExistingDefinition": False,
    ...                 "owner": "Refinitiv",
    ...             },
    ...             "curvePoints": [
    ...                 {
    ...                     "endDate": "2021-02-01",
    ...                     "startDate": "2021-02-01",
    ...                     "discountFactor": 1.0,
    ...                     "ratePercent": 7.040811073443143,
    ...                     "tenor": "0D",
    ...                 },
    ...                 {
    ...                     "endDate": "2021-02-04",
    ...                     "startDate": "2021-02-01",
    ...                     "discountFactor": 0.999442450671571,
    ...                     "ratePercent": 7.040811073443143,
    ...                     "tenor": "1D",
    ...                 },
    ...             ],
    ...         },
    ...     ]
    ... }
    """
    datas = raw.get("data", [])
    datas = datas or []
    dfs = []
    for data in datas:
        error = data.get("error")
        if error:
            continue

        curve_points = data.get("curvePoints")

        for curve_point in curve_points:
            d = {}
            for key, value in curve_point.items():
                values = d.setdefault(key, [])
                values.append(value)

            df = pd.DataFrame(d)
            df = df.convert_dtypes()
            dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)
    df = convert_df_columns_to_datetime(df, "Date", utc=True, delete_tz=True)
    df = convert_dtypes(df)
    return df


def cross_currency_curves_curve_build_df(raw, **kwargs):
    """
    Parameters
    ----------
    raw : dict

    Returns
    -------
    DataFrame

    Examples
    -------
    >>> raw
    ... {
    ... 'data':
    ...    [
    ...        {
    ...            "error": {
    ...                "id": "b6f9797d-72c8-4baa-84eb-6a079fc40ec5/b6f9797d-72c8-4baa-84eb-6a079fc40ec5",
    ...                "code": "QPS-Curves.6",
    ...                "message": "Invalid input: curveDefinition is missing",
    ...            }
    ...        },
    ...        {
    ...            'curveDefinition': {
    ...                'baseCurrency': 'EUR', 'baseIndexName': 'ESTR',
    ...                'quotedCurrency': 'USD', 'quotedIndexName': 'SOFR',
    ...                'crossCurrencyDefinitions': [
    ...                    {
    ...                        'baseCurrency': 'EUR', 'baseIndexName': 'ESTR',
    ...                        'name': 'EUR ESTR/USD SOFR FxCross',
    ...                        'quotedCurrency': 'USD', 'quotedIndexName': 'SOFR',
    ...                        'source': 'Refinitiv', 'isNonDeliverable': False,
    ...                        'mainConstituentAssetClass': 'Swap',
    ...                        'riskType': 'CrossCurrency',
    ...                        'id': 'c9f2e9fb-b04b-4140-8377-8b7e47391486',
    ...                        'ignoreExistingDefinition': False
    ...                    }
    ...                ]
    ...            },
    ...            'curveParameters': {
    ...                'valuationDate': '2021-10-06',
    ...                'interpolationMode': 'Linear',
    ...                'extrapolationMode': 'Constant', 'turnAdjustments': {},
    ...                'ignorePivotCurrencyHolidays': False,
    ...                'useDelayedDataIfDenied': False,
    ...                'ignoreInvalidInstrument': True,
    ...                'marketDataLookBack': {'value': 10, 'unit': 'CalendarDay'}
    ...            },
    ...            'curve': {
    ...                'fxCrossScalingFactor': 1.0, 'fxSwapPointScalingFactor': 10000.0,
    ...                'curvePoints': [
    ...                    {
    ...                        'tenor': 'SPOT', 'startDate': '2021-10-08',
    ...                        'endDate': '2021-10-08',
    ...                        'swapPoint': {'bid': 0.0, 'ask': 0.0, 'mid': 0.0},
    ...                        'outright': {'bid': 1.1556, 'ask': 1.156, 'mid': 1.1558}
    ...                    },
    ...                    {
    ...                        'tenor': 'SN', 'startDate': '2021-10-08',
    ...                        'endDate': '2021-10-12',
    ...                        'instruments': [{'instrumentCode': 'EURSN='}],
    ...                        'swapPoint': {
    ...                            'bid': 0.8399999999997299,
    ...                            'ask': 0.8800000000008801,
    ...                            'mid': 0.860000000000305
    ...                        },
    ...                        'outright': {'bid': 1.155684, 'ask': 1.156088,
    ...                                     'mid': 1.155886}
    ...                    }
    ...                ]
    ...            }
    ...        }
    ...    ]
    ... }
    """
    datas = raw.get("data", [])
    datas = datas or []
    get_curve = (data["curve"] for data in datas if "curve" in data)
    columns_have_level_1 = ("swapPoint", "outright")
    level_1 = ("bid", "ask", "mid")

    curve = next(get_curve, {})
    curve_points = curve.get("curvePoints", [])
    curve_point = max(curve_points, key=lambda x: len(x))
    columns = [key for key in curve_point]
    data_df = _create_data_for_df(curve_points, columns, columns_have_level_1, level_1)

    allcolumns = []
    for name in columns:
        if name in columns_have_level_1:
            allcolumns.extend(list(product([name], level_1)))
        else:
            allcolumns.append((name, ""))

    columns_date_idxs = [index for index, value in enumerate(allcolumns) if "date" in value[0].lower()]
    columns = pd.MultiIndex.from_tuples(allcolumns)
    df = pd.DataFrame(data_df, columns=columns)
    df = convert_df_columns_to_datetime_by_idx(df, columns_date_idxs, utc=True, delete_tz=True)
    df = convert_dtypes(df)
    return df


def _create_data_for_df(curve_points, columns, columns_have_level_1, columns_level_1):
    data_df = []

    for curve_point in curve_points:
        row_data = []
        for name in columns:
            value = curve_point.get(name, pd.NA)
            if name == "instruments" and not pd.isna(value):
                value = [v["instrumentCode"] for v in value if "instrumentCode" in v]
                value = value.pop() if len(value) == 1 else value
            if name in columns_have_level_1:
                value = [value.get(i, pd.NA) for i in columns_level_1]
                row_data.extend(value)
            else:
                row_data.append(value)
        data_df.append(row_data)

    return data_df


def zc_curves_build_df(raw, **kwargs):
    """

    Parameters
    ----------
    raw : dict

    Returns
    -------
    DataFrame
    >>> raw
    ... {
    ...     "data": [
    ...         {
    ...             "curveTag": "TAG",
    ...             "error": {
    ...                 "id": "9fef13f4-6d11-4d71-a388-824ddcc8a95a/9fef13f4-6d11-4d71-a388-824ddcc8a95a",
    ...                 "code": "QPS-Curves.7",
    ...                 "message": "The service failed to find the curve definition",
    ...             },
    ...         },
    ...         {
    ...             "curveParameters": {
    ...                 "extrapolationMode": "None",
    ...                 "interpolationMode": "CubicDiscount",
    ...                 "interestCalculationMethod": "Dcb_Actual_Actual",
    ...                 "priceSide": "Mid",
    ...                 "calendarAdjustment": "Calendar",
    ...                 "calendars": ["EMU_FI"],
    ...                 "compoundingType": "Compounded",
    ...                 "useMultiDimensionalSolver": True,
    ...                 "useConvexityAdjustment": True,
    ...                 "useSteps": False,
    ...                 "convexityAdjustment": {
    ...                     "meanReversionPercent": 3.9012,
    ...                     "volatilityPercent": 0.863,
    ...                 },
    ...                 "valuationDate": "2022-02-09",
    ...             },
    ...             "curveDefinition": {
    ...                 "availableTenors": ["OIS", "1M", "3M", "6M", "1Y"],
    ...                 "availableDiscountingTenors": ["OIS", "1M", "3M", "6M", "1Y"],
    ...                 "currency": "EUR",
    ...                 "mainConstituentAssetClass": "Swap",
    ...                 "riskType": "InterestRate",
    ...                 "indexName": "EURIBOR",
    ...                 "source": "Refinitiv",
    ...                 "name": "EUR EURIBOR Swap ZC Curve",
    ...                 "id": "9d619112-9ab3-45c9-b83c-eb04cbec382e",
    ...                 "discountingTenor": "OIS",
    ...                 "ignoreExistingDefinition": False,
    ...                 "owner": "Refinitiv",
    ...                 "indexTenors": ["OIS", "1M", "3M", "6M", "1Y"],
    ...             },
    ...             "curves": {
    ...                 "OIS": {
    ...                     "curvePoints": [
    ...                         {
    ...                             "endDate": "2022-02-09",
    ...                             "startDate": "2022-02-09",
    ...                             "discountFactor": 1.0,
    ...                             "ratePercent": -0.49456799906775206,
    ...                             "tenor": "0D",
    ...                         },
    ...                         {
    ...                             "endDate": "2022-02-10",
    ...                             "startDate": "2022-02-09",
    ...                             "discountFactor": 1.0000135835178428,
    ...                             "ratePercent": -0.49456799906775206,
    ...                             "tenor": "ON",
    ...                             "instruments": [{"instrumentCode": "EUROSTR="}],
    ...                         },
    ...                     ],
    ...                     "isDiscountCurve": True,
    ...                 },
    ...                 "1M": {
    ...                     "curvePoints": [
    ...                         {
    ...                             "endDate": "2022-02-09",
    ...                             "startDate": "2022-02-09",
    ...                             "discountFactor": 1.0,
    ...                             "ratePercent": -0.5560912053716005,
    ...                             "tenor": "0D",
    ...                         },
    ...                         {
    ...                             "endDate": "2022-02-10",
    ...                             "startDate": "2022-02-09",
    ...                             "discountFactor": 1.0000152780111917,
    ...                             "ratePercent": -0.5560912053716005,
    ...                             "tenor": "ON",
    ...                             "instruments": [{"instrumentCode": "EUROND="}],
    ...                         },
    ...                     ],
    ...                     "isDiscountCurve": False,
    ...                 },
    ...                 "3M": {
    ...                     "curvePoints": [
    ...                         {
    ...                             "endDate": "2022-02-09",
    ...                             "startDate": "2022-02-09",
    ...                             "discountFactor": 1.0,
    ...                             "ratePercent": -0.5560912053716005,
    ...                             "tenor": "0D",
    ...                         },
    ...                         {
    ...                             "endDate": "2022-02-10",
    ...                             "startDate": "2022-02-09",
    ...                             "discountFactor": 1.0000152780111917,
    ...                             "ratePercent": -0.5560912053716005,
    ...                             "tenor": "ON",
    ...                             "instruments": [{"instrumentCode": "EUROND="}],
    ...                         },
    ...                     ],
    ...                     "isDiscountCurve": False,
    ...                 },
    ...                 "6M": {
    ...                     "curvePoints": [
    ...                         {
    ...                             "endDate": "2022-02-09",
    ...                             "startDate": "2022-02-09",
    ...                             "discountFactor": 1.0,
    ...                             "ratePercent": -0.5560912053716005,
    ...                             "tenor": "0D",
    ...                         },
    ...                         {
    ...                             "endDate": "2022-02-10",
    ...                             "startDate": "2022-02-09",
    ...                             "discountFactor": 1.0000152780111917,
    ...                             "ratePercent": -0.5560912053716005,
    ...                             "tenor": "ON",
    ...                             "instruments": [{"instrumentCode": "EUROND="}],
    ...                         },
    ...                     ],
    ...                     "isDiscountCurve": False,
    ...                 },
    ...                 "1Y": {
    ...                     "curvePoints": [
    ...                         {
    ...                             "endDate": "2022-02-09",
    ...                             "startDate": "2022-02-09",
    ...                             "discountFactor": 1.0,
    ...                             "ratePercent": -0.5560912053716005,
    ...                             "tenor": "0D",
    ...                         },
    ...                         {
    ...                             "endDate": "2022-02-10",
    ...                             "startDate": "2022-02-09",
    ...                             "discountFactor": 1.0000152780111917,
    ...                             "ratePercent": -0.5560912053716005,
    ...                             "tenor": "ON",
    ...                             "instruments": [{"instrumentCode": "EUROND="}],
    ...                         },
    ...                     ],
    ...                     "isDiscountCurve": False,
    ...                 },
    ...             },
    ...         },
    ...     ]
    ... }
    """
    datas = raw.get("data", [])
    datas = datas or []
    dfs = []

    for data in datas:
        error = data.get("error")
        if error:
            continue

        curves = data.get("curves")
        for value in curves.values():
            curve_points = value.get("curvePoints")

            d = {}
            for curve_point in curve_points:
                for key, value in curve_point.items():
                    values = d.setdefault(key, [])
                    values.append(value)

            d.pop("instruments", None)

            df = pd.DataFrame(d)
            dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)
    df = convert_df_columns_to_datetime(df, "Date", utc=True, delete_tz=True)
    df = convert_dtypes(df)
    return df


def forward_curve_build_df(raw, **kwargs):
    """

    Parameters
    ----------
    raw : dict

    Returns
    -------
    DataFrame

    Examples
    -------
    >>> raw
    ... {
    ...     "data": [
    ...         {
    ...             "error": {
    ...                 "id": "b6f9797d-72c8-4baa-84eb-6a079fc40ec5/b6f9797d-72c8-4baa-84eb-6a079fc40ec5",
    ...                 "code": "QPS-Curves.6",
    ...                 "message": "Invalid input: curveDefinition is missing",
    ...             }
    ...         },
    ...         {
    ...             "curveTag": "test_curve",
    ...             "curveParameters": {
    ...                 "interestCalculationMethod": "Dcb_Actual_Actual",
    ...                 "priceSide": "Mid",
    ...                 "calendarAdjustment": "Calendar",
    ...                 "calendars": ["EMU_FI"],
    ...                 "compoundingType": "Compounded",
    ...                 "useConvexityAdjustment": True,
    ...                 "useSteps": False,
    ...                 "valuationDate": "2022-02-09",
    ...             },
    ...             "curveDefinition": {
    ...                 "availableTenors": ["OIS", "1M", "3M", "6M", "1Y"],
    ...                 "availableDiscountingTenors": ["OIS", "1M", "3M", "6M", "1Y"],
    ...                 "currency": "EUR",
    ...                 "mainConstituentAssetClass": "Swap",
    ...                 "riskType": "InterestRate",
    ...                 "indexName": "EURIBOR",
    ...                 "source": "Refinitiv",
    ...                 "name": "EUR EURIBOR Swap ZC Curve",
    ...                 "id": "9d619112-9ab3-45c9-b83c-eb04cbec382e",
    ...                 "discountingTenor": "OIS",
    ...                 "ignoreExistingDefinition": False,
    ...                 "owner": "Refinitiv",
    ...             },
    ...             "forwardCurves": [
    ...                 {
    ...                     "curvePoints": [
    ...                         {
    ...                             "endDate": "2021-02-01",
    ...                             "startDate": "2021-02-01",
    ...                             "discountFactor": 1.0,
    ...                             "ratePercent": 7.040811073443143,
    ...                             "tenor": "0D",
    ...                         },
    ...                         {
    ...                             "endDate": "2021-02-04",
    ...                             "startDate": "2021-02-01",
    ...                             "discountFactor": 0.999442450671571,
    ...                             "ratePercent": 7.040811073443143,
    ...                             "tenor": "1D",
    ...                         },
    ...                     ],
    ...                     "forwardCurveTag": "ForwardTag",
    ...                     "forwardStart": "2021-02-01",
    ...                     "indexTenor": "3M",
    ...                 }
    ...             ],
    ...         },
    ...     ]
    ... }
    """
    datas = raw.get("data", [])
    datas = datas or []
    dfs = []
    for data in datas:
        if data.get("error"):
            continue

        forward_curves = data.get("forwardCurves")

        for forward_curve in forward_curves:
            if forward_curve.get("error"):
                continue

            curve_points = forward_curve.get("curvePoints")

            d = {}
            for curve_point in curve_points:
                for key, value in curve_point.items():
                    values = d.setdefault(key, [])
                    values.append(value)

            df = pd.DataFrame(d)
            df = df.convert_dtypes()
            dfs.append(df)

    if not dfs:
        df = pd.DataFrame()

    else:
        df = pd.concat(dfs, ignore_index=True)
        df = convert_df_columns_to_datetime(df, "Date", utc=True, delete_tz=True)
        df = convert_dtypes(df)

    return df


def zc_curve_definitions_build_df(raw, **kwargs):
    data = raw.get("data", [])
    data = data or []
    curve_definitions = [d for d in data if d for d in d.get("curveDefinitions")]
    df = pd.DataFrame(curve_definitions)

    if not df.empty:
        df = convert_df_columns_to_datetime(df, "Date", utc=True, delete_tz=True)
        df = convert_dtypes(df)
    return df


def cross_currency_curves_definitions_search_build_df(raw, **kwargs):
    return zc_curve_definitions_build_df(raw)
