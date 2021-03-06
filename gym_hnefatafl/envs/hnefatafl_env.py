import copy

import gym
from gym_hnefatafl.envs.render_utils import Render_utils
from gym_hnefatafl.envs.board import Outcome
from gym_hnefatafl.envs.board import HnefataflBoard
from gym_hnefatafl.envs.board import Player


# the environment class necessary for integration with gym
class HnefataflEnv(gym.Env):
    """The main OpenAI Gym class. It encapsulates an environment with
    arbitrary behind-the-scenes dynamics. An environment can be
    partially or fully observed.
    The main API methods that users of this class need to know are:
        step
        reset
        render
        close
        seed
    And set the following attributes:
        action_space: The Space object corresponding to valid actions
        observation_space: The Space object corresponding to valid observations
        reward_range: A tuple corresponding to the min and max possible rewards
    Note: a default reward range set to [-inf,+inf] already exists. Set it if you want a narrower range.
    The methods are accessed publicly as "step", "reset", etc.. The
    non-underscored versions are wrapper methods to which we may add
    functionality over time.
    """

    # Set this in SOME subclasses
    metadata = {'render.modes': []}
    reward_range = (-float('inf'), float('inf'))
    spec = None

    # Set these in ALL subclasses
    observation_space = None

    def __init__(self, size):
        self.size = size
        self.viewer = None
        self._hnefatafl = HnefataflBoard(size)
        self._blackTurn = True
        self.action_space = []
        self.recalculate_action_space()

    def step(self, action):
        """Run one timestep of the environment's dynamics. When end of
        episode is reached, you are responsible for calling `reset()`
        to reset this environment's state.
        Accepts an action and returns a tuple (observation, reward, done, info).
        Args:
            action (object): an action provided by the environment
        Returns:
            observation (object): agent's observation of the current environment
            reward (float) : amount of reward returned after previous action
            done (boolean): whether the episode has ended, in which case further step() calls will return undefined results
            info (dict): contains auxiliary diagnostic information (helpful for debugging, and sometimes learning)
        """

        captured_pieces = self._hnefatafl.do_action(action, self.turn_player())
        self._blackTurn = not self._blackTurn
        self.recalculate_action_space()

        game_over = self._hnefatafl.outcome != Outcome.ongoing
        return self, 0, game_over, self._hnefatafl.outcome, captured_pieces

    # returns a copy of the internal board
    def get_board(self):
        board_copy = copy.deepcopy(self._hnefatafl)
        board_copy.print_to_console = False
        board_copy.save_game=False
        return board_copy

        # return self._hnefatafl.copy()

    # recalculates the action space for the agent whose turn it is next
    def recalculate_action_space(self):
        self.action_space = self._hnefatafl.get_valid_actions(self.turn_player())

    # returns either Player.black or Player.white depending on whose turn it is
    def turn_player(self):
        return Player.black if self._blackTurn else Player.white

    def reset(self):
        """Resets the state of the environment and returns an initial observation.
        Returns: observation (object): the initial observation of the
            space.
        """
        self._hnefatafl = HnefataflBoard()
        self._blackTurn = True
        self.recalculate_action_space()

        raise NotImplementedError

    def render(self, mode='human'):
        # assert mode in RENDERING_MODES

        img = self.get_image(mode)

        if 'rgb_array' in mode:
            return img

        elif 'human' in mode:
            from gym.envs.classic_control import rendering
            # print(img)
            if self.viewer is None:
                self.viewer = rendering.SimpleImageViewer()
            self.viewer.imshow(img)
            return self.viewer.isopen

        else:
            super(HnefataflEnv, self).render(mode=mode)  # just raise an exception

    def get_image(self, mode):
        # print(self._hnefatafl.board)
        img = Render_utils.room_to_rgb(self._hnefatafl.board, self.size)
        # if mode.startswith('tiny_'):
            # img = Render_utils.room_to_tiny_world_rgb(self.room_state, self.room_fixed, scale=4)

        return img
        """Renders the environment.
        The set of supported modes varies per environment. (And some
        environments do not support rendering at all.) By convention,
        if mode is:
        - human: render to the current display or terminal and
          return nothing. Usually for human consumption.
        - rgb_array: Return an numpy.ndarray with shape (x, y, 3),
          representing RGB values for an x-by-y pixel image, suitable
          for turning into a video.
        - ansi: Return a string (str) or StringIO.StringIO containing a
          terminal-style text representation. The text can include newlines
          and ANSI escape sequences (e.g. for colors).
        Note:
            Make sure that your class's metadata 'render.modes' key includes
              the list of supported modes. It's recommended to call super()
              in implementations to use the functionality of this method.
        Args:
            mode (str): the mode to render with
            close (bool): close all open renderings
        Example:
        class MyEnv(Env):
            metadata = {'render.modes': ['human', 'rgb_array']}
            def render(self, mode='human'):
                if mode == 'rgb_array':
                    return np.array(...) # return RGB frame suitable for video
                elif mode is 'human':
                    ... # pop up a window and render
                else:
                    super(MyEnv, self).render(mode=mode) # just raise an exception
        """
        raise NotImplementedError

    def close(self):
        """Override _close in your subclass to perform any necessary cleanup.
        Environments will automatically close() themselves when
        garbage collected or when the program exits.
        """
        return

    # prints the tile state board
    def __str__(self):
        return str(self._hnefatafl.board)
