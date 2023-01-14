from datetime import date, datetime


class DateConverter:
    regex = r"[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}"
    date_format = "%Y-%m-%d"

    def to_python(self, value):
        return datetime.strptime(value, DateConverter.date_format).date()

    def to_url(self, value):
        if isinstance(value, datetime) or isinstance(value, date):
            return value.strftime(DateConverter.date_format)
        elif isinstance(value, str):
            return value
        else:
            raise ValueError(f"Can convert value of type {type(value)} to date.")
