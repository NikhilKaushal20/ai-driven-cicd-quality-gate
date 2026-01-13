def classify_failure(log_text):
    # TEMP logic (replace with OpenAI later)
    if "AssertionError" in log_text:
        return "TEST_FAILURE"
    elif "Timeout" in log_text or "Connection refused" in log_text:
        return "ENVIRONMENT_ISSUE"
    else:
        return "APPLICATION_BUG"
