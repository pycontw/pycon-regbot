import os
from datetime import datetime
from dotenv import load_dotenv
from google.cloud import bigquery
import requests
load_dotenv()

# Defined in .env file
USED_FILE = os.getenv("USED_FILE_PATH")
BIQUERY_CLIENT = bigquery.Client(project=os.getenv("BIGQUERY_PROJECT"))

def import_all_token():
    token_dict = dict()
    token_dict = _import_qrcode_from_bigquery(token_dict, table_name='dwd.kktix_ticket_corporate_attendees')
    token_dict = _import_qrcode_from_bigquery(token_dict, table_name='dwd.kktix_ticket_individual_attendees')
    token_dict = _import_qrcode_from_bigquery(token_dict, table_name='dwd.kktix_ticket_reserved_attendees')
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

def _import_qrcode_from_bigquery(token_dict: dict, table_name: str) -> dict:
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
        if len(qrcode) != 32:
            requests.post(
                os.getenv("DISCORD_WEBHOOK"),
                json={
                    "username": "大會當天的 kktix 註冊機器人",
                    "content": f"Invalid qrcode: {qrcode}! It's length should be 32",
                },
            )
            continue
        token_dict[qrcode] = ticket_name
    return token_dict