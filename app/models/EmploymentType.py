from enum import Enum

class EmploymentType(str, Enum):
    FULL_TIME_8_HOURS = "FullTime8Hours"
    PART_TIME_4_HOURS = "PartTime4Hours"
    PART_TIME_6_HOURS = "PartTime6Hours"
    DAILY_WORKER = "DailyWorker"
