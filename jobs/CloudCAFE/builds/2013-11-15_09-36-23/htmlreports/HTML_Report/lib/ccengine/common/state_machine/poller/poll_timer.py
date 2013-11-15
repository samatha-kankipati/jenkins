"""
poll_timer.py

(C) 2013 - Rackspace Hosting, Inc.
Author: Christopher Hunt

Purpose: To provide a simple mechanism for tracking when a timer/poller would
    fire. The class will allow a script to determine when the last time the
    poller fired, when it is due to fire again, and how much time (in seconds)
    until the poller fires or since the poller last fired.

Methods:
    is_poll_now()
    poll_nearest_time()
    time_of_next_poll()
    time_till_next_poll()
    time_of_last_poll()
    time_since_last_poll()

"""
import datetime


class PollTimer(object):
    """
    Provides a simple mechanism for tracking when a timer/poller would fire.
    The class will allow a script to determine when the last time the poller
    fired, when it is due to fire again, and how much time (in seconds) until
    the poller fires or since the poller last fired.

    """

    def __init__(self, reference_time, interval_min):
        """
        @param reference_time: datetime.datetime object containing a known time
             that the poller actually fired (used as a reference for all other
             firing times)
        @param interval_min: interval of time (in mins) when poller should fire
        """
        self.reference_time = reference_time
        self.interval = datetime.timedelta(minutes=interval_min)

    def is_poll_now(self):
        """
        Should the poller be firing at this very second?
        @return:(Boolean): True/False
        """
        return True if self.time_till_next_poll() == 0 else False

    def time_of_next_poll(self):
        """
        Determine when the next poll should occur based on the reference
        time and the poller interval
        @return: (datetime object): The time of the next poll
        """
        event_time = self.reference_time

        # In the case that the event time is in the future,
        # Adjust the event time by the poll interval so that the reference time
        # is in the past (makes the math consistent)
        while datetime.datetime.now() < event_time:
            event_time -= self.interval

        # Determine the difference between now and the event time
        difference = datetime.datetime.now() - event_time

        # Find the number of intervals required to add to the reference time
        # to determine the closest future poll time.
        num_intervals = 1
        while difference > self.interval:
            difference -= self.interval
            num_intervals += 1

        # The next poll would be the known event time + the number of intervals
        return event_time + (num_intervals * self.interval)

    def time_till_next_poll(self):
        """
        Determines the amount of time (in seconds) left until the next poll
        @return: (integer) seconds until next poll
        """
        remaining = self.time_of_next_poll() - datetime.datetime.now()
        return remaining.seconds

    def time_of_last_poll(self):
        """
        Determine the last time the poller should have fired.
        @return: (datetime obj): The last time the poller should have fired.
        """
        return self.time_of_next_poll() - self.interval

    def time_since_last_poll(self):
        """
        Determines the amount of time (in seconds) left until the next poll
        @return: (integer) seconds until next poll
        """
        now = datetime.datetime.now()
        return (now - self.time_of_last_poll()).total_seconds()

    def poll_nearest_time(self, target_time):
        """
        Determines the nearest poll time occurring before the specified time.
        @param target_time: (datetime) Time of interest
        @return: (datetime) Time of poll closest to but before time of interest
        """
        next_poll = self.time_of_next_poll()

        # If reference time is equal or in the future, check if adding interval
        # to next poll exceeds the reference time. If not, then add the
        # interval to the poll time, and check again.
        if next_poll <= target_time:
            while True:
                if next_poll + self.interval < target_time:
                    next_poll += self.interval
                else:
                    return next_poll

        # If reference time is in the past, check if subtracting interval
        # to next poll exceeds the reference time. If so, subtract the
        # interval from poll time again and check.
        else:
            while True:
                if next_poll - self.interval > target_time:
                    next_poll -= self.interval
                else:
                    return next_poll
