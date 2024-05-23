#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd
import os


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="data_clean")
    run.config.update(args)

    logger.info("Downloading artifact")
    artifact = run.use_artifact(args.input_artifact)
    artifact_path = artifact.file()
    df = pd.read_csv(artifact_path)

    # Drop outliers
    min_price = 10
    max_price = 350
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])
    print(df)
    filename = "clean_data.csv"
    df.to_csv(filename, index=False)

    logger.info("Creating artifact")
    artifact = wandb.Artifact(
        name=args.output_artifact_name,
        type=args.output_artifact_type,
        description=args.output_artifact_description,
    )
    artifact.add_file(filename)

    run.log_artifact(artifact)

    #os.remove(filename)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Cleaning of data")


    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Name of the input artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact_name",
        type=str,
        help="Name of the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact_type",
        type=str,
        help="Type of the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact_description",
        type=str,
        help="Description of the output artifact",
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help="Minimum number for price",
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help="Maximum number for price",
        required=True
    )


    args = parser.parse_args()

    go(args)