import os
from datetime import datetime
from dotenv import load_dotenv
from google.cloud import bigquery
load_dotenv()

# Defined in .env file
USED_FILE = os.getenv("USED_FILE_PATH")
BIQUERY_CLIENT = bigquery.Client(project=os.getenv("BIGQUERY_PROJECT"))

def import_all_token():
    token_dict = dict()

    # TODO(david): remove _copy table posfix, once Angus is ready
    token_dict = _import_qrcode_from_bigquery(token_dict, table_name='dwd.kktix_ticket_corporate_attendees_copy')
    token_dict = _import_qrcode_from_bigquery(token_dict, table_name='dwd.kktix_ticket_individual_attendees_copy')
    token_dict = _import_qrcode_from_bigquery(token_dict, table_name='dwd.kktix_ticket_reserved_attendees_copy')
    return token_dict

def read_used_list():
    try:
        with open(USED_FILE, 'r') as f:
            used_list = f.read().splitlines()
        return used_list
    except IOError as e:
        print(f"{USED_FILE} not exist, create one!")
        f = open(USED_FILE, 'w+')
        f.close()
        return list()

def _import_qrcode_from_bigquery(token_dict: dict, table_name: str) -> dict[str, str]:
    current_year = datetime.now().year
    query = f"""
        SELECT
          ticket_type,
          qrcode
        FROM
          `pycontw-225217.{table_name}`
        WHERE
          qrcode IS NOT NULL
          AND payment_status = 'paid'
          AND EXTRACT(YEAR
          FROM
            CAST(paid_date AS DATE)) = {current_year};
    """
    query_job = BIQUERY_CLIENT.query(query)
    for row in query_job:
        ticket_name = row["ticket_type"].lower().replace("\"", "")
        qrcode = row["qrcode"].replace("\"", "")
        assert len(qrcode) == 32, f"qrcode length should be 32, but got {len(qrcode)}"
        token_dict[qrcode] = ticket_name
    return token_dict