import pandas
import pandas as pd


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
        Calculate features based on user contract data and
        ensures datetime columns are properly formatted for feature calculation.

        Returns:
            * total_claims, loan_sum, loan_interval: calculated values of features.
        """

        self.contract_df['claim_date'] = pd.to_datetime(self.contract_df['claim_date'], format='mixed')
        self.contract_df['contract_date'] = pd.to_datetime(self.contract_df['contract_date'], format='mixed')

        total_claims = self._calculate_total_claims()
        loan_sum = self._calculate_loan_sum()
        loan_interval = self._calculate_loan_interval()

        return total_claims, loan_sum, loan_interval


    def _calculate_total_claims(self) -> int:
        """
        Calculates the total number of claims within the last 180 days.

        Returns:
            * total_claims: total number of claims within the last 180 days.
        """

        target_date = pd.Timestamp.now() - pd.DateOffset(days=180)

        claims_df = self.contract_df[
            (self.contract_df['claim_id'].notna()) &
            (self.contract_df['claim_date'].notna()) &
            (self.contract_df['claim_date'] >= target_date)
        ]

        return claims_df.shape[0] if not claims_df.empty else self.default_claim

    def _calculate_loan_sum(self) -> int:
        """
        Calculates the total sum of loans excluding tbc bank loans.

        Returns:
            * loan_sum: sum of loans excluding tbc bank loans.
        """

        target_values = ['LIZ', 'LOM', 'MKO', 'SUG', pandas.NA]

        loans_df = self.contract_df[
            (self.contract_df['contract_date'].notna()) &
            (self.contract_df['loan_summa'].notna())
        ]

        if not loans_df.empty:
            if 'bank' in loans_df.columns:
                loans_df = loans_df[loans_df['bank'].isin(target_values) == False]

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

        loans_df = self.contract_df[
            (self.contract_df['contract_date'].notna()) &
            (self.contract_df['summa'].notna())
        ]

        if not loans_df.empty:
            max_loan_date = loans_df['contract_date'].max()

            return (self.application_date - max_loan_date).days
        return self.default_loan
