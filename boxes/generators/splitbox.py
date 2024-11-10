# Copyright (C) 2013-2014 Florian Festi
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from boxes import *
from boxes.lids import LidSettings


class splitbox(Boxes):
    """A split box"""

    description = "Box and lid, with the intension of having an external hinge"

    ui_group = "Box"

    def __init__(self) -> None:
        Boxes.__init__(self)
        self.addSettingsArgs(edges.FingerJointSettings)

        self.buildArgParser("outside", "bottom_edge", x=265, y=200)
        self.argparser.add_argument(
            "--base_h",  action="store", type=int, default=40,
            help="Hight of the bottom section")
        self.argparser.add_argument(
            "--lid_h",  action="store", type=int, default=30,
            help="Hight of the lid section")
        self.argparser.add_argument(
            "--window_y_percent",  action="store", type=float, default=0.80,
            help="Vertical size of the window in percent of y ")
        self.argparser.add_argument(
            "--window_x_percent",  action="store", type=float, default=0.90,
            help="Horizontal size of the window in percent of x ")
        self.argparser.add_argument(
            "--window_y_offset",  action="store", type=float, default=0.5,
            help="Vertical offset in percent of y gap ")
        self.argparser.add_argument(
            "--window_x_offset",  action="store", type=float, default=0,
            help="Horizontal offset in percent of x gap ")

    def window(self):
        x, y = self.x, self.y
        t = self.thickness

        stack = self.edges['s'].settings
        h = y * self.window_y_percent
        w = x * self.window_x_percent
        x_offset = (x-w) / 2.0 * self.window_x_offset
        y_offset = (y-h) / 2.0 * self.window_y_offset
        print("window",x,y,h,w,x_offset,y_offset)
        self.rectangularHole((x / 2.0) + x_offset, 
            (y / 2.0)+y_offset, w, h )

    def render(self):
        x, y, base_h, lid_h = self.x, self.y, self.base_h, self.lid_h
        t = self.thickness

        t1, t2, t3, t4 = "eeee"
        b = self.edges.get(self.bottom_edge, self.edges["F"])
        sideedge = "F" # if self.vertical_edges == "finger joints" else "h"

        if self.outside:
            self.x = x = self.adjustSize(x, sideedge, sideedge)
            self.y = y = self.adjustSize(y)
            self.base_h = base_h = self.adjustSize(base_h, b, t1)
            self.lid_h = lid_h = self.adjustSize(lid_h, b, t1)

        # Base and Lid
        for i, h in enumerate([ base_h, lid_h ]):
            bottom_cb = [ self.window ] if i == 0 else []
            with self.saved_context():
                if self.bottom_edge != "e":
                    self.rectangularWall(x, y, "ffff", callback=bottom_cb, label="3", move="up")
                self.lid(x, y)
                self.rectangularWall(y, h, [b, "f", t2, "f"],
                                 ignore_widths=[1, 6], label="4", move="up")
                self.rectangularWall(y, h, [b, "f", t4, "f"],
                                 ignore_widths=[1, 6], label="5", move="up")
                self.rectangularWall(x, h, [b, sideedge, t1, sideedge],
                                     ignore_widths=[1, 6], label="1", move="up")
                self.rectangularWall(x, h, [b, sideedge, t3, sideedge],
                                     ignore_widths=[1, 6], label="2", move="up")
            self.rectangularWall(x, 0, [b, sideedge, t3, sideedge],
                                 ignore_widths=[1, 6], label="3", move="right only")


