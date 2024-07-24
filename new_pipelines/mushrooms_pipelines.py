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
    parser = argparse.ArgumentParser(description="Real worlds pipelines - Mushrooms Pipeline")
    parser.add_argument("--dataset", type=str, default="../../demos/real_world_pipelines/datasets/mushrooms.csv",
                        help="Relative path to the dataset file")
    parser.add_argument("--frac", type=float, default=0.0, help="Sampling fraction")

    return parser.parse_args()


def run_pipeline(args) -> None:
    
    logger = CustomLogger('ProvenanceTracker')

    input_path = args.dataset

    df = pd.read_csv(input_path, sep=';', index_col=False)

    if args.frac != 0.0:
        df = df.sample(frac=args.frac)
        logger.info(f'The dataframe was sampled ({args.frac * 100}%)')

    # Create provenance tracker
    tracker = ProvenanceTracker(save_on_neo4j=True)

    # Subscribe dataframe
    df = tracker.subscribe(df)


    logger.info(f' OPERATION M0 - Drop 13 columns')

    df = df.drop(["does-bruise-or-bleed", "gill-attachment", "gill-color", "stem-root", "stem-surface",
                "stem-color", "veil-type", "veil-color", "has-ring", "ring-type", "spore-print-color", "habitat",
                "gill-spacing"], axis=1)
    
    

    logger.info(f' OPERATION M1 - binary assignment for edible or poisonus')

    # Assign 1 if class is 'e', 0 otherwise
    df['class'] = df['class'].replace({'e': 1, 'p': 0})

    logger.info(f' OPERATION M2 - Remove missing values')

    df = df.dropna()

    logger.info(f' OPERATION M3 - Value Transformation')

    df = df.replace({'cap-color': {'n': 1, 'b': 2, 'g': 3,
                  'r': 3, 'p': 4, 'u' : 5, 'e' : 6, 'w': 7, 'y': 8,
                  'l' : 9, 'o': 10, 'k': 11},
                  'cap-shape': {'b': 1, 'c': 2, 'x': 3, 'f': 4, 's': 5, 'p': 6, 'o': 7},
                  'cap-surface': {'i': 1, 'g': 2,'y': 3,'s': 4,'h': 5,'l': 6,'k': 7,'t': 8,
                  'w': 9,'e': 10,}, 
                  'season': {'s': 1, 'u': 2, 'a': 3, 'w': 4 }})



if __name__ == '__main__':
    run_pipeline(get_args())
