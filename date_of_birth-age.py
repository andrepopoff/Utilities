from datetime import date

# Date of birth --> Age
bdate = date(1988, 3, 27)
today = date.today()
age = today.year - bdate.year
if today.month < bdate.month or today.month == bdate.month and today.day < bdate.day:
    age -= 1
print(age)
