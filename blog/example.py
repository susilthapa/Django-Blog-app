import os

email_user = os.environ.get('EMAIL_HOST_USER')

email_password = os.environ.get('EMAIL_HOST_PASS')

print(email_user)
print(email_password)
