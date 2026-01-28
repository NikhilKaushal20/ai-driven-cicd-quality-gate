def classify_failure(log: str) -> dict:
    log_lower = log.lower()

    if "assert" in log_lower or "expected" in log_lower:
        return {
            "status": "UNSTABLE",
            "failure_type": "TEST_FAILURE",
            "recommendation": "Fix assertion or update expected value"
        }

    if "timeout" in log_lower or "chrome not reachable" in log_lower:
        return {
            "status": "FAILURE",
            "failure_type": "ENVIRONMENT_ISSUE",
            "recommendation": "Check environment or browser setup"
        }

    return {
        "status": "FAILURE",
        "failure_type": "APPLICATION_BUG",
        "recommendation": "Investigate application defect"
    }
