import sys, os
def validate_content():
    body = os.environ.get("GIT_SENDEMAIL_BODY", "")
    if not body or len(body.strip()) < 10:
        print("ERROR: Email body is too short or empty.")
        sys.exit(1)
    print("Validation successful.")

if __name__ == "__main__":
    validate_content()
