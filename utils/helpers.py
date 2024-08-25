import pandas as pd

def prepare_df_for_analysis(df: pd.DataFrame) -> None:
    """
    Function prepares dataframe for analysis by:
        * Turning csv id column values from float to int type.
        * Checking that the "id" column values are not None and if so drops the None values.
        * Turning "application_date" column values from string to datetime type.

    Args:
        * df:Pandas dataframe containing data to be validated.
    """

    df['id'] = df['id'].astype(int)
    contains_none = df['id'].isna().any()

    if contains_none:
        df.drop(columns=['id'], inplace=True)

    df['application_date'] = pd.to_datetime(df['application_date'], format='mixed', utc=True)
