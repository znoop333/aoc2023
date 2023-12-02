import sys
from antlr4 import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from VisitorInterp import VisitorInterp
from typing import List
import subprocess
import pathlib
import pandas as pd
from datetime import datetime
from pyproj import CRS
from pyproj import Transformer
import numpy as np


def build_dataframe(positions: List) -> pd.DataFrame:
    time_start = datetime.combine(positions[0].home_time, positions[0].time_start)
    times = [(datetime.combine(positions[0].home_time, r.time_start) - time_start).total_seconds() for r in positions if
             r]

    home = [(r.home_gps[0], r.home_gps[1], 0) for r in positions if r]
    home_time = [r.home_time for r in positions if r]
    airframe_gps = [r.airframe_gps for r in positions if r]

    iso = [r.iso for r in positions if r]
    shutter = [r.shutter for r in positions if r]
    exposure = [r.exposure for r in positions if r]
    f_num = [r.f_num for r in positions if r]

    airframe_pry = [r.airframe_pry for r in positions if r]
    camera_pry = [r.camera_pry for r in positions if r]

    df = pd.DataFrame(data={'times': times, 'home': home, 'home_time': home_time, 'airframe_gps': airframe_gps,
                            'iso': iso, 'shutter': shutter, 'exposure': exposure, 'f_num': f_num,
                            'airframe_pry': airframe_pry, 'camera_pry': camera_pry})
    return df


class CRSHelper:
    def __init__(self, home_lat, home_lon, takeoff_alt=100):
        self.gps_crs = CRS.from_epsg(4326)
        self.utm_crs = CRS(proj='utm', zone=17, ellps='WGS84')
        self.transformer = Transformer.from_crs(self.gps_crs, self.utm_crs)
        self.takeoff_alt = takeoff_alt
        self.home_utm = self.transformer.transform(home_lat, home_lon, takeoff_alt)

    def gps_to_local(self, df: pd.DataFrame):
        utm_coord = [self.transformer.transform(r[1].airframe_gps[0], r[1].airframe_gps[1], r[1].airframe_gps[2]) for r
                     in df.iterrows()]
        df['utm_coord'] = utm_coord
        local_coord = np.array(utm_coord) - np.array(self.home_utm)
        df['local_coord'] = [(lc[0], lc[1], lc[2]) for lc in local_coord]
        return df


def main(argv):
    if len(argv) > 1:
        inname = pathlib.Path(argv[1])
        outname = inname.with_suffix(".srt")
        if not outname.exists():
            print(f"Extracting subtitles from {inname} into {outname}")
            subprocess.check_call(
                [
                    "ffmpeg",
                    "-y",
                    "-i",
                    inname,
                    "-map", "0:m:language:und", "-map", "-0:v", "-map", "-0:a", outname
                ]
            )
        else:
            print(f"Reading subtitles from {outname}")
        input_stream = FileStream(outname, encoding='utf-8')
    else:
        input_stream = FileStream('input.txt', encoding='utf-8')
    lexer = ExprLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ExprParser(stream)
    tree = parser.start_()
    if parser.getNumberOfSyntaxErrors() > 0:
        print("syntax errors")
    else:
        vinterp = VisitorInterp()
        positions = vinterp.visit(tree)
        df = build_dataframe(positions)
        ref_pt = next(df.iterrows())[1]
        crs_helper = CRSHelper(ref_pt.home[0], ref_pt.home[1])
        crs_helper.gps_to_local(df)
        1


if __name__ == '__main__':
    main(sys.argv)
