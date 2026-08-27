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


def get_google_sheet():
    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    client = gspread.authorize(credentials)
    spreadsheet = client.open("AI lead assistant")
    return spreadsheet


def get_worksheet():
    spreadsheet = get_google_sheet()
    worksheet = spreadsheet.worksheet("sheet1")
    return worksheet


def setup_worksheet():
    """تنظيف الشيت بالكامل أو إنشاء الهيدرز لو الشيت فاضية"""
    worksheet = get_worksheet()
    first_row = worksheet.row_values(1)
    if not first_row:
        worksheet.insert_row(HEADERS, 1)
        return True
    return False


def clear_and_reset_sheet():
    """فانكشن لمسح كل البيانات في الشيت وإعادة كتابة الهيدرز فقط (زي مسح leads.db)"""
    worksheet = get_worksheet()
    worksheet.clear()
    worksheet.append_row(HEADERS)
    print("🧹 [Google Sheets] Cleared all data and reset headers.")


def save_or_update_lead_in_sheet(lead, score, classification, lead_id, created_at):
    """تأخذ البيانات وتتحقق: لو الـ ID موجود تعمل UPDATE، لو مش موجود تعمل INSERT"""
    worksheet = get_worksheet()
    
    # التأكد من وجود الهيدرز
    setup_worksheet()

    # تجهيز الصف الجديد
    prop_val = lead.property_type.value if hasattr(lead.property_type, 'value') else lead.property_type
    fin_val = lead.finishing.value if hasattr(lead.finishing, 'value') else lead.finishing

    row = [
        lead_id,
        lead.name,
        lead.phone,
        prop_val,
        lead.location,
        lead.budget,
        lead.bedrooms,
        fin_val,
        lead.timeline,
        lead.intent,
        score,
        classification,
        str(created_at)
    ]

    # البحث عن الـ ID في العمود الأول (Column 1)
    try:
        cell = worksheet.find(str(lead_id), in_column=1)
    except Exception:
        cell = None

    if cell:
        # لو الـ ID موجود: تحديث الصف (UPDATE)
        row_number = cell.row
        # تحديث النطاق الخاص بالصف A{row}:M{row}
        worksheet.update(f"A{row_number}:M{row_number}", [row])
        print(f"🔄 [Google Sheets] Updated Row {row_number} for Lead ID: {lead_id}")
    else:
        # لو الـ ID مش موجود: إضافة صف جديد (INSERT)
        worksheet.append_row(row)
        print(f"✅ [Google Sheets] Added new row for Lead ID: {lead_id}")

    return True


def save_lead_to_sheet(lead, score, classification, lead_id, created_at):
    """دالة للتوافق مع استدعاءات الكود القديمة"""
    return save_or_update_lead_in_sheet(lead, score, classification, lead_id, created_at)