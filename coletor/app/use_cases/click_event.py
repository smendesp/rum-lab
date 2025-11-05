from multiprocessing import Process
import time

from app.services.time_series.click_event import ClickEvent


class ClickEventUseCase:
    def __init__(self):
        ...

    def set_events(self, events):
        click_event = ClickEvent()
        click_event.set_events(events)
