import firebase_admin
from firebase_admin import db
from firebase_admin import credentials

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {"databaseURL": ""})

ref = db.reference('Data')

data = {
    "000":
        {
            "name": "Erling Haaland",
            "Department": "Football",
            "starting_year": 2022,
            "total_days_attendance": 30,
            "standing": "A+",
            "year": 1,
            "last_attendance_time": "2023-5-6 00:54:34"
        },
    "001":
        {
            "name": "Mohamed Mamdouh",
            "Department": "AI",
            "starting_year": 2021,
            "total_days_attendance": 25,
            "standing": "B",
            "year": 2,
            "last_attendance_time": "2023-5-6 00:54:34"
        },
    "002":
        {
            "name": "Anas Samir",
            "Department": "Cyber Security",
            "starting_year": 2022,
            "total_days_attendance": 35,
            "standing": "B",
            "year": 1,
            "last_attendance_time": "2023-5-6 00:54:34"
        },
    "003":
        {
            "name": "Mahmoud Nabil",
            "Department": "Flutter",
            "starting_year": 2020,
            "total_days_attendance": 15,
            "standing": "A",
            "year": 3,
            "last_attendance_time": "2023-5-6 00:54:34"
        },
    "005":
        {
            "name": "Ahmed Abdelrahman",
            "Department": "Operation",
            "starting_year": 2019,
            "total_days_attendance": 10,
            "standing": "A",
            "year": 4,
            "last_attendance_time": "2023-5-6 00:54:34"
        }
}

for key, value in data.items():
    ref.child(key).set(value)