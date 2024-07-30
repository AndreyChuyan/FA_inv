import requests


# def get_all_arm():
#     url = "http://127.0.0.1:8000/arm"
#     response = requests.get(url)
#     return response.json()


# students = get_all_arm()
# for i in students:
#     print(i)

def get_arm_with_param_requests(department: int, description: str):
    url = "http://127.0.0.1:8000/arm/{department}"
    response = requests.get(url, params={"description": description})
    return response.json()


arms = get_arm_with_param_requests(1, description=None)
print(arms)