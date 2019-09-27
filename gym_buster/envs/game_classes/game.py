import pygame
import sys

from gym_buster.envs.game_classes.constants import Constants
from gym_buster.envs.game_classes.map import Map
from gym_buster.envs.game_classes.buster import Buster
from gym_buster.envs.game_classes.ghost import Ghost
from gym_buster.envs.game_classes.entity import Entity
from gym_buster.envs.game_classes.math_utils import MathUtility
from gym_buster.envs.game_classes.ai_behaviour import Aibehaviour
from gym_buster.envs.game_classes.render.game_rendering import GameRendering


class Game(GameRendering):
    """
    Class that will handle a game
    """

    def __init__(self, mode, ghost_number, buster_number, round_number):
        """
        Constructor
        :param mode: the mode used for the game (console or human)
        """
        print("Initializing game ...")
        GameRendering.__init__(self, Constants.PYGAME_WINDOW_WIDTH, Constants.PYGAME_WINDOW_HEIGHT)
        self.mode = mode
        self.ghost_number = ghost_number
        self.buster_number = buster_number
        self.round_number = round_number
        self.reset()
        self.init_screen()

        self._generate_ghosts(self.ghost_number)
        self._generate_busters(self.buster_number)

        self.clock = pygame.time.Clock()
        print("Initializing game : DONE")

    # -------------- INITIALIZATION AND PRIVATE FUNCTIONS ------------ #

    def reset(self):
        """
        Function that will reset the game
        """
        self.board = Map(Constants.MAP_WIDTH, Constants.MAP_HEIGHT)
        self.speed = Constants.PYGAME_SPEED

        self.score_team_0 = 0
        self.score_team_1 = 0
        self.step = 0
        self.running = True
        self.battle_ended = False
        self.battle_won = False
        self.state = {'battle_ended': False}

    def _generate_busters(self, buster_number):
        """
        Function that will generate all busters
        :param buster_number: the number of buster in each team
        """
        self.busters = []
        for i in range(buster_number):
            self.busters.append(Buster(Constants.TYPE_BUSTER_TEAM_0))
            print(str(self.busters[i - 1]))

        for i in range(buster_number):
            self.busters.append(Buster(Constants.TYPE_BUSTER_TEAM_1))
            print(str(self.busters[buster_number - 1 + i - 1]))

    def _generate_ghosts(self, ghost_number):
        """
        Function that will generate all ghosts
        :param ghost_number: the number of ghosts to generate
        """
        self.ghosts = []
        for i in range(ghost_number):
            self.ghosts.append(Ghost())

    # -------------- INITIALIZATION AND PRIVATE FUNCTIONS ------------ #

    # ----------- RENDERING FUNCTIONS ------------- #

    def game_render(self):
        """
        Function called to render the game
        """

        self.screen.fill(Constants.PYGAME_BLACK)

        for buster in self.busters:
            buster.draw(self.screen)

        for ghost in self.ghosts:
            ghost.draw(self.screen)

        self.render_writings()

        pygame.display.update()

    def render_writings(self):
        """
        Function where score is evolving and redering it in text on screen
        """
        self.text_surface_obj = self.font.render(
            "Team 1 = " + str(self.score_team_0) + " | Team 2 = " + str(self.score_team_1) + " | Step = " + str(
                self.step), True,
            Constants.PYGAME_WHITE)
        self.text_rect_obj = self.text_surface_obj.get_rect()
        self.text_rect_obj.center = (
            round(Constants.PYGAME_WINDOW_WIDTH * 0.2), round(Constants.PYGAME_WINDOW_HEIGHT * 0.9))
        self.screen.blit(self.text_surface_obj, self.text_rect_obj)

    # ----------- END RENDERING FUNCTIONS ------------- #

    # ------------- GAME FUNCTIONS --------------#

    def _get_commands_from_console(self):
        """
        Function that will get commands of each buster from console
        :return: the tuple of each list of command for each team
        """
        print("Enter commands for team 0 (top left)")
        commands_0 = []
        for i in range(self.buster_number):
            commands_0.append(str(input()))

        commands_1 = []
        print("Enter commands for team 1 (bot right)")
        for i in range(self.buster_number):
            commands_1.append(str(input()))

        return commands_0, commands_1

    def _get_command_from_console(self):
        """
        Function that will get commands of each buster from console for one team
        :return: the list of commands
        """
        print("Enter commands for team 0 (top left)")
        commands_0 = []
        for i in range(self.buster_number):
            commands_0.append(str(input()))

        return commands_0

    def _run_round(self, commands_team_0, commands_team_1):
        """
        Function that will run a round and execute each event triggered
        """
        # First execute automatic actions

        print("--------- Running a new round ------------")
        remove_ghosts = []
        # Ghost released in a base
        for ghost in self.ghosts:
            if ghost.is_in_team_0_base and not ghost.captured:
                self.score_team_0 += 1
                ghost.kill()
                remove_ghosts.append(ghost)
            elif ghost.is_in_team_1_base and not ghost.captured:
                self.score_team_1 += 1
                ghost.kill()
                remove_ghosts.append(ghost)
            elif not ghost.captured:
                ghost.value = Constants.VALUE_GHOST_BASIC

        # Remove ghosts not available anymore
        for ghost in remove_ghosts:
            self.ghosts.remove(ghost)

        # Execute for each buster his tasks
        for i in range(1, self.buster_number + 1):
            # Retrieve busters i to execute their action at the same moment (almost)
            buster_team_0 = Buster.get_buster(self.busters, i, Constants.TYPE_BUSTER_TEAM_0)
            buster_team_1 = Buster.get_buster(self.busters, i, Constants.TYPE_BUSTER_TEAM_1)

            command_0 = commands_team_0[i - 1]
            command_1 = commands_team_1[i - 1]

            print(str(buster_team_0) + "| Command : " + command_0)
            self.score_team_0 += buster_team_0.buster_command(command_0)
            print(str(buster_team_1) + " | Command : " + command_1)
            self.score_team_1 += buster_team_1.buster_command(command_1)

        for ghost in self.ghosts:
            # Get all busters with the id of the ghost
            if ghost.value != Constants.VALUE_GHOST_BASIC:
                nb_buster_team_0_busting_this_ghost = []
                nb_buster_team_1_busting_this_ghost = []
                for buster in Buster.busters_0:
                    if buster.value == ghost.id:
                        nb_buster_team_0_busting_this_ghost.append(buster)
                for buster in Buster.busters_1:
                    if buster.value == ghost.id:
                        nb_buster_team_1_busting_this_ghost.append(buster)

                closest = None
                buster_on_this_ghost = len(nb_buster_team_0_busting_this_ghost) + len(
                    nb_buster_team_1_busting_this_ghost)

                # If list length != 0 and same value then draw nobody take the ghost
                if len(nb_buster_team_0_busting_this_ghost) == len(nb_buster_team_1_busting_this_ghost) and len(
                        nb_buster_team_1_busting_this_ghost) > 0:
                    ghost.captured = False
                elif len(nb_buster_team_0_busting_this_ghost) > len(nb_buster_team_1_busting_this_ghost):
                    # Find closest team 0 buster and give it to him
                    closest = nb_buster_team_0_busting_this_ghost[0]
                    dist = MathUtility.distance(ghost.x, ghost.y, closest.x, closest.y)
                    for buster in nb_buster_team_0_busting_this_ghost:
                        new_dist = MathUtility.distance(ghost.x, ghost.y, buster.x, buster.y)
                        if new_dist < dist:
                            dist = new_dist
                            closest = buster

                elif len(nb_buster_team_0_busting_this_ghost) < len(nb_buster_team_1_busting_this_ghost):
                    # Find closest team 1 buster and give it to him
                    closest = nb_buster_team_1_busting_this_ghost[0]
                    dist = MathUtility.distance(ghost.x, ghost.y, closest.x, closest.y)
                    for buster in nb_buster_team_0_busting_this_ghost:
                        new_dist = MathUtility.distance(ghost.x, ghost.y, buster.x, buster.y)
                        if new_dist < dist:
                            dist = new_dist
                            closest = buster

                # Reset all busters with this ghost id except closest
                if closest and buster_on_this_ghost >= 1:
                    if closest.type == Constants.TYPE_BUSTER_TEAM_0 and closest.action == Constants.ACTION_BUSTING:
                        self.score_team_0 += 1
                        ghost.being_captured(closest)
                        closest.capturing_ghost()
                    elif closest.type == Constants.TYPE_BUSTER_TEAM_1 and closest.action == Constants.ACTION_BUSTING:
                        self.score_team_1 += 1
                        ghost.being_captured(closest)
                        closest.capturing_ghost()
                    else:
                        ghost.updating_position(closest)

                    for buster in nb_buster_team_0_busting_this_ghost + nb_buster_team_1_busting_this_ghost:
                        if buster != closest:
                            buster.value = Constants.VALUE_BUSTER_NOTHING
                            buster.state = Constants.STATE_BUSTER_NOTHING

                elif not ghost.captured:
                    for buster in nb_buster_team_0_busting_this_ghost + nb_buster_team_1_busting_this_ghost:
                        buster.value = Constants.VALUE_BUSTER_NOTHING
                        buster.state = Constants.STATE_BUSTER_NOTHING

            else:
                ghost.captured = False

        # make ghost run away for those who are not being busted
        for ghost in self.ghosts:
            if not ghost.captured and ghost.alive:
                ghost.run_away(self.busters)

    def run_step(self, commands, render, step):
        """
        Run a step of the game
        :param commands:  the commands coming from the agent
        """
        self.step = step
        commands_team_1 = Aibehaviour.next_command(Buster.busters_1, self.ghosts)
        self._run_round(commands, commands_team_1)
        if render:
            self.game_render()
            pygame.display.flip()
            self.clock.tick_busy_loop(Constants.FPS)

        # Check alive ghosts
        if len(self.ghosts) == 0:
            self.battle_ended = True
            if self.score_team_0 >= self.score_team_1:
                self.battle_won = True
            else:
                self.battle_won = False

    def loop(self):
        """
        Main function that handle every rounds
        """
        self.game_render()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            # commands_team_0, commands_team_1 = self._get_commands_from_console()
            # Lets say that they can see every ghosts
            # commands_team_1 = Aibehaviour.next_command(Buster.busters_1, self.ghosts)
            commands_team_0 = self._get_command_from_console()
            # self._run_round(commands_team_0, commands_team_1)
            self.game_render()
            pygame.display.flip()
            self.clock.tick(Constants.FPS)

        pygame.quit()
        sys.exit()

    def exit(self):
        """
        Function that will close a gaming session
        """
        self.running = False
        pygame.quit()

    def get_state(self):
        """
        Function that will return the state of the game
        :return: a dictionnary with the game state
        """
        state = {}

        state['scoreteam0'] = self.score_team_0
        state['scoreteam1'] = self.score_team_1
        state['battle_ended'] = self.battle_ended
        state['battle_won'] = self.battle_won
        state['ghosts'] = self.ghosts
        state['team0'] = Buster.busters_0
        state['team1'] = Buster.busters_1

        state['ghostvisibleteam0'] = Entity.get_entities_visible(Buster.busters_0, self.ghosts)
        state['ghostvisibleteam1'] = Entity.get_entities_visible(Buster.busters_1, self.ghosts)
        state['ennemyvisibleteam0'] = Entity.get_entities_visible(Buster.busters_0, Buster.busters_1)
        state['ennemyvisibleteam1'] = Entity.get_entities_visible(Buster.busters_1, Buster.busters_0)

        return state

    # ------------- END GAME FUNCTIONS --------------#

    def _update_entities_position(self):
        """
        Function that will update entities position on the map
        """
        for ghost in self.ghosts:
            self.board.map[ghost.x][ghost.y] = Constants.TYPE_GHOST

        for buster in self.busters:
            self.board.map[buster.x][buster.y] = buster.type
