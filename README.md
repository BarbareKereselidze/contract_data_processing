# Contract Data Processing

This is a python script that processes a csv file containing user_id, application date and contract data, 
calculates specific features for each user based on their contract history
and saves the results into a new csv file. <br>

The key features calculated include:

* tot_claim_cnt_l180d - Total claims in the last 180 days.
* disb_bank_loan_wo_tbc - Sum of user's loans excluding tbc bank loans
* day_sinlastloan - Interval of days between user's last loan and application date.

## Features:

### 1. tot_claim_cnt_l180d
Counts the number of valid claims made by the user in the last 180 days. <br>

__Conditions:__ <br>
* `claim_id` is not null or an empty string. 
* `claim_date` is not null or an empty string. 
* `claim_date` is within the last 180 days from today. 

__Default Value:__ -3

__Final Calculation:__ valid `claim_id` count for each user.

### 2. disb_bank_loan_wo_tbc
Sums up all valid loan amounts, excluding loans from tbc bank which are identified 
by values: 'LIZ', 'LOM', 'MKO', 'SUG'.

__Conditions:__ <br>
* `bank` is not in ['LIZ', 'LOM', 'MKO', 'SUG'] 
* `bank` is not null or an empty string.
* `contract_date` is not null or an empty string.
* `loan_summa` is not null or an empty string.

__Default Value:__ -1

__Final Calculation:__ valid` loan_summa` sum for each user.

### 3. day_sinlastloan
Calculates the number of days since the user's most recent loan.

__Conditions:__ <br>
* `contract_date` is not null or an empty string.
* `summa` is not null or an empty string.

__Default Value:__ -1

__Final Calculation:__ user's `application_date` - max ` loan_date`.


## How To Use:

* Make sure to install the required modules listed in requirements.txt:
```
   pip install -r requirements.txt
```
* Update the configuration details in .env if necessary, before executing the scripts.

## Example .env:

```
CSV_DIR=/datasets
CSV_PATH=/datasets/data.csv
OUTPUT_CSV_NAME=contract_features.csv
```
