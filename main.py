import os
import pandas as pd
from dotenv import load_dotenv

from utils import logger
from utils import prepare_df_for_analysis
from utils import CreateFeatureDF


load_dotenv()

CSV_DIR = os.getenv('CSV_DIR')
CSV_PATH = os.getenv('CSV_PATH')
OUTPUT_CSV_NAME = os.getenv('OUTPUT_CSV_NAME')


def main() -> None:
    df = pd.read_csv(CSV_PATH)

    prepare_df_for_analysis(df)
    logger.info("dataframe is ready for analysis")

    feature_df_creator = CreateFeatureDF(df)
    feature_df = feature_df_creator.calculate_features()
    logger.info("all features calculated and written in a dataframe")

    if not os.path.exists(CSV_DIR):
        os.mkdir(CSV_DIR)
        logger.info("csv directory created")

    output_csv_path = os.path.join(CSV_DIR, OUTPUT_CSV_NAME)
    feature_df.to_csv(output_csv_path, index=False)
    logger.info(f"df successfully saved as a csv at {output_csv_path}")


if __name__ == '__main__':
    main()
