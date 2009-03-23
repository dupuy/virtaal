#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2009 Zuza Software Foundation
#
# This file is part of Virtaal.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

import gobject
import logging
from translate.storage.placeables import general, StringElem

from virtaal.common import GObjectWrapper
from virtaal.views import placeablesguiinfo

from basecontroller import BaseController


class PlaceablesController(BaseController):
    """Basic controller for placeable-related logic."""

    __gtype_name__ = 'PlaceablesController'
    __gsignals__ = {
        'parsers-changed': (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, tuple()),
    }

    parsers = []
    """The list of parsers that should be used by the main placeables C{parse()}
    function.
    @see translate.storage.placeables.parse"""

    # INITIALIZERS #
    def __init__(self, main_controller):
        GObjectWrapper.__init__(self)

        self.main_controller = main_controller
        self.main_controller.placeables_controller = self
        self.parsers = list(general.parsers)


    # METHODS #
    def add_parsers(self, *newparsers):
        """Add the specified parsers to the list of placeables parser functions."""
        if [f for f in newparsers if not callable(f)]:
            raise TypeError('newparsers may only contain callable objects.')

        self.parsers.extend(newparsers)
        self.emit('parsers-changed')

    def get_gui_info(self, placeable):
        """Get an appropriate C{StringElemGUI} or sub-class instance based on
        the type of C{placeable}. The mapping between placeables classes and
        GUI info classes is defined in
        L{virtaal.views.placeablesguiinfo.element_gui_map}."""
        if not isinstance(placeable, StringElem):
            raise ValueError('placeable must be a StringElem.')
        for plac_type, info_type in placeablesguiinfo.element_gui_map:
            if isinstance(placeable, plac_type):
                return info_type
        return placeablesguiinfo.StringElemGUI

    def remove_parsers(self, *parsers):
        changed = False
        for p in parsers:
            if p in self.parsers:
                self.parsers.remove(p)
                changed = True
        if changed:
            self.emit('parsers-changed')
