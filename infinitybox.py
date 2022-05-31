#!/usr/bin/env python3
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

import boxes
from boxes import *
from boxes.edges import Bolts
# from boxes.lids import _TopEdge, _ChestLid


class InfinityBox(Boxes):
    """A simple Box

    Edges:
      h - Holes for finger joins.
      f - Finger joins
      F - finger joins opposite side
      e - Straight edge
      E - ????
    """

    description = "This box is kept simple on purpose. If you need more features have a look at the UniversalBox."

    ui_group = "Box"

    def __init__(self):
        Boxes.__init__(self)
        self.addSettingsArgs(edges.FingerJointSettings)
        self.buildArgParser("x", "y", "h", "outside", "bottom_edge")
        self.argparser.add_argument(
            "--screwdiameter", action="store", type=float, default=3.,
            help="Diameter of the lid screw holes in mm for handle")
        self.argparser.add_argument(
            "--handlewidth", action="store", type=float, default=100,
            help="Width of handle between holes in mm")

    def render(self):
        x, y, h = self.x, self.y, self.h
        sh = self.screwdiameter
        hw = self.handlewidth
        t = self.thickness

        b1 = Bolts(1)

        # --- Main box structure ---
        # base of box.
        self.rectangularWall(x, y, 'efff', bedBolts=[None, b1, b1, b1], move="up", label="Base")

        # Side panels
        self.rectangularWall(y, h, 'hFfe', bedBolts=[b1, b1, b1, None], move='up', label="Right side")
        self.rectangularWall(y, h, 'hefF', bedBolts=[b1, None, b1, b1], move='up', label="Left side")

        # Back panel
        self.rectangularWall(x, h, 'hfff', bedBolts=[b1, b1, b1, b1], move='up', label="Back Panel")

        # Top panel with holes for handle
        self.rectangularWall(x, y, 'eFFF', callback=[
            lambda: self.hole(x/2-(self.handlewidth/2), y/2, d=self.screwdiameter),
        ] * 2, bedBolts=[None, b1, b1, b1], move='up', label="Top panel")

        # --- Inner supports for shelves ---

        # --- Lid ---




if __name__ == '__main__':
    box = InfinityBox()
    # box.x = 250
    # box.y = 150
    # box.z = 300
    # box.thickness = 10
    print(sys.argv)
    box.parseArgs(sys.argv[1:])
    box.open()
    box.render()
    box.close()
