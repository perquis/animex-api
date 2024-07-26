def clean_string(s):
    # Remove leading/trailing whitespace and extra spaces between words
    return ' '.join(s.split())

# Function to convert comma-separated strings into lists
def split_comma_separated(s):
    return [clean_string(part) for part in s.split(',')]

# Process the dictionary
def process_data(d):
    for key, value in d.items():
        if isinstance(value, dict):
            process_data(value)
        elif isinstance(value, str):
            # Clean string
            cleaned_value = clean_string(value)
            # Convert comma-separated strings to lists
            if ',' in cleaned_value:
                d[key] = split_comma_separated(cleaned_value)
            else:
                d[key] = cleaned_value