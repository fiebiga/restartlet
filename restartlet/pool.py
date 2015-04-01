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

from gevent.pool import Pool
from gevent import sleep
from restartlet import RestartableGreenlet

class RestartPool(Pool):
    """
    A simple extension of the gevent Pool class that, by default, adds a callback to all greenlet spawns that will
    restart the greenlet in the event of an exceptional exit

    Additional parameters:
        - restart       (bool):     (Default: True) This flag is designed to be used as a signifier to a linked exception callback
                                        as to whether or not the callback should spawn a new greenlet to replace the one that crashed.
                                        If true, the callback should try to spawn a new greenlet. If false, the greenlet function stays dead
        - sleep_interval (int):     (Default: 0) The amount of time to sleep between greenlet restarts. A value of 0 may not be appropriate, as it could bring
                                        an application or process to its knees
        - logger      (Logger):     (Default: None) This should be an instance of a logger that emulates the "warn, error, info" python log levels. If one is
                                        provided, the greenlet restart will be directed to that log file as well as STDOUT

    """

    def __init__(self, sleep_interval=0, restart=True, logger=None, *args, **kwargs):
        self.sleep_interval = sleep_interval
        self.restart = restart
        self.logger = logger
        super(RestartPool, self).__init__(greenlet_class=RestartableGreenlet, *args, **kwargs)

    def spawn(self, run, *args, **kwargs):
        """
        An override of the gevent.pool.Pool.spawn(). Exactly the same but uses the kwarg 'restart' to determine if this greenlet restarts.
        If not provided, it defaults to the pool default value
        """
        restart = kwargs.pop('restart', None) or self.restart
        new_greenlet = super(RestartPool, self).spawn(run, restart, *args, **kwargs)
        new_greenlet.link_exception(self._greenlet_monitor)
        return new_greenlet

    def _greenlet_monitor(self, exceptional_greenlet):
        function_name = exceptional_greenlet.run_target.__name__
        error_message = exceptional_greenlet.exception.message

        if self.logger:
            self.logger.error("Greenlet '{function_name}' has encountered an uncaught error: {err}".format(function_name=function_name,
                                                                                                         err=error_message))
        if exceptional_greenlet.restart:
            sleep(self.sleep_interval)
            if self.logger:
                self.logger.info("Restarting greenlet '{function_name}'...".format(function_name=function_name))

            self.spawn(exceptional_greenlet.run_target, *exceptional_greenlet.run_target_args, **exceptional_greenlet.run_target_kwargs)
        else:
            if self.logger:
                self.logger.info("Greenlet '{function_name}' does not desire a restart.".format(function_name=function_name))
            else:
                raise exceptional_greenlet.exception