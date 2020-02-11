from gym.envs.registration import register

register(
    id="hnefatafl-v0", entry_point="gym_hnefatafl.envs:HnefataflEnv",
)

register(
    id="hnefatafl-7x7-v0",
    entry_point="gym_hnefatafl.envs:HnefataflEnv",
    kwargs={"size": 7},
)

register(
    id="hnefatafl-9x9-v0",
    entry_point="gym_hnefatafl.envs:HnefataflEnv",
    kwargs={"size": 9},
)

register(
    id="hnefatafl-11x11-v0",
    entry_point="gym_hnefatafl.envs:HnefataflEnv",
    kwargs={"size": 11},
)
