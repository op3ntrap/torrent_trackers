import requests
import os

"""
NewTrackon Web API
<https://newtrackon.com/api>

GET https://newtrackon.com/api/stable
Returns a two line delimited list announce URLs of trackers that have an uptime
of equal or more than 95%.

GET https://newtrackon.com/api/:percentage
Returns a two line delimited list announce URLs of trackers that have an uptime
of equal or more than the given percentage.

GET https://newtrackon.com/api/all
Returns a two line delimited list announce URLs of all known trackers, dead or
alive.

GET https://newtrackon.com/api/live
Returns a two line delimited list announce URLs of currently active and
responding trackers.5ion: not readable


GET https://newtrackon.com/api/udp
Returns a two line delimited list announce URLs of stable and UDP trackers.

GET https://newtrackon.com/api/http
Returns a two line delimited list announce URLs of stable and HTTP/HTTPS
trackers.
"""


class NewTrackon:
    """docstring for .NewTrackon"""

    def __init__(self, *args, **kwargs):
        self.base_url = "https://newtrackon.com/api/"
        self.live = self.base_url + "live"
        self.udp = self.base_url + "udp"
        self.http = self.base_url + "http"
        # Data Accumulation
        self.stable_data = [
            link
            for link in requests.get(self.base_url + "stable").text.split("\n\n")
            if len(link) > 2
        ]
        self.live_data = [
            link for link in requests.get(self.live).text.split("\n\n") if len(link) > 2
        ]

        self.udp_data = [
            link for link in requests.get(self.udp).text.split("\n\n") if len(link) > 2
        ]
        self.http_data = [
            link for link in requests.get(self.http).text.split("\n\n") if len(link) > 2
        ]
        # Data Filtering
        self.udp_live_data = [link for link in self.udp_data if link in self.live_data]
        self.http_live_data = [
            link for link in self.http_data if link in self.live_data
        ]
        self.master_dump = []

    def trackers(self):
        self.master_dump = self.stable_data + self.udp_live_data + self.http_live_data
        # Add all the remaining trackers to list from the live data if they all
        # are not already there
        for remaining_tracker in self.live_data:
            if remaining_tracker not in self.master_dump:
                if len(remaining_tracker) > 2:
                    self.master_dump.append(remaining_tracker)
        return self.master_dump


class SubmoduleTrackerLists:
    """docstring for SubmoduleTrackerLists."""

    def __init__(self, *arg):
        self.lists_dir = os.getcwd() + "/trackerslist/"
        # Sort through all the best lists.
        self.best_lists = [
            self.lists_dir + trackers_list
            for trackers_list in os.listdir(self.lists_dir)
            if "best" in trackers_list
        ]
        # print(self.bestlists)
        self.best_trackers = []
        for b_list in self.best_lists:
            with open(b_list, "r") as raw_data:  # B_list are short for best_lists.
                local_trackers = [
                    tracker.strip()
                    for tracker in raw_data.readlines()
                    if len(tracker) > 4
                ]
                self.best_trackers.extend(local_trackers)
        # Evaluate other lists
        self.other_trackers = []
        self.other_lists = [
            self.lists_dir + trackers_list
            for trackers_list in os.listdir(self.lists_dir)
            if "best" not in trackers_list and "trackers" in trackers_list
        ]
        for o_list in self.other_lists:
            with open(o_list, "r") as raw_data:
                local_trackers = [
                    tracker.strip()
                    for tracker in raw_data.readlines()
                    if len(tracker) > 4
                ]
                self.other_trackers.extend(local_trackers)
        # Remove Duplicates
        self.other_trackers = list(dict.fromkeys(self.other_trackers))


if __name__ == "__main__":
    am = SubmoduleTrackerLists()
    pm = NewTrackon()
    # Finally fffffff

    for val in am.best_trackers:
        print(val)
    for val in pm.master_dump:
        print(val)
    print("\n\n# Other Trackers\n\n")
    for val in am.other_trackers:
        print(val)
