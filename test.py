#!/usr/bin/env python3

import collections
import datetime
import math
import os
import sys

from solution import solve
from util import Color, Vector3


BOLD    = "\u001b[1m"
GRAY    = "\u001b[38;5;248m"
CYAN    = "\u001b[36m"
RED     = "\u001b[31m"
GREEN   = "\u001b[32m"
YELLOW  = "\u001b[33m"
RESET   = "\u001b[0m"

TIMEOUT = datetime.timedelta(seconds=600)


def fail(message):
    print(RED + BOLD + "FAIL: " + RESET + message + "\n")
    sys.exit(1)


def check(condition, message):
    if not condition:
        fail(message)


class Scenario(object):
    def __init__(self, path: str):
        super().__init__()

        self.sats = {}
        self.users = {}
        self.min_coverage = 1.0

        for line in open(path):
            line = line.split('#')[0].strip()
            if line == '':
                continue

            parts = line.split()
            if parts[0] == 'min_coverage':
                self.min_coverage = float(parts[1])
            elif parts[0] == 'sat':
                self.sats[int(parts[1])] = Vector3(float(parts[2]), float(parts[3]), float(parts[4]))
            elif parts[0] == 'user':
                self.users[int(parts[1])] = Vector3(float(parts[2]), float(parts[3]), float(parts[4]))
            else:
                fail("Invalid token: %r" % parts[0])

    def check(self, solution):
        beams = collections.defaultdict(list)

        for user, (sat, color) in solution.items():
            user_pos = self.users[user]
            sat_pos = self.sats[sat]
            check(color in Color, 'Invalid color: %r' % color)

            angle = math.degrees(math.acos(user_pos.unit().dot((sat_pos - user_pos).unit())))
            check(angle <= 45,
                  "User %d cannot see satellite %d (%.2f degrees from vertical)" %
                  (user, sat, angle))

            beams[sat].append((color, user))


        for sat, sat_beams in beams.items():
            sat_pos = self.sats[sat]
            check(len(sat_beams) <= 32,
                  "Satellite %d cannot serve more than 32 users (%d assigned)" %
                  (sat, len(sat_beams)))
            for color1, user1 in sat_beams:
                for color2, user2 in sat_beams:
                    if color1 == color2 and user1 != user2:
                        user1_pos = self.users[user1]
                        user2_pos = self.users[user2]
                        angle = sat_pos.angle_between(user1_pos, user2_pos)
                        check(angle >= 10.0,
                              "Users %d and %d on satellite %d %s are too close (%.2f degrees)" %
                              (user1, user2, sat, color1, angle))

        coverage = 1.0 * len(solution) / len(self.users)
        check(coverage >= self.min_coverage, "Too few users served")


def main():
    if len(sys.argv) != 3:
        print("USAGE: %s TEST_CASE OUT_PATH" % sys.argv[0])
        sys.exit(1)

    test_case = sys.argv[1]
    out_path  = sys.argv[2]

    print(BOLD + CYAN + "============================================================" + RESET)
    print(BOLD + CYAN + test_case + RESET)
    print(BOLD + CYAN + "============================================================" + RESET)

    scenario = Scenario(test_case)

    print((GRAY + "Scenario: " + RESET + "%.2f%% coverage (%d users, %d sats)" + RESET) % (
          100 * scenario.min_coverage,
          len(scenario.users),
          len(scenario.sats),
    ))

    start    = datetime.datetime.now()
    solution = solve(scenario.users, scenario.sats)
    duration = datetime.datetime.now() - start
    covered  = 1.0 * len(solution) / len(scenario.users)

    print((GRAY + "Solution: " + RESET + BOLD + "%s%.2f%%" + RESET + " coverage (%d users) in %s" + BOLD + "%.2fs" + RESET) % (
          GREEN if covered >= scenario.min_coverage else RED,
          100.0 * len(solution) / len(scenario.users),
          len(solution),
          RED if duration > TIMEOUT else YELLOW if duration > TIMEOUT / 2 else GREEN,
          duration.total_seconds(),
    ))

    with open(out_path, 'a') as out:
        out.write('%-44s %6.2f%% %6.2fs\n' % (test_case, 100.0 * covered, duration.total_seconds()))

    check(duration < TIMEOUT, "Took too long to produce a solution")
    scenario.check(solution)


if __name__ == '__main__':
    if os.environ.get('PROFILE', None) == '1':
        import cProfile, pstats, io
        profile = cProfile.Profile()

        profile.enable()
        main()
        profile.disable()

        pstats.Stats(profile).sort_stats(pstats.SortKey.CUMULATIVE).print_stats()

    else:
        main()
