import pandas as pd
import json

from utils.calculate_features import CalculateFeatures


class CreateFeatureDF:
    """
    Class to create a new dataframe containing calculated features
    based on the contract data from the input dataframe.

    Attributes:
        df: original dataframe containing contract data and application dates.
        total_claims: assigning default value to tot_claim_cnt_l180d feature, will get overwritten if necessary.
        loan_sum: assigning default value to disb_bank_loan_wo_tbc feature, will get overwritten if necessary.
        loan_interval: assigning default value to day_sinlastloan feature, will get overwritten if necessary.
    """

    def __init__(self, df):
        self.df = df
        self.total_claims = -3
        self.loan_sum = -3
        self.loan_interval = -3

    @staticmethod
    def _parse_contracts(contracts: str) -> list[dict]:
        """
        Parses a json like string containing user contract data
        and turns it into a list of dictionaries.

        Parameters:
            * contracts: user contract data.

        Returns:
            * parsed contract data.
        """

        try:
            result = json.loads(contracts.replace("'", '"'))
            return [result] if isinstance(result, dict) else result
        except AttributeError:
            return []

    def calculate_features(self) -> pd.DataFrame:
        """
        Calculates features for every user's contract data
        and creates a dataframe containing calculated features.

        Returns:
            * final dataframe containing calculated features.
        """

        pd.set_option('future.no_silent_downcasting', True)
        features_list = []

        for _, row in self.df.iterrows():
            contract_data = self._parse_contracts(row['contracts'])
            contract_df = pd.DataFrame(contract_data)

            if not contract_df.empty:
                feature_calculator = CalculateFeatures(contract_df, row['application_date'])
                self.total_claims, self.loan_sum, self.loan_interval = feature_calculator.get_features()

            features_list.append({
                'id': row['id'],
                'tot_claim_cnt_l180d': self.total_claims,
                'disb_bank_loan_wo_tbc': self.loan_sum,
                'day_sinlastloan': self.loan_interval
            })

        features_df = pd.DataFrame(features_list)
        return features_df
