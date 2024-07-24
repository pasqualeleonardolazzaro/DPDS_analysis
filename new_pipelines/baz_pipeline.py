import sys

sys.path.append("../../")

import argparse
import pandas as pd
import numpy as np
from misc.logger import CustomLogger

from prov_acquisition.prov_libraries.tracker import ProvenanceTracker

def get_args() -> argparse.Namespace:
    """
    Parses command line arguments.
    """
    parser = argparse.ArgumentParser(description="Real worlds pipelines - Baz Pipeline")
    parser.add_argument("--dataset", type=str, default="../../demos/real_world_pipelines/datasets/census.csv",
                        help="Relative path to the dataset file")
    parser.add_argument("--frac", type=float, default=0.0, help="Sampling fraction [0.0 - 1.0]")

    return parser.parse_args()


def one_hot_encode(data, columns):
    """
    Perform one-hot encoding on the specified columns of a DataFrame.

    Parameters:
    data (pandas.DataFrame): The DataFrame containing the categorical columns to encode.
    columns (list): A list of column names to encode.

    Returns:
    pandas.DataFrame: The DataFrame with one-hot encoded columns.
    """
    
    # Iterate over each column to encode
    for column in columns:
        # Perform one-hot encoding using pandas' get_dummies function
        one_hot_encoded = pd.get_dummies(data[column], prefix=column)
        
        # Drop the original column from the DataFrame
        data = data.drop(column, axis=1)
        
        # Concatenate the one-hot encoded columns to the DataFrame
        data = pd.concat([data, one_hot_encoded], axis=1)
    
    return data


def run_pipeline(args) -> None:
    
    logger = CustomLogger('ProvenanceTracker')

    input_path = args.dataset

    df = pd.read_csv(input_path)

    # Assign names to columns
    names = ['age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status', 'occupation', 'relationship',
             'race', 'sex', 'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'label']

    df.columns = names

    if args.frac > 0.0 and args.frac < 1.0:
        df = df.sample(frac=args.frac)
        logger.info(f'The dataframe was sampled ({args.frac * 100}%)')
    elif args.frac > 1.0:
        df = pd.concat([df] * int(args.frac), ignore_index=True)
        logger.info(f'The dataframe has been enlarged by ({int(args.frac)} times')

    # Create provenance tracker
    tracker = ProvenanceTracker(save_on_neo4j=True)

    # Subscribe dataframe
    df = tracker.subscribe(df)

    print(df)

    logger.info(" OPERATION C0 - one-hot encode of some columns")
    tracker.dataframe_tracking = False
    columns = ['workclass', 'native-country']
    for i, col in enumerate(columns):
        
        dummies = pd.get_dummies(df[col])
        df_dummies = dummies.add_prefix(col + '_')
        df = df.join(df_dummies)
        
        # Check last iteration:
        if i == len(columns) - 1:
            tracker.dataframe_tracking = True
        
        df = df.drop([col], axis=1)
    
    print(df)

    logger.info( " OPERATION C1 - Replace ? character for NaN value")
    df = df.replace('?', np.nan)
    print(df)

    logger.info( " OPERATION C2 - new columns")
    # Calcola alcune nuove features combinate
    df['capital-net'] = df['capital-gain'] - df['capital-loss']
    df['hours-per-week-to-age-ratio'] = df['hours-per-week'] / df['age']
    print(df)




if __name__ == '__main__':
    run_pipeline(get_args())
