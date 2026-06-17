from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import Union, Optional, Iterable, Set


class DateService:

    DEFAULT_FORMAT = "%Y-%m-%d"

    def __init__(
        self,
        holidays: Optional[Iterable[Union[str, datetime]]] = None,
        extra_workdays: Optional[Iterable[Union[str, datetime]]] = None,
        fmt: str = None,
    ):
        fmt = fmt or DateService.DEFAULT_FORMAT
        self.holidays: Set[str] = self._normalize(holidays, fmt) if holidays else set()
        self.extra_workdays: Set[str] = self._normalize(extra_workdays, fmt) if extra_workdays else set()
        self.default_fmt = fmt

    @staticmethod
    def _normalize(items: Iterable[Union[str, datetime]], fmt: str) -> Set[str]:
        result: Set[str] = set()
        for item in items:
            if isinstance(item, str):
                dt = datetime.strptime(item, fmt)
            else:
                dt = item
            result.add(dt.strftime(DateService.DEFAULT_FORMAT))
        return result

    def set_holidays(self, holidays: Iterable[Union[str, datetime]], fmt: str = None) -> None:
        fmt = fmt or self.default_fmt
        self.holidays = self._normalize(holidays, fmt)

    def set_extra_workdays(self, extra_workdays: Iterable[Union[str, datetime]], fmt: str = None) -> None:
        fmt = fmt or self.default_fmt
        self.extra_workdays = self._normalize(extra_workdays, fmt)

    def add_holiday(self, date: Union[str, datetime], fmt: str = None) -> None:
        fmt = fmt or self.default_fmt
        if isinstance(date, str):
            date = datetime.strptime(date, fmt)
        self.holidays.add(date.strftime(DateService.DEFAULT_FORMAT))

    def add_extra_workday(self, date: Union[str, datetime], fmt: str = None) -> None:
        fmt = fmt or self.default_fmt
        if isinstance(date, str):
            date = datetime.strptime(date, fmt)
        self.extra_workdays.add(date.strftime(DateService.DEFAULT_FORMAT))

    @staticmethod
    def parse(date_str: str, fmt: str = None) -> datetime:
        fmt = fmt or DateService.DEFAULT_FORMAT
        return datetime.strptime(date_str, fmt)

    def is_workday(self, date: Union[str, datetime], fmt: str = None) -> bool:
        fmt = fmt or self.default_fmt
        if isinstance(date, str):
            date = DateService.parse(date, fmt)
        key = date.strftime(DateService.DEFAULT_FORMAT)
        if key in self.holidays:
            return False
        if key in self.extra_workdays:
            return True
        return date.weekday() < 5

    def add_workdays(
        self,
        date: Union[str, datetime],
        days: int,
        fmt: str = None,
        include_start: bool = False,
    ) -> str:
        fmt = fmt or self.default_fmt
        if isinstance(date, str):
            date = DateService.parse(date, fmt)
        if days == 0:
            return date.strftime(DateService.DEFAULT_FORMAT)

        direction = 1 if days > 0 else -1
        remaining = abs(days)
        current = date

        if not include_start:
            current += timedelta(days=direction)

        while remaining > 0:
            if self.is_workday(current):
                remaining -= 1
                if remaining == 0:
                    break
            current += timedelta(days=direction)

        return current.strftime(DateService.DEFAULT_FORMAT)

    def subtract_workdays(
        self,
        date: Union[str, datetime],
        days: int,
        fmt: str = None,
        include_start: bool = False,
    ) -> str:
        return self.add_workdays(date, -days, fmt, include_start)

    def workdays_between(
        self,
        start: Union[str, datetime],
        end: Union[str, datetime],
        fmt: str = None,
        include_end: bool = True,
    ) -> int:
        fmt = fmt or self.default_fmt
        if isinstance(start, str):
            start = DateService.parse(start, fmt)
        if isinstance(end, str):
            end = DateService.parse(end, fmt)

        if end < start:
            start, end = end, start

        direction = 1
        if not include_end:
            end_limit = end
        else:
            end_limit = end + timedelta(days=1)

        count = 0
        current = start
        while current < end_limit:
            if self.is_workday(current):
                count += 1
            current += timedelta(days=direction)

        return count

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
        return (end - start).days

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


def _weekday_cn(w: int) -> str:
    return ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][w]


if __name__ == "__main__":
    holidays_2026 = [
        "2026-01-01", "2026-01-02", "2026-01-03",
        "2026-02-16", "2026-02-17", "2026-02-18", "2026-02-19", "2026-02-20",
        "2026-04-04", "2026-04-05", "2026-04-06",
        "2026-05-01", "2026-05-02", "2026-05-03", "2026-05-04", "2026-05-05",
        "2026-06-19", "2026-06-20", "2026-06-21",
        "2026-09-25", "2026-09-26", "2026-09-27",
        "2026-10-01", "2026-10-02", "2026-10-03", "2026-10-04", "2026-10-05", "2026-10-06", "2026-10-07",
    ]
    extra_workdays_2026 = [
        "2026-02-14", "2026-02-15",
        "2026-09-20",
        "2026-10-10",
    ]

    svc = DateService(holidays=holidays_2026, extra_workdays=extra_workdays_2026)

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

    print("\n===== 工作日判断 (含配置的法定假日与调休) =====")
    test_dates = ["2026-06-17", "2026-06-20", "2026-06-19", "2026-02-14", "2026-02-16"]
    for d in test_dates:
        dt = DateService.parse(d)
        mark = ""
        if d in holidays_2026:
            mark = " [法定假日]"
        elif d in extra_workdays_2026:
            mark = " [调休上班]"
        print(f"  {d} ({_weekday_cn(dt.weekday())}) -> 工作日? {svc.is_workday(d)}{mark}")

    print("\n===== 加减 N 个工作日 =====")
    r14 = svc.add_workdays("2026-06-17", 5)
    print(f"2026-06-17 ({_weekday_cn(DateService.parse('2026-06-17').weekday())}) + 5个工作日 = {r14} ({_weekday_cn(DateService.parse(r14).weekday())})")
    r15 = svc.add_workdays("2026-02-13", 3)
    print(f"2026-02-13 ({_weekday_cn(DateService.parse('2026-02-13').weekday())}) + 3个工作日 = {r15} (跨越春节假期 + 调休)")
    r16 = svc.subtract_workdays("2026-02-23", 3)
    print(f"2026-02-23 ({_weekday_cn(DateService.parse('2026-02-23').weekday())}) - 3个工作日 = {r16} (反向穿越春节假期)")
    r17 = svc.add_workdays("2026-09-24", 5)
    print(f"2026-09-24 ({_weekday_cn(DateService.parse('2026-09-24').weekday())}) + 5个工作日 = {r17} (跨越中秋假期 + 调休补班 2026-09-20)")

    print("\n===== 区间工作日统计 =====")
    r18 = svc.workdays_between("2026-06-15", "2026-06-21")
    print(f"2026-06-15 ~ 2026-06-21 (含端午节 6/19-6/21) 工作日: {r18} 天")
    r19 = svc.workdays_between("2026-02-09", "2026-02-22", include_end=True)
    print(f"2026-02-09 ~ 2026-02-22 (跨越春节黄金周 + 调休) 工作日: {r19} 天")
