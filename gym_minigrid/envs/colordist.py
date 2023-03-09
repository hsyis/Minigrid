from gym_minigrid.roomgrid import RoomGrid
from gym_minigrid.register import register

class ColorDist(RoomGrid):
    """
    A ball is behind a locked door, the key is placed in a
    random room.
    """

    def __init__(
        self,
        room_size=9,
        num_rows=2,
        num_cols=1,
        seed=None,
        agent_view_size=9
    ):
        super().__init__(
            room_size=room_size,
            num_rows=num_rows,
            num_cols=num_cols,
            max_steps=100,
            seed=seed,
            agent_view_size=agent_view_size,
        )

    def _gen_grid(self, width, height):
        super()._gen_grid(width, height)

        # Place the agent in the middle
        self.place_agent(0, 1)

        # Colorize the room
        self.colorize_room(0, 0)
        self.colorize_room(0, 1)

        # Make sure all rooms are accessible
        added_doors = self.connect_all()
        self.door = added_doors[0]
        self.nobody_opened = True

        self.mission = 'explore the next room'

    def step(self, action):
        obs, reward, done, info = super().step(action)

        if action == self.actions.toggle:
            if self.nobody_opened and self.door.is_open:
                reward = self._reward()
                self.nobody_opened = False

        return obs, reward, done, info

class ColorDistR5V9(ColorDist):
    def __init__(self, seed=None):
        super().__init__(
            room_size=5,
            agent_view_size=9,
            seed=seed,
        )

class ColorDistR7V9(ColorDist):
    def __init__(self, seed=None):
        super().__init__(
            room_size=7,
            agent_view_size=9,
            seed=seed,
        )

class ColorDistR9V9(ColorDist):
    def __init__(self, seed=None):
        super().__init__(
            room_size=9,
            agent_view_size=9,
            seed=seed,
        )

class ColorDistR11V9(ColorDist):
    def __init__(self, seed=None):
        super().__init__(
            room_size=11,
            agent_view_size=9,
            seed=seed,
        )

class ColorDistR13V9(ColorDist):
    def __init__(self, seed=None):
        super().__init__(
            room_size=13,
            agent_view_size=9,
            seed=seed,
        )

class ColorDistR15V9(ColorDist):
    def __init__(self, seed=None):
        super().__init__(
            room_size=15,
            agent_view_size=9,
            seed=seed,
        )

register(
    id='MiniGrid-ColorDistR5V9-v0',
    entry_point='gym_minigrid.envs:ColorDistR5V9'
)

register(
    id='MiniGrid-ColorDistR7V9-v0',
    entry_point='gym_minigrid.envs:ColorDistR7V9'
)

register(
    id='MiniGrid-ColorDistR9V9-v0',
    entry_point='gym_minigrid.envs:ColorDistR9V9'
)

register(
    id='MiniGrid-ColorDistR11V9-v0',
    entry_point='gym_minigrid.envs:ColorDistR11V9'
)

register(
    id='MiniGrid-ColorDistR13V9-v0',
    entry_point='gym_minigrid.envs:ColorDistR13V9'
)

register(
    id='MiniGrid-ColorDistR15V9-v0',
    entry_point='gym_minigrid.envs:ColorDistR15V9'
)
