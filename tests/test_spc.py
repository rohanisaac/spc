import os
from os.path import join, dirname

import numpy as np
import pandas as pd
from numpy.testing import assert_allclose

import spc


def _list_all_spc_files():
    """List the spc files in the data folders."""
    path_data = join(dirname(__file__), 'data')
    filenames = [filename
                 for filename in os.listdir(path_data)
                 if filename.lower().endswith('spc')]
    return filenames


def _split_data(spc_file):
    """Reorganize into numpy format the data depending of the format.

    Parameters
    ----------
    spc_file : spc.File
        The spc.File object to be reorganized to ease the testing.

    Returns
    -------
    X : ndarray, shape (n_spectra, n_frequency) or (n_frequency,)
        The x axis.

    Y : ndarray shape (n_spectra, n_frequency)
        The y axis.

    """
    if (spc_file.dat_fmt == 'gx-y' or
            spc_file.dat_fmt == 'x-y'):
        X = spc_file.x
    elif spc_file.dat_fmt == '-xy':
        X = np.array([f.x for f in spc_file.sub])
    Y = np.array([f.y for f in spc_file.sub])

    return X, Y


def _read_expected_file(spc_filename, spc_file_format):
    """Reorganize into numpy format the data depending of the format.

    Parameters
    ----------
    spc_filename : str
        The filename of the SPC file which will be checked.

    spc_file_format : str
        The format of the SPC file: '-xy', 'x-y', or 'gx-y'.

    Returns
    -------
    X : ndarray, shape (n_spectra, n_frequency) or (n_frequency,)
        The x axis.

    Y : ndarray shape (n_spectra, n_frequency)
        The y axis.

    """
    path_data = join(dirname(__file__), 'data', 'txt2')
    data_expected = pd.read_csv(join(path_data, spc_filename + '.txt'),
                                sep='\t', header=None, skip_blank_lines=False)
    if (spc_file_format == 'gx-y' or
            spc_file_format == 'x-y'):
        X = data_expected.iloc[:, 0].values.T
        Y = data_expected.iloc[:, 1:].values.T
    elif spc_file_format == '-xy':
        data_expected['group_no'] = data_expected.isnull().all(axis=1).cumsum()
        # split into a list of DataFrames
        data_expected = [
            (data_expected.loc[data_expected['group_no'] == i,
                               [0, 1]]).dropna()
            for i in range(data_expected['group_no'].iloc[-1])]
        X, Y = [], []
        for df in data_expected:
            X.append(df.iloc[:, 0].values.T)
            Y.append(df.iloc[:, 1].values.T)
        X = np.array(X)
        Y = np.array(Y)

    return X, Y


def test_spc():
    filenames_spc = _list_all_spc_files()

    for filename in filenames_spc:
        path_data = join(dirname(__file__), 'data')
        file_spc = spc.File(join(path_data, filename))
        X, Y = _split_data(file_spc)
        X_expected, Y_expected = _read_expected_file(filename,
                                                     file_spc.dat_fmt)
        if file_spc.dat_fmt == '-xy':
            for x, y, x_expected, y_expected in zip(X, Y,
                                                    X_expected,
                                                    Y_expected):
                assert_allclose(x, x_expected)
                assert_allclose(y, y_expected)
        else:
            assert_allclose(X, X_expected)
            assert_allclose(Y, Y_expected)
