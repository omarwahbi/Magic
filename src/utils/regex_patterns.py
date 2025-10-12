"""Regular expression patterns used throughout the application."""

import re

# Pattern for national medicine codes (format: XX-XXX-XXX)
CODE_PATTERN = re.compile(r'([A-Z0-9]{2}-[A-Z0-9]{3}-+[A-Z0-9]{3})', re.IGNORECASE)

# Pattern for expiry dates (format: DD/MM/YYYY)
DATE_PATTERN = re.compile(r'(\d{1,2})/(\d{1,2})/(\d{4})')
