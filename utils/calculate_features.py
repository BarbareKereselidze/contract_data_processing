import pandas as pd
import numpy as np


class CalculateFeatures:
    """
    Class to calculate user's features based on a dataframe contract data.

    Attributes:
        contract_df: dataframe containing user's contract data.
        application_date: user's application date, used to calculate loan interval.
        default_claim: default value for when no claims are found.
        default_loan: default value for when no loans are found.
    """

    def __init__(self, contract_df: pd.DataFrame, application_date: pd.Timestamp) -> None:
        self.contract_df = contract_df
        self.application_date = self._normalize_datetime(application_date)
        self.default_claim = -3
        self.default_loan = -1

    def get_features(self) -> tuple[int, int, int]:
        """
        Prepares dataframe and calculates features based on user contract data.
        * Changes empty strings to pandas Nan, so that all values that are empty
          can be the same type.
        * Ensures datetime columns are properly formatted for feature calculation.

        Returns:
            * total_claims, loan_sum, loan_interval: calculated values of features.
        """
        self.contract_df.replace('', np.nan, inplace=True)

        self.contract_df['claim_date'] = pd.to_datetime(self.contract_df['claim_date'], format='mixed')
        self.contract_df['contract_date'] = pd.to_datetime(self.contract_df['contract_date'], format='mixed')

        total_claims = self._calculate_total_claims()
        loan_sum = self._calculate_loan_sum()
        loan_interval = self._calculate_loan_interval()

        return total_claims, loan_sum, loan_interval

    def _get_valid_claims(self) -> pd.DataFrame:
        """
        Creates a new dataframe with contracts that include valid claims:
            * "claim_id" is not Nan
            * "claim_date" is not Nan

        Returns:
            * claim_df: valid claims dataframe.
        """

        claim_df = self.contract_df[
            (self.contract_df['claim_id'].notna()) &
            (self.contract_df['claim_date'].notna())
        ]
        return claim_df

    def _get_valid_loans(self) -> pd.DataFrame:
        """
        Creates a new dataframe with contracts that include valid loans:
            * "contract_date" is not Nan

        Returns:
            * loan_df: valid loans dataframe.
        """

        loan_df = self.contract_df[self.contract_df['contract_date'].notna()]
        return loan_df

    def _calculate_total_claims(self) -> int:
        """
        Calculates the total number of claims within the last 180 days,
        based on unique "claim_id" count.

        Returns:
            * total_claims: total number of claims within the last 180 days.
        """

        target_date = pd.Timestamp.now() - pd.DateOffset(days=180)

        claim_df = self._get_valid_claims()
        claim_df = claim_df[claim_df['claim_date'] >= target_date]

        return claim_df['claim_id'].nunique() if not claim_df.empty else self.default_claim

    def _calculate_loan_sum(self) -> int:
        """
        Calculates the total sum of loans excluding tbc bank loans.

        Returns:
            * loan_sum: sum of loans excluding tbc bank loans.
        """

        # if claims are valid, for this feature uncomment the following section:

        # if self._get_valid_claims().empty:
        #     return self.default_claim

        target_values = ['LIZ', 'LOM', 'MKO', 'SUG', pd.NA]

        loan_df = self._get_valid_loans()
        loan_df = loan_df[loan_df['loan_summa'].notna()]

        if not loan_df.empty:
            if 'bank' in loan_df.columns:
                loans_df = loan_df[loan_df['bank'].isin(target_values) == False]

                return loans_df['loan_summa'].sum()
        return self.default_loan

    @staticmethod
    def _normalize_datetime(date_value: pd.Timestamp) -> pd.Timestamp:
        """
        Normalizes a datetime object to remove
        time components and timezone information.

        Parameters:
            * date_value: datetime object to normalize.

        Returns:
            * date_value: normalized datetime object.
        """
        return date_value.normalize().tz_localize(None)

    def _calculate_loan_interval(self) -> int:
        """
        Calculates the number of days since the most recent loan contract.

        Returns:
            * loan_interval: user loan interval in days.
        """

        # if claims are valid, for this feature uncomment the following section:

        # if self._get_valid_claims().empty:
        #     return self.default_claim

        loan_df = self._get_valid_loans()
        loan_df = loan_df[(loan_df['summa'].notna()) &
                           # used to not get negative value of days
                           (loan_df['contract_date'] <= self.application_date)]

        if not loan_df.empty:
            max_loan_date = loan_df['contract_date'].max()

            return (self.application_date - max_loan_date).days
        return self.default_loan
