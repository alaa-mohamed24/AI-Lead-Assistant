from src.ai_lead_assistant.models import Lead

def get_enum_value(val) -> str:
    """استخراج القيمة بنص صغير أياً كان نوعها (Enum أو Str) لتجنب الأخطاء"""
    if val is None:
        return "unknown"
    if hasattr(val, "value"):
        return str(val.value).lower()
    return str(val).lower()

def is_lead_complete(lead: Lead) -> bool:
    if not lead.name:
        return False
    if not lead.phone:
        return False
    if get_enum_value(lead.property_type) == "unknown":
        return False
    if not lead.location:
        return False
    if lead.budget is None:
        return False
    if not lead.intent:
        return False
    return True

def calculate_score(lead: Lead) -> int:
    score = 0

    # 1. Property Type Score
    if get_enum_value(lead.property_type) != "unknown":
        score += 10

    # 2. Location Score 
    if lead.location:
        score += 10

    # 3. Budget Score
    if lead.budget is not None and lead.budget > 0:
        score += 20 

    # 4. Bedrooms
    if lead.bedrooms is not None:
        score += 5

    # 5. Finishing Score
    if get_enum_value(lead.finishing) != "unknown":
        score += 10

    # 6. Intent Score
    if lead.intent and str(lead.intent).lower() in ["buy", "rent"]:
        score += 10

    # 7. Phone Score
    if lead.phone:
        score += 10

    # 8. Timeline Score
    if lead.timeline:
        score += 25

    return score

def classify_lead(score: int) -> str:
    if score >= 80:
        return "Hot"
    elif score >= 50:
        return "Warm"
    else:
        return "Cold"

def analyze_lead(lead: Lead) -> dict:
    score = calculate_score(lead)
    classification = classify_lead(score)

    return {
        "score": score,
        "classification": classification
    }