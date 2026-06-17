from datetime import datetime, timedelta
from typing import Union


class DateService:

    DEFAULT_FORMAT = "%Y-%m-%d"

    @staticmethod
    def parse(date_str: str, fmt: str = None) -> datetime:
        fmt = fmt or DateService.DEFAULT_FORMAT
        return datetime.strptime(date_str, fmt)

    @staticmethod
    def add_days(date: Union[datetime, str], days: int, fmt: str = None) -> str:
        if isinstance(date, str):
            date = DateService.parse(date, fmt)
        result = date + timedelta(days=days)
        return result.strftime(DateService.DEFAULT_FORMAT)

    @staticmethod
    def subtract_days(date: Union[datetime, str], days: int, fmt: str = None) -> str:
        return DateService.add_days(date, -days, fmt)

    @staticmethod
    def days_between(start: Union[datetime, str], end: Union[datetime, str], fmt: str = None) -> int:
        fmt = fmt or DateService.DEFAULT_FORMAT
        if isinstance(start, str):
            start = DateService.parse(start, fmt)
        if isinstance(end, str):
            end = DateService.parse(end, fmt)
        return (end - start).days

    @staticmethod
    def format_date(date: Union[datetime, str], target_fmt: str = None, source_fmt: str = None) -> str:
        target_fmt = target_fmt or DateService.DEFAULT_FORMAT
        if isinstance(date, str):
            date = DateService.parse(date, source_fmt)
        return date.strftime(target_fmt)


if __name__ == "__main__":
    svc = DateService()

    r1 = svc.add_days("2026-06-17", 10)
    print(f"2026-06-17 + 10天 = {r1}")

    r2 = svc.subtract_days("2026-06-17", 5)
    print(f"2026-06-17 - 5天 = {r2}")

    r3 = svc.days_between("2026-01-01", "2026-06-17")
    print(f"2026-01-01 到 2026-06-17 间隔 {r3} 天")

    r4 = svc.format_date("2026-06-17", "%Y年%m月%d日")
    print(f"格式化: 2026-06-17 -> {r4}")

    r5 = svc.format_date("06/17/2026", "%Y年%m月%d日", source_fmt="%m/%d/%Y")
    print(f"格式化(自定义源): 06/17/2026 -> {r5}")
