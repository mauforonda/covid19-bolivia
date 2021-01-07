#!/usr/bin/env python3
# coding: utf-8

import io
import requests

import numpy as np
import pandas as pd
import datetime as dt


URL = 'https://opendata.arcgis.com/datasets/89873d02cfef44928668711cae827105_0.csv'
TIMEOUT = 30
RETRY_M = 3

feature_map = {
    'TOTAL_CASES': 'confirmados',
    'TOTAL_DEATHS': 'decesos'
}


def do_fetch(_try=1):
    try:
        req = requests.get(URL, timeout=TIMEOUT)
        raw = pd.read_csv(io.BytesIO(req.content))

    except Exception as e: # :S
        if _try > RETRY_M:
            raise(e)

        do_fetch(_try + 1)

    return raw


def do_format(df):
    df = df[df['ISO3_CODE'] == 'BOL']
    df = df.loc[df['POP2018'].dropna().index]

    df = df[['DATA_DATE', 'ADM1', 'TOTAL_CASES', 'TOTAL_DEATHS']]
    df['DATA_DATE'] = pd.to_datetime(df['DATA_DATE']) - dt.timedelta(days=1)

    df = df.set_index('ADM1').T
    df = df.rename(columns={'Potosi': 'Potosí'}, index=feature_map)
    df.columns.name = None

    features_date = df.loc['DATA_DATE'][0]

    df = df.loc[['confirmados', 'decesos']]
    df['Fecha'] = features_date

    df = df[np.roll(df.columns, shift=1)]

    return df


def do_patch(feature_df, feature):
    patches = pd.read_csv(
        './patches/{}.csv'.format(feature),
        parse_dates=True,
        index_col='Fecha'
    )

    feature_df = pd.concat([feature_df, patches], sort=False)
    feature_df = feature_df[~feature_df.index.duplicated(keep='last')]

    return feature_df.sort_index(ascending=False)


def do_merge(df, feature):
    feature_df = pd.read_csv(
        './{}.csv'.format(feature),
        parse_dates=True,
        index_col='Fecha'
    )

    feature_df = pd.concat(
        [feature_df, df.loc[[feature]].set_index('Fecha')],
        sort=False
    )
    feature_df = feature_df[~feature_df.index.duplicated(keep='last')]

    return feature_df.sort_index(ascending=False)


def merge_features(df):
    for feature in feature_map.values():
        feature_df = do_merge(df, feature)
        feature_df = do_patch(feature_df, feature)

        feature_df.to_csv('./{}.csv'.format(feature))


if __name__ == '__main__':
    df = do_fetch()

    if df is not None:
        df = do_format(df)
        merge_features(df)
