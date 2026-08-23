# responsible for google sheets 

import gspread
from google.oauth2.service_account import Credentials

SERVICE_ACCOUNT_FILE = "service_account.json"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


HEADERS = [
    "ID",
    "Name",
    "Phone",
    "Property Type",
    "Location",
    "Budget",
    "Bedrooms",
    "Finishing",
    "Timeline",
    "Intent",
    "Score",
    "Classification",
    "Created At"
]


def setup_worksheet():

    worksheet= get_worksheet()
    frist_row = worksheet.row_values(1)
    if not frist_row:
        worksheet.insert_row(HEADERS, 1)

        return True

def get_google_sheet():
    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes= SCOPES
    )

    client= gspread.authorize(credentials)

    spreadsheet = client.open("AI lead assistant")

    return spreadsheet


def get_worksheet():

    spreadsheet = get_google_sheet()
    worksheet = spreadsheet.worksheet("sheet1")

    return worksheet


def save_lead_to_sheet(lead, score, classification, lead_id, created_at):
    worksheet = get_worksheet()

    row= [
        lead_id,
        lead.name,
        lead.phone,
        lead.property_type.value,
        lead.location,
        lead.budget,
        lead.bedrooms,
        lead.finishing.value,
        lead.timeline,
        lead.intent,
        score,
        classification,
        created_at
    ]

    worksheet.append_row(row)

    return True