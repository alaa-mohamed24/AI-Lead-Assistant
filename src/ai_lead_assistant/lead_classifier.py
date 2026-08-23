# responsible for classification

from src.ai_lead_assistant.models import Lead

# calculate score

def is_lead_complelt(lead:Lead):
    if not lead.name:
        return False

    if not lead.phone:
        return False

    if not lead.property_type.value == "unknown":
        return False

    if not lead.location:
        return False

    if not lead.budget:
        return False

    if not lead.intent:
        return False

    return True

def calculate_score(lead: Lead):

    score= 0

    # property type score

    if lead.property_type.value != "unknown":
        score += 10

    #location score 

    if lead.location:
        score +=10

    # budget score

    if lead.budget is not None :
        score += 20 

    # bedrooms

    if lead.bedrooms is not None :
        score += 5

    # finishing

    if lead.finishing.value != "unknown":
        score += 10

    # intent

    if lead.intent in ["buy", "rent"]:
        score += 10

    # phone

    if lead.phone:
        score += 10

    # timeline
    if lead.timeline:
        score += 25

    

    return score

def classify_lead(score: int):

    if score >= 80 :
        return "hot"

    elif score >= 50 :
        return "warm"

    else:
        return "cold"


def analyze_lead(lead: Lead):
    score= calculate_score(lead)
    classification = classify_lead(score)

    return {
        "score": score,
        "classification": classification
    }    