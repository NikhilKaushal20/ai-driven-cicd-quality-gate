def extract_failure(log_path):
    with open(log_path, "r") as file:
        return file.read()
