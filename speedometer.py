#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
The Speedometer module provides one class and one function that can be used to
help determine the throughput performance of applications on a system, or
transfers on the network.
"""

def speed_str(speed):
    """
    speed_str(float speed) -> string with , separators and B/s | KiB/s | MiB/s
    """
    if speed > 1024*1024:
        return '{:,.4}'.format(speed/1024/1024) + ' MiB/s'
    elif speed > 1024:
        return '{:,.4}'.format(speed/1024) + ' KiB/s'
    else:
        return '{:,.4}'.format(speed) + ' B/s'

class Speedometer(object):
    """
    The Speedometer class implements a file copier that gives regular updates
    on the number of bytes copied, the time taken and the average speed of the
    transfer.
    """

    def __init__(self, in_fd, out_fd, info_fd):
        """
        This method sets up the instance of Speedometer and runs it.
        """
        self.in_fd = in_fd
        self.out_fd = out_fd
        self.info_fd = info_fd
        self.total_bytes = 0
        self.start_time = None
        self.total_time = 0.0
        self.average_speed = 0.0

    def start(self):
        """
        This method actually starts the transfer and writes out the statistics.
        """
        import datetime

        with self.in_fd as in_file:
            with self.out_fd as out_file:
                with self.info_fd as info_file:
                    self.total_bytes = 0
                    self.start_time = datetime.datetime.now()
                    while 1:
                        data = in_file.read(8192)
                        if len(data) == 0:
                            break
                        out_file.write(data)

                        self.total_bytes += len(data)
                        self.total_time = (datetime.datetime.now() -
                            self.start_time).total_seconds()
                        self.average_speed = self.total_bytes / self.total_time

                        info_file.write(
                            '\033[0GTotal bytes: %d ' % self.total_bytes +
                            'Total time: %.3f ' % self.total_time +
                            'Average speed: %s\033[K' % speed_str(
                                self.average_speed)
                            )
                    info_file.write('\n')

    def reset(self):
        """
        reset all counters to zero and bring the instance back to
        post-instantiate state.
        """
        self.__init__()

if __name__ == '__main__':
    import sys
    SPEEDO = Speedometer(sys.stdin, sys.stdout, sys.stderr)
    SPEEDO.start()
