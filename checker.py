import math
import re
import hashlib

# ===========================
# CONSTANTS
# ===========================

GUESSES_PER_SECOND = 1e10
YEAR_REGEX = r"(^|[^0-9])(19|20)\d{2}($|[^0-9])"
SEQUENTIAL_PATTERNS = ["1234", "abcd", "qwerty"]

LEET_MAP = {
    "4": "a", "@": "a",
    "3": "e",
    "1": "i",
    "0": "o",
    "$": "s",
    "5": "s",
    "7": "t"
}

# ===========================
# LOAD DICTIONARY
# ===========================

def load_common_passwords(filename="common_passwords.txt"):
    try:
        with open(filename, "r") as file:
            return set(line.strip().lower() for line in file)
    except FileNotFoundError:
        return set()

# ===========================
# HASH FUNCTION (Optional Feature)
# ===========================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ===========================
# ENTROPY CALCULATION
# ===========================

def calculate_entropy(password):
    charset = 0

    if re.search(r"[a-z]", password):
        charset += 26
    if re.search(r"[A-Z]", password):
        charset += 26
    if re.search(r"[0-9]", password):
        charset += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        charset += 32

    if charset == 0:
        return 0

    entropy = len(password) * math.log2(charset)
    return round(entropy, 2)

# ===========================
# MASK ATTACK SIMULATION
# ===========================

def mask_attack_estimate(digits_count):
    combinations = 10 ** digits_count
    seconds = combinations / GUESSES_PER_SECOND
    return seconds

# ===========================
# REALISTIC CRACK TIME
# ===========================

def realistic_crack_time(password, entropy, common_passwords):
    lower_pass = password.lower()

    # Phase 1: Exact match
    if lower_pass in common_passwords:
        return "Instant (Exact dictionary match)"

    # Phase 2: Word + 4 digits (Mask attack simulation)
    match = re.match(r"^([a-zA-Z]+)(\d{4})$", password)
    if match:
        base = match.group(1).lower()
        if base in common_passwords:
            seconds = mask_attack_estimate(4)
            return "Seconds (Dictionary + 4 digit mask attack)"

    # Phase 3: Digits + letters
    if re.match(r"^[0-9]+[a-zA-Z]+$", password):
        return "Minutes (Digits + word pattern)"

    # Phase 4: Digits + letters + digits
    if re.match(r"^[0-9]+[a-zA-Z]+[0-9]+$", password):
        return "Minutes (Number + word + number pattern)"

    # Phase 5: Letters + digits + letters
    if re.match(r"^[a-zA-Z]+[0-9]+[a-zA-Z]+$", password):
        return "Minutes (Word + number + word pattern)"

    # Phase 6: Year detection (isolated year only)
    if re.search(YEAR_REGEX, password):
        return "Minutes (Contains isolated year pattern)"

    # Phase 7: Dictionary substring
    for word in common_passwords:
        if len(word) >= 4 and word in lower_pass:
            return "Minutes (Contains dictionary substring)"

    # Phase 8: Leet normalization
    normalized = lower_pass
    for k, v in LEET_MAP.items():
        normalized = normalized.replace(k, v)

    for word in common_passwords:
        if word in normalized:
            return "Minutes (Leet-based dictionary match)"

    # Phase 9: Repeated characters
    if re.search(r"(.)\1{2,}", password):
        return "Minutes (Repeated character sequence)"

    # Phase 10: Sequential patterns
    for seq in SEQUENTIAL_PATTERNS:
        if seq in lower_pass:
            return "Minutes (Sequential pattern detected)"

    # Phase 11: Weak entropy
    if entropy < 50:
        return "Days (Low entropy - brute-force feasible)"

    # Phase 12: Brute-force fallback
    combinations = 2 ** entropy
    seconds = combinations / GUESSES_PER_SECOND
    years = seconds / (60 * 60 * 24 * 365)

    if years > 1e6:
        return "Effectively uncrackable (current tech)"
    elif years > 100:
        return "Centuries"
    elif years > 10:
        return "Decades"
    else:
        return f"{round(years, 2)} years"

# ===========================
# PASSWORD EVALUATION
# ===========================

def evaluate_password(password, common_passwords):
    entropy = calculate_entropy(password)
    crack_time = realistic_crack_time(password, entropy, common_passwords)

    score = min(int(entropy * 1.5), 100)

    if score > 70:
        strength = "Strong"
    elif score > 40:
        strength = "Moderate"
    else:
        strength = "Weak"

    suggestions = []

    if not re.search(r"[A-Z]", password):
        suggestions.append("Add uppercase letters.")
    if not re.search(r"[0-9]", password):
        suggestions.append("Add numbers.")
    if not re.search(r"[!@#$%^&*]", password):
        suggestions.append("Add special characters.")
    if len(password) < 12:
        suggestions.append("Increase password length.")

    return {
        "entropy": entropy,
        "score": score,
        "strength": strength,
        "crack_time": crack_time,
        "suggestions": suggestions
    }
