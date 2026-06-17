from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Union, Optional


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
        result = date + relativedelta(days=days)
        return result.strftime(DateService.DEFAULT_FORMAT)

    @staticmethod
    def subtract_days(date: Union[datetime, str], days: int, fmt: str = None) -> str:
        return DateService.add_days(date, -days, fmt)

    @staticmethod
    def add_months(date: Union[datetime, str], months: int, fmt: str = None) -> str:
        if isinstance(date, str):
            date = DateService.parse(date, fmt)
        result = date + relativedelta(months=months)
        return result.strftime(DateService.DEFAULT_FORMAT)

    @staticmethod
    def subtract_months(date: Union[datetime, str], months: int, fmt: str = None) -> str:
        return DateService.add_months(date, -months, fmt)

    @staticmethod
    def add_years(date: Union[datetime, str], years: int, fmt: str = None) -> str:
        if isinstance(date, str):
            date = DateService.parse(date, fmt)
        result = date + relativedelta(years=years)
        return result.strftime(DateService.DEFAULT_FORMAT)

    @staticmethod
    def subtract_years(date: Union[datetime, str], years: int, fmt: str = None) -> str:
        return DateService.add_years(date, -years, fmt)

    @staticmethod
    def add(
        date: Union[datetime, str],
        *,
        years: int = 0,
        months: int = 0,
        days: int = 0,
        weeks: int = 0,
        fmt: str = None,
    ) -> str:
        if isinstance(date, str):
            date = DateService.parse(date, fmt)
        result = date + relativedelta(years=years, months=months, days=days, weeks=weeks)
        return result.strftime(DateService.DEFAULT_FORMAT)

    @staticmethod
    def days_between(start: Union[datetime, str], end: Union[datetime, str], fmt: str = None) -> int:
        fmt = fmt or DateService.DEFAULT_FORMAT
        if isinstance(start, str):
            start = DateService.parse(start, fmt)
        if isinstance(end, str):
            end = DateService.parse(end, fmt)
        rd = relativedelta(end, start)
        total_days = (end - start).days
        return total_days

    @staticmethod
    def detail_between(
        start: Union[datetime, str],
        end: Union[datetime, str],
        fmt: str = None,
    ) -> dict:
        fmt = fmt or DateService.DEFAULT_FORMAT
        if isinstance(start, str):
            start = DateService.parse(start, fmt)
        if isinstance(end, str):
            end = DateService.parse(end, fmt)
        rd = relativedelta(end, start)
        total_days = (end - start).days
        return {
            "years": rd.years,
            "months": rd.months,
            "days": rd.days,
            "total_days": total_days,
        }

    @staticmethod
    def format_date(date: Union[datetime, str], target_fmt: str = None, source_fmt: str = None) -> str:
        target_fmt = target_fmt or DateService.DEFAULT_FORMAT
        if isinstance(date, str):
            date = DateService.parse(date, source_fmt)
        return date.strftime(target_fmt)


if __name__ == "__main__":
    svc = DateService()

    print("===== 基础加减天数 =====")
    r1 = svc.add_days("2026-06-17", 10)
    print(f"2026-06-17 + 10天 = {r1}")
    r2 = svc.subtract_days("2026-06-17", 5)
    print(f"2026-06-17 - 5天 = {r2}")

    print("\n===== 跨月/跨年加减月份 (timedelta 无法正确处理) =====")
    r3 = svc.add_months("2026-01-31", 1)
    print(f"2026-01-31 + 1月 = {r3}  (月末自动对齐到 2月28日)")
    r4 = svc.add_months("2024-01-31", 1)
    print(f"2024-01-31 + 1月 = {r4}  (闰年对齐到 2月29日)")
    r5 = svc.add_months("2026-12-31", 2)
    print(f"2026-12-31 + 2月 = {r5}  (跨年 + 月末对齐)")
    r6 = svc.subtract_months("2026-03-31", 1)
    print(f"2026-03-31 - 1月 = {r6}  (回退月末对齐)")

    print("\n===== 加减年份 (处理闰年 2月29日) =====")
    r7 = svc.add_years("2024-02-29", 1)
    print(f"2024-02-29 + 1年 = {r7}  (非闰年自动对齐到 2月28日)")
    r8 = svc.add_years("2024-02-29", 4)
    print(f"2024-02-29 + 4年 = {r8}  (到下一个闰年保持 2月29日)")

    print("\n===== 组合加减 (年+月+日) =====")
    r9 = svc.add("2026-01-15", years=1, months=2, days=5)
    print(f"2026-01-15 + 1年2月5天 = {r9}")

    print("\n===== 日期间隔 =====")
    r10 = svc.days_between("2026-01-01", "2026-06-17")
    print(f"2026-01-01 到 2026-06-17 间隔 {r10} 天")
    r11 = svc.detail_between("2024-02-29", "2026-06-17")
    print(f"2024-02-29 到 2026-06-17 详细间隔: {r11}")

    print("\n===== 日期格式化 =====")
    r12 = svc.format_date("2026-06-17", "%Y年%m月%d日")
    print(f"格式化: 2026-06-17 -> {r12}")
    r13 = svc.format_date("06/17/2026", "%Y年%m月%d日", source_fmt="%m/%d/%Y")
    print(f"格式化(自定义源): 06/17/2026 -> {r13}")
