import sys

sys.path.append("../../")

import argparse
import pandas as pd
import numpy as np
from misc.logger import CustomLogger

from prov_acquisition.prov_libraries.tracker_old import ProvenanceTracker



def get_args() -> argparse.Namespace:
    """
    Parses command line arguments.
    """
    parser = argparse.ArgumentParser(description="Real worlds pipelines - Titanic Pipeline")
    parser.add_argument("--dataset", type=str, default="../../demos/real_world_pipelines/datasets/titanic.csv",
                        help="Relative path to the dataset file")
    parser.add_argument("--frac", type=float, default=0.0, help="Sampling fraction")

    return parser.parse_args()


def run_pipeline(args) -> None:
    
    logger = CustomLogger('ProvenanceTracker')

    input_path = args.dataset

    df = pd.read_csv(input_path, header=0)

    if args.frac != 0.0:
        df = df.sample(frac=args.frac)
        logger.info(f'The dataframe was sampled ({args.frac * 100}%)')

    # Create provenance tracker
    tracker = ProvenanceTracker()

    # Subscribe dataframe
    df = tracker.subscribe(df)


    logger.info(f' OPERATION 0 - Drop Name, Ticket, Cabin column')
    cols = ['Name', 'Ticket', 'Cabin']
    df = df.drop(cols, axis = 1)
    
    

    logger.info(f' OPERATION 1 - drop all rows in the data that have missing values (NaNs)')

    df = df.dropna()
    
    

    logger.info(f' OPERATION 2 - categorical encoding')
    cols = ['Pclass', 'Sex', 'Embarked']
    tracker.dataframe_tracking = False #to have the missing link for now
    for i,col in enumerate(cols):
            
        dummies = pd.get_dummies(df[col])
        df_dummies = dummies.add_prefix(col + '_')
        df = df.join(df_dummies)
        # Check last iteration:
        if i == len(cols) - 1:
            tracker.dataframe_tracking = True
        
        df = df.drop([col], axis=1)


    

if __name__ == '__main__':
    run_pipeline(get_args())
