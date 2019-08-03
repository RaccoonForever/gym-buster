import random

from .constants import Constants


class Aibehaviour:
    """
    Class that will handle an easy / medium IA
    """

    def __init__(self):
        pass

    @staticmethod
    def next_command(busters, ghosts):
        """
        Function that will return commands to do for the next round
        :param busters: the busters belonging to the AI
        :param ghosts: the ghosts busters can see
        :return: a list of commands
        """
        busters_already_treated = dict(zip(busters, [None, None, None]))
        ghosts_already_treated = []
        commands = []
        if 1 <= len(busters) <= 3:
            for buster in busters:
                # If a buster is carrying a ghost then go back to base or release if in distance
                if buster.state == Constants.STATE_BUSTER_CARRYING and busters_already_treated[buster] is None:
                    print("Buster " + str(buster.id) + " carrying a ghost.")
                    # Verify if in base else go back to base
                    if buster.is_in_team_base():
                        busters_already_treated[buster] = "RELEASE"
                    else:
                        busters_already_treated[buster] = "MOVE 15000 8000"
                    continue

                # If a busters can see a ghost then go on it (only one)
                for ghost in ghosts:
                    if buster.can_bust(ghost) and busters_already_treated[buster] is None:
                        busters_already_treated[buster] = "BUST " + str(ghost.id)
                        ghosts_already_treated.append(ghost)
                        continue

                # if busters can see a ghost go for it
                for ghost in ghosts:
                    if not buster.can_bust(ghost) and ghost not in ghosts_already_treated and \
                            busters_already_treated[buster] is None:
                        busters_already_treated[buster] = "MOVE " + str(int(ghost.x)) + " " + str(int(ghost.y))
                        ghosts_already_treated.append(ghost)
                        continue

                # move randomly if nothing good
                if busters_already_treated[buster] is None:
                    x = random.randint(1500, 14500)
                    y = random.randint(1000, 8000)
                    busters_already_treated[buster] = "MOVE " + str(x) + " " + str(y)

        for buster in busters:
            commands.append(busters_already_treated[buster])

        return commands
