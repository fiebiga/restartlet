#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  greenlet.py
#
#  Copyright 2015 Adam Fiebig <fiebig.adam@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

from gevent.greenlet import Greenlet

class RestartableGreenlet(Greenlet):
    """
    A simple extension of the greenlet class that keeps track of the the run target
    and targets args/kwargs, as the base Greenlet deletes these values at the end of 'run'
    We can then use these properties in the callback to start a new greenlet to replace the failed greenlet automatically,
    if we so desire.

    Additional parameters:
        - restart (bool):   (Default: True) This flag is designed to be used as a signifier to a linked exception callback
                                        as to whether or not the callback should spawn a new greenlet to replace the one that crashed.
                                        If true, the callback should try to spawn a new greenlet. If false, the greenlet function stays dead

    """

    def __init__(self, run=None, restart=True, *args, **kwargs):
        self.run_target = run
        self.run_target_args = args
        self.run_target_kwargs = kwargs
        self.restart = restart
        Greenlet.__init__(self, run, *args, **kwargs)