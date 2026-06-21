#!/usr/bin/env python3
"""Standalone WCAG compliance score calculator.
Usage: python3 compliance_score.py <axe-json-file>
       echo '{"violations":[...]}' | python3 compliance_score.py -
"""
import json, sys

IMPACT_WEIGHTS = {"critical": 8, "serious": 4, "moderate": 2, "minor": 1}
WCAG_CRITERIA = {
    "1.1.1": "Non-text Content", "1.2.1": "Audio-only/Video-only",
    "1.2.2": "Captions (Prerecorded)", "1.2.3": "Audio Description",
    "1.2.4": "Captions (Live)", "1.2.5": "Audio Description (Prerecorded)",
    "1.3.1": "Info and Relationships", "1.3.2": "Meaningful Sequence",
    "1.3.3": "Sensory Characteristics", "1.3.4": "Orientation",
    "1.3.5": "Identify Input Purpose", "1.4.1": "Use of Color",
    "1.4.3": "Contrast (Minimum)", "1.4.4": "Resize Text",
    "1.4.5": "Images of Text", "1.4.10": "Reflow",
    "1.4.11": "Non-text Contrast", "1.4.12": "Text Spacing",
    "1.4.13": "Content on Hover or Focus",
    "2.1.1": "Keyboard", "2.1.2": "No Keyboard Trap",
    "2.1.4": "Character Key Shortcuts", "2.4.1": "Bypass Blocks",
    "2.4.2": "Page Titled", "2.4.3": "Focus Order",
    "2.4.4": "Link Purpose (In Context)", "2.4.5": "Multiple Ways",
    "2.4.6": "Headings and Labels", "2.4.7": "Focus Visible",
    "2.5.1": "Pointer Gestures", "2.5.2": "Pointer Cancellation",
    "2.5.3": "Label in Name", "2.5.4": "Motion Actuation",
    "3.1.1": "Language of Page", "3.1.2": "Language of Parts",
    "3.2.1": "On Focus", "3.2.2": "On Input",
    "3.2.3": "Consistent Navigation", "3.2.4": "Consistent Identification",
    "3.3.1": "Error Identification", "3.3.2": "Labels or Instructions",
    "3.3.3": "Error Suggestion", "3.3.4": "Error Prevention (Legal/Financial)",
    "4.1.1": "Parsing", "4.1.2": "Name, Role, Value",
    "4.1.3": "Status Messages",
}

def tag_to_criterion(tag):
    """Convert axe tag like 'wcag111' to '1.1.1', 'wcag244' to '2.4.4',
    'wcag21aa' to '2.1.1' (ignoring trailing 'aa'/'aaa')."""
    # Remove leading 'wcag'
    if not tag.startswith("wcag"):
        return tag
    rest = tag[4:]  # e.g., '111', '244', '21aa', '21aaa'
    # Remove trailing 'aa' or 'aaa' (level indicators)
    if rest.endswith("aaa"):
        rest = rest[:-3]
    elif rest.endswith("aa"):
        rest = rest[:-2]
    # Now rest should be digits only, e.g., '111', '244', '21'
    if len(rest) == 0:
        return tag
    # First digit = principle number
    principle = rest[0]
    # Second digit = sub-guide number
    sub_guide = rest[1] if len(rest) >= 2 else ''
    # Remaining digits = criterion number; if none, default to '1'
    criterion = rest[2:] if len(rest) >= 3 else ''
    if criterion == '':
        criterion = '1'
    return f"{principle}.{sub_guide}.{criterion}"

def calc_score(violations):
    total_penalty = sum(IMPACT_WEIGHTS.get(v.get("impact","minor"), 1) for v in violations)
    return max(0, min(100, 100 - total_penalty))

def get_criteria_status(violations):
    violated = {}
    for v in violations:
        for tag in v.get("tags", []):
            if tag.startswith("wcag") and "best" not in tag:
                criterion = tag_to_criterion(tag)
                violated.setdefault(criterion, {"count": 0, "worst": "minor"})
                violated[criterion]["count"] += 1
                impact = v.get("impact", "minor")
                if IMPACT_WEIGHTS.get(impact, 0) > IMPACT_WEIGHTS.get(violated[criterion]["worst"], 0):
                    violated[criterion]["worst"] = impact
    return violated

def risk_info(score):
    """Return (legal_risk, recommendation) tuple based on score."""
    if score < 30:
        return "CRITICAL", "Immediate remediation required"
    elif score < 60:
        return "HIGH", "Prompt remediation strongly recommended"
    elif score < 80:
        return "MODERATE", "Improvements recommended for full compliance"
    else:
        return "LOW", "Minor adjustments recommended"

def main():
    if len(sys.argv) < 2:
        print("Usage: compliance_score.py <axe-json-file>")
        sys.exit(1)

    if sys.argv[1] == "-":
        data = json.load(sys.stdin)
    else:
        with open(sys.argv[1]) as f:
            data = json.load(f)

    if isinstance(data, list) and data:
        data = data[0]

    violations = data.get("violations", [])
    score = calc_score(violations)
    criteria = get_criteria_status(violations)

    buckets = {"critical": 0, "serious": 0, "moderate": 0, "minor": 0}
    for v in violations:
        buckets[v.get("impact", "minor")] += 1

    legal_risk, recommendation = risk_info(score)

    output = {
        "url": data.get("url", "unknown"),
        "wcag_compliance_score": score,
        "total_violations": len(violations),
        "by_severity": buckets,
        "criteria_evaluated": len(WCAG_CRITERIA),
        "criteria_violated": len(criteria),
        "criteria_passing": len(WCAG_CRITERIA) - len(criteria),
        "pass_rate": f"{((len(WCAG_CRITERIA) - len(criteria)) / len(WCAG_CRITERIA) * 100):.1f}%",
        "violated_criteria": [
            {"criterion": k, "name": WCAG_CRITERIA.get(k, k),
             "violations": v["count"], "severity": v["worst"]}
            for k, v in sorted(criteria.items())
        ],
        "legal_risk": legal_risk,
        "recommendation": recommendation,
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
