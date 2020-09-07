import requests

headers = {}
headers['Authorization'] = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTk5MDQ1NTI0LCJqdGkiOiI2ZTJlMzUxN2EwNDc0ZmZhYTdjN2IyNDc4ZGZiYWQyNSIsInVzZXJfaWQiOjI1fQ.UHn6_Jl3PAXtG-wMTjIHYJDy1JesQ32oIcZYPSbCIBg'

r = requests.get('http://127.0.0.1:8000/api/posts/23/', headers=headers)

print(r.text)