#!/usr/bin/env python

from datetime import datetime, date
from typing import Generator, Optional, Tuple
import requests
import icalendar
import click

ICAL_URL = "https://calendar.google.com/calendar/ical/eclecticpro.co.uk%40gmail.com/private-28bc3fb5f8b1279ee374d602e8296876/basic.ics"


def fetch_calendar():
    resp = requests.get(ICAL_URL)
    resp.raise_for_status()
    return resp.text


def load_calendar(content: str) -> icalendar.Calendar:
    return icalendar.Calendar.from_ical(content)


def get_events(
    calendar: icalendar.Calendar,
    only_dt: Optional[datetime] = None,
    remove_all_day_events: bool = True,
) -> Generator[Tuple[datetime, str], None, None]:

    for component in calendar.walk():
        if component.name == "VEVENT":
            dt = component.get("dtstart").dt
            if remove_all_day_events and type(dt) is date:
                continue

            if only_dt and dt.date() != only_dt.date():
                continue

            yield dt, component.get("summary")  # type: ignore


@click.command()
@click.argument("on_date", type=click.DateTime())
def get_calendar(on_date):
    cal_text = fetch_calendar()
    calendar = load_calendar(cal_text)
    for dt, summary in sorted(get_events(calendar, on_date), key=lambda x: x[0]):
        if on_date:
            dt = dt.time()
        print(f"- ({dt.strftime('%H%M') }) {summary}")


if __name__ == "__main__":
    get_calendar()
