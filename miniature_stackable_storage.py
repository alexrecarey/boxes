from boxes import *
from boxes.edges import Bolts


class DisplayCutoutEdge(edges.BaseEdge):
    """An edge with room to fit a display panel"""
    def __call__(self, length, **kw):
        arc_height = self.settings.h * 4 / 5
        t = self.settings.thickness
        r = min(arc_height-t, length/4)
        self.edge(length/10-t, tabs=2)
        self.corner(90, t)
        self.edge(arc_height-2*t, tabs=2)
        self.corner(-90, t)
        self.edge(8*(length/10) - 2*t)
        self.corner(-90, t)
        self.edge(arc_height-2*t, tabs=2)
        self.corner(90, t)
        self.edge(length/10-t, tabs=2)


class StackingNotch(edges.BaseEdge):
    """A stackable notch, 2x thickness high"""
    char = 'n'
    def __call__(self, length, **kw):
        t = self.settings.thickness
        if length < t*4:
            self.edge(length)
        else:
            self.corner(-90, t)
            self.corner(90, t)
            self.edge(length - 4*t)
            self.corner(90, t)
            self.corner(-90, t)

    def margin(self):
        return self.settings.thickness * 2


class StackingNotchBase(edges.BaseEdge):
    """The base where a StackingNotch fits. Default 2x thickness high"""
    char = 'N'
    def __call__(self, length, **kw):
        t = self.settings.thickness
        if length < t * 4:
            self.edge(length)
        else:
            self.corner(90, t)
            self.corner(-90, t)
            self.edge(length - 4 * t)
            self.corner(-90, t)
            self.corner(90, t)

    def startwidth(self):
        return self.settings.thickness * 2


class MiniatureStackableStorageBox(Boxes):
    """Modular stackable storage containers for miniatures.

    The edges are described (bottom, right, top, left).

    Edges:
      h - Holes for finger joins.
      f - Finger joins
      F - finger joins opposite side
      e - Straight edge
      E - Straight Edge (outset by thickness)
      s - Stackable edge bottom
      S - stackable edge top
    """

    description = "This box is kept simple on purpose. If you need more features have a look at the UniversalBox."

    ui_group = "Box"

    def __init__(self):
        Boxes.__init__(self)
        self.addSettingsArgs(edges.FingerJointSettings)
        self.buildArgParser(x=210, y=297, h=70)

    def render(self):
        x, y, h, t = self.x, self.y, self.h, self.thickness

        # Prerequisites to create custom edge to create the stackable flanges
        stackable_edge_length = 30
        quarter_distance = y / 4
        long_side_section_lengths = (
            quarter_distance - stackable_edge_length / 2,
            stackable_edge_length,
            (quarter_distance - stackable_edge_length / 2) * 2,
            stackable_edge_length,
            quarter_distance - stackable_edge_length / 2
        )
        n = StackingNotch(self, self)
        N = StackingNotchBase(self, self)

        # Base of box edge. This edge alternates straight and finger, used for the base of the box
        straight_compound_edge = edges.CompoundEdge(
            self, "fefef", long_side_section_lengths)

        # Lower edge of side wall.
        # This edge is used for the bottom of the walls. Alternates holes with upwards cuts to fit a box below
        stackable_compound_edge_bottom = edges.CompoundEdge(
            self, ["h", N, "h", N, "h"], long_side_section_lengths)

        # Higher edge of side wall.
        # This edge is used for the top of the side wall, with upwards flanges to fit into a box on top
        stackable_compound_edge_top = edges.CompoundEdge(
            self, ["e", n, "e", n, "e"], long_side_section_lengths)

        # Edges necessary for the lid
        # These alternate between straight and outset straight to get around the notches in the box
        lid_notch_edge = edges.CompoundEdge(
            self, ['E', 'e', 'E', 'e', 'E'], long_side_section_lengths)

        # This custom edge has a huge cutout to see inside the box
        display_edge = DisplayCutoutEdge(self, self)

        # Some edges need double length finger joints to pierce the plexiglass and front panel of wood
        fjs = edges.FingerJointSettings(t, extra_length=1)
        double_long_fingerjoint = edges.FingerJointEdge(self, fjs)

        # Sizing guidelines. I think 4 of these boxes fit in an 1200x600 piece of 3mm board (without lid!)
        #with self.saved_context():
        #    self.rectangularWall(300, 600)

        # --- Main box structure ---
        # Base of box.
        self.rectangularWall(
            x, y, [double_long_fingerjoint, straight_compound_edge, 'f', straight_compound_edge],
            move="rotated up", label="Base")

        # Side panels
        self.rectangularWall(
            y, h, [stackable_compound_edge_bottom, double_long_fingerjoint, stackable_compound_edge_top, 'f'],
            move='up', label="Left side")
        self.rectangularWall(
            y, h, [stackable_compound_edge_bottom, 'f', stackable_compound_edge_top, double_long_fingerjoint],
            move='up', label="Right Side")

        # Back panel
        self.rectangularWall(x, h, 'hFeF', move='up', label="Back Panel")

        # Front panel with display cutout.
        self.rectangularWall(x, h, ["h", "F", display_edge, "F"], label="Display Panel front", move="up")

        # --- Lid ---
        self.rectangularWall(x, y, ["E", lid_notch_edge, "E", lid_notch_edge], label="Lid of box", move="up")

#
# class MiniatureStackableStorageBoxLid(Boxes):
#
#     def __init__(self):
#         Boxes.__init__(self)
#         self.addSettingsArgs(edges.FingerJointSettings)
#         self.buildArgParser(x=210, y=297, h=70)
#
#     def render(self):
#         x, y, h, t = self.x, self.y, self.h, self.thickness
#         stackable_edge_length = 30
#         quarter_distance = y / 4
#         long_side_section_lengths = (
#             quarter_distance - stackable_edge_length / 2,
#             stackable_edge_length,
#             (quarter_distance - stackable_edge_length / 2) * 2,
#             stackable_edge_length,
#             quarter_distance - stackable_edge_length / 2
#         )
#         lid_notch_edge = edges.CompoundEdge(
#             self, ['E', 'e', 'E', 'e', 'E'], long_side_section_lengths)
#         self.rectangularWall(x, y, ["E", lid_notch_edge, "E", lid_notch_edge], label="Lid of box", move="up")


if __name__ == '__main__':
    box = MiniatureStackableStorageBox()
    box.parseArgs(sys.argv[1:])
    box.open()
    box.render()
    box.close()
