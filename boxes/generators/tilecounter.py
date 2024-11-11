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


class tilecounter(Boxes):
    """A tile counter"""

    description = "Tile Counter"

    ui_group = "Box"

    def __init__(self) -> None:
        Boxes.__init__(self)
        self.addSettingsArgs(edges.FingerJointSettings)

        self.buildArgParser(x=255, y=52, h=30, outside=True, bottom_edge="e")
        self.argparser.add_argument(
            "--axel_dia",  action="store", type=int, default=2,
            help="Axel Diameter in mm")
        self.argparser.add_argument(
            "--tiles",  action="store", type=int, default=9,
            help="Number of tiles to create")
        self.argparser.add_argument(
            "--tile_gap",  action="store", type=int, default=0,
            help="Gap between tiles after acounting for spacers")
        self.argparser.add_argument(
            "--tile_spacers",  action="store", type=bool, default=True,
            help="True for spacers of one thickness between each tile")
        self.argparser.add_argument(
            "--front_h_percent",  action="store", type=float, default=.6,
            help="Front hight as a precentage of overall height")

    def axel(self):
        h, y = self.h, self.y
        axel_dia = self.axel_dia
        t = self.thickness

        self.hole((y / 2.0), 
            (h / 2.0), d=axel_dia )

    def curve(self):
        x = self.x
        h, y, front_h_percent = self.h, self.y, self.front_h_percent
        finger, space = self.edges["f"].settings.finger, self.edges["f"].settings.space
        h_offset = h * front_h_percent
        h_offset = max(h_offset, finger+space)
        y_offset = min(h_offset, y)
        t = self.thickness
        self.moveTo(h_offset,y)
        self.curveTo(h-h_offset, 0,  (h-h_offset)*0.9,y_offset*-0.1,  h-h_offset ,y_offset*-1 )
    
    def tile_number(self):
        x, y = self.x, self.y
        h, w = self.ctx.tile_h, self.ctx.tile_w
        font_size = min(h,w) * 0.95
        tile_num = self.ctx.tile_num
        self.text(str(tile_num), w/4.0, h/2.0, fontsize=font_size, align="middle center")
    
    def tile_slot(self):
        h, w = self.ctx.tile_h, self.ctx.tile_w
        axel_dia = self.axel_dia
        self.rectangularHole(0, h/4.0, w, axel_dia )

    def render(self):
        x, y, h, front_h_percent = self.x, self.y, self.h, self.front_h_percent
        tiles, tile_gap, tile_spacers = self.tiles, self.tile_gap, self.tile_spacers
        t = self.thickness

        t1, t2, t3, t4 = "eeee"
        b = self.edges.get(self.bottom_edge, self.edges["F"])
        sideedge = "F" # if self.vertical_edges == "finger joints" else "h"
        

        if self.outside:
            self.x = x = self.adjustSize(x, sideedge, sideedge)
            self.y = y = self.adjustSize(y)
            self.h = h = self.adjustSize(h, b, t1)
        gap = tile_gap + t if tile_spacers else tile_gap
        tile_width = ( x - (gap * tiles + 2 * gap) ) / tiles

        endplate_cb = [ self.axel, self.curve ]
        with self.saved_context():
            if self.bottom_edge != "e":
                self.rectangularWall(x, y, "ffff", label="3", move="up")
            self.rectangularWall(y, h, [b, "f", t2, "f"],
                             ignore_widths=[1, 6], callback=endplate_cb, label="4", move="up")
            self.rectangularWall(y, h, [b, "f", t4, "f"],
                             ignore_widths=[1, 6], callback=endplate_cb, label="5", move="up")
            self.rectangularWall(x, h*front_h_percent, [b, sideedge, t1, sideedge],
                                 ignore_widths=[1, 6], label="1", move="up")
            self.rectangularWall(x, h, [b, sideedge, t3, sideedge],
                                 ignore_widths=[1, 6], label="2", move="up")
        self.rectangularWall(x, h, [b, sideedge, t3, sideedge],
                             ignore_widths=[1, 6], label="3", move="right only")
        
        tile_front_cb = [ self.tile_number, self.tile_slot ]
        tile_back_cb = [ ] # ending position of roundedPlate doesn't seem consitant making slotting both fails
        with self.saved_context() as ctx:
            ctx.tile_h = h*1.6
            ctx.tile_w = tile_width
            line=1
            for tile in range(1,tiles + 1):
                ctx.tile_num = tile
                self.roundedPlate(ctx.tile_w, ctx.tile_h, 6, edge='e', extend_corners=False, 
                    callback=tile_front_cb, move="up")
                self.roundedPlate(ctx.tile_w, ctx.tile_h, 6, edge='e', extend_corners=False, 
                    callback=tile_back_cb, move="up")
                self.rectangularWall(ctx.tile_w, ctx.tile_h,  move="right down only")
                self.rectangularWall(ctx.tile_w, ctx.tile_h,  move="down only")
                #print(tile * tile_width,x-y)
                #if ( tile * 2 * tile_width >= (x - y)*line ):
                #    print("push")
                #    self.rectangularWall(ctx.tile_w, ctx.tile_h,  move="right only")
                #    line += 1
                #    #self.roundedPlate(ctx.tile_w, ctx.tile_h, 6, edge='e', extend_corners=False, 
                #    #    callback=None, move="up")



