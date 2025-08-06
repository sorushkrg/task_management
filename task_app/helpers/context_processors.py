import os
import jdatetime
from flask import request
from task_app.utils.hashid import encode_id, decode_id


def inject_globals():
    def to_jalali(value):
        if not value:
            return ""
        return jdatetime.datetime.fromgregorian(datetime=value).strftime('%Y/%m/%d')

    def status(value):
        match value:

            case 0:
                return "در حال انجام", "info"  # آبی روشن
            case "done":
                return "انجام شده", "success"  # سبز
            case "canceled":
                return "لغو شده", "danger"  # قرمز
            case _:
                return "نامشخص", "dark"

    return {
        "APP_NAME": os.getenv("APP_NAME", "برنامه من"),
        "current_year": jdatetime.date.today().year,
        "to_jalali": to_jalali,
        "status": status,
        "request" : request,
        "encode_id": encode_id,
        "decode_id": decode_id

    }
#
