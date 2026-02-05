import re

def check_password_strength(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long.")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add at least one uppercase letter.")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add at least one lowercase letter.")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("Add at least one number.")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("Add at least one special character.")

    return score, feedback


password = input("Enter a password to check: ")
score, feedback = check_password_strength(password)

print("\nPassword Strength Result:")

if score <= 2:
    print("Very Weak Password")
elif score == 3:
    print("Weak Password")
elif score == 4:
    print("Strong Password")
else:
    print("Very Strong Password")

for message in feedback:
    print("-", message)
