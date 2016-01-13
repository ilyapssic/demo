import os
import sys

import pandas as pd
from pandas.util.testing import assert_almost_equal

import argparse


def _check_files_match(csv_file, offset, time_col, rec_time_col, tmp_file, part_ratio=0.1, part_limits=(10, 1000)):
    # check its OK
    org_df = pd.read_csv(csv_file)
    new_df = pd.read_csv(tmp_file)

    print('checking columns:')

    try:
        [(print(col), assert_almost_equal(org_df[col], new_df[col], obj=col, lobj='original', robj='new'))
            for col in new_df.columns if col not in [time_col, rec_time_col]]
    except AssertionError:
        print(sys.exc_value)
        return False
    else:
        return True


def time_offset(csv_file, offset, time_col='time', rec_time_col='rtime', out_file=None):
    df = pd.read_csv(csv_file)
    df[rec_time_col] = df[time_col]
    df[time_col] += offset

    # write to a temporary file
    pfx, fname = os.path.split(csv_file)
    tmp_file = os.path.join(pfx, '_temp_offset_' + fname)
    df.to_csv(tmp_file, index=False)

    if _check_files_match(csv_file, offset, time_col, rec_time_col, tmp_file):
        if out_file is None:
            os.remove(csv_file)
            os.rename(tmp_file, csv_file)
        else:
            os.rename(tmp_file, out_file)
    else:
        os.remove(tmp_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_file')
    parser.add_argument('offset', type=float)
    parser.add_argument('time_col', default='time', nargs='?',
                        help="name of the 'time' column the offset to be applied to")
    parser.add_argument('rec_time_col', default='rtime', nargs='?',
                        help="name of the column to keep original time. If None - don't keep")
    parser.add_argument('out_file', default=None, nargs='?',
                        help="if specified a new file with this name is created as output")

    args = parser.parse_args()

    print(args)
    # time_offset(r'data/collection1.csv', 0)


