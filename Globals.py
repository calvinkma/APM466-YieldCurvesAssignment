from calendar import month
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Globals:
    DATETIME_FORMAT_STR = "%m/%d/%Y"

    NEXT_CPN_DATE = datetime.strptime("3/1/2022", DATETIME_FORMAT_STR).date()
    CPN_INTERVAL = relativedelta(months=+6)
    CPN_UNIT = 0.01
    FACE_VALUE = 100.0
