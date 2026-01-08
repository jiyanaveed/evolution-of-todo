import requests

# Test the update endpoint with proper headers
url = "http://localhost:8000/tasks/16"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjZWMxYTkyYS00YWI2LTQyNDAtOTU2Yy1kMzRmYTY4YWExNTgiLCJlbWFpbCI6ImppeWEubmF2ZWVkNzBAZ21haWwuY29tIiwiZXhwIjoxNzY3NDQ2MDczfQ.TEvjz4HDFuR2BDRUuQa6PCPng4JTNkNzTWNLoCJhsTA",
    "Content-Type": "application/json"
}
data = {"title": "Updated task title"}

response = requests.put(url, json=data, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")