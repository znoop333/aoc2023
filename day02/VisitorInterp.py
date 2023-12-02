import sys
from antlr4 import *
from ExprParser import ExprParser
from ExprVisitor import ExprVisitor

from dataclasses import dataclass
from typing import List
import datetime
import time


@dataclass
class AutelSRT:
    index: int
    time_start: time.time
    time_end: time.time
    home_gps: List
    home_time: datetime.datetime
    airframe_gps: List
    iso: int
    shutter: int
    exposure: float
    f_num: float
    airframe_pry: List
    camera_pry: List


def parse_timestamp_ms(ctx: ExprParser.Time_stamp_msContext) -> datetime.time:
    return datetime.time(hour=int(ctx.hh.text), minute=int(ctx.mm.text), second=int(ctx.ss.text),
                         microsecond=1000 * int(ctx.ms.text))


def parse_gps(ctx: ExprParser.Lat_lonContext) -> List:
    lat = float(ctx.lat_gps.text)
    lon = float(ctx.lon_gps.text)
    if ctx.lat_dir.text == 'S':
        lat = -lat
    if ctx.lon_dir.text == 'W':
        lon = -lon

    return [lat, lon]


def parse_datetime(ctx: ExprParser.DatetimestampContext) -> datetime.datetime:
    return datetime.datetime(int(ctx.yyyy.text), int(ctx.mmmm.text), int(ctx.dddd.text), int(ctx.hh.text),
                             int(ctx.mm.text),
                             int(ctx.ss.text))


def parse_airframe_gps(ctx: ExprParser.AirframeContext) -> List:
    lat_lon = parse_gps(ctx.lat_lon())
    alt = float(ctx.alt_gps.text)
    lat_lon.append(alt)
    return lat_lon


def parse_pry(ctx: ExprParser.PryContext) -> List:
    return [float(ctx.pitch.text), float(ctx.roll.text), float(ctx.yaw.text)]


class VisitorInterp(ExprVisitor):

    def visitFrame(self, ctx: ExprParser.FrameContext) -> AutelSRT:
        print(f'visiting frame {ctx.id_.text} from {ctx.time_start.getText()} to {ctx.time_end.getText()}')
        return AutelSRT(index=int(ctx.id_.text), time_start=parse_timestamp_ms(ctx.time_start),
                        time_end=parse_timestamp_ms(ctx.time_end), home_gps=parse_gps(ctx.home().lat_lon()),
                        home_time=parse_datetime(ctx.home().datetimestamp()),
                        airframe_gps=parse_airframe_gps(ctx.airframe()), iso=int(ctx.camera().iso.text),
                        shutter=int(ctx.camera().shutter.text), exposure=float(ctx.camera().exposure.text),
                        f_num=float(ctx.camera().f_num.text), airframe_pry=parse_pry(ctx.orientation().frame_pry),
                        camera_pry=parse_pry(ctx.orientation().gimbal_pry))

    def visitStart_(self, ctx: ExprParser.Start_Context):
        positions = []
        for i in range(0, ctx.getChildCount(), 1):
            positions.append(self.visit(ctx.getChild(i)))
            print(positions[-1])
        return positions
