from gym_minigrid.roomgrid import RoomGrid
from gym_minigrid.register import register
from gym_minigrid.minigrid import Door, Key
import numpy as np

class ColorDistV0(RoomGrid):
    """
    Two room with random distribution of colored tiles.
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

class ColorDistV0R5(ColorDistV0):
    def __init__(self, seed=None):
        super().__init__(
            room_size=5,
            agent_view_size=9,
            seed=seed,
        )

class ColorDistV0R7(ColorDistV0):
    def __init__(self, seed=None):
        super().__init__(
            room_size=7,
            agent_view_size=9,
            seed=seed,
        )

class ColorDistV0R9(ColorDistV0):
    def __init__(self, seed=None):
        super().__init__(
            room_size=9,
            agent_view_size=9,
            seed=seed,
        )

class ColorDistV0R11(ColorDistV0):
    def __init__(self, seed=None):
        super().__init__(
            room_size=11,
            agent_view_size=9,
            seed=seed,
        )

class ColorDistV0R13(ColorDistV0):
    def __init__(self, seed=None):
        super().__init__(
            room_size=13,
            agent_view_size=9,
            seed=seed,
        )

class ColorDistV0R15(ColorDistV0):
    def __init__(self, seed=None):
        super().__init__(
            room_size=15,
            agent_view_size=9,
            seed=seed,
        )

register(
    id='MiniGrid-ColorDistR5-v0',
    entry_point='gym_minigrid.envs:ColorDistV0R5'
)

register(
    id='MiniGrid-ColorDistR7-v0',
    entry_point='gym_minigrid.envs:ColorDistV0R7'
)

register(
    id='MiniGrid-ColorDistR9-v0',
    entry_point='gym_minigrid.envs:ColorDistV0R9'
)

register(
    id='MiniGrid-ColorDistR11-v0',
    entry_point='gym_minigrid.envs:ColorDistV0R11'
)

register(
    id='MiniGrid-ColorDistR13-v0',
    entry_point='gym_minigrid.envs:ColorDistV0R13'
)

register(
    id='MiniGrid-ColorDistR15-v0',
    entry_point='gym_minigrid.envs:ColorDistV0R15'
)


class ColorDistV1(RoomGrid):
    """
    Two room with random distribution of colored tiles.
    A key is behind an unlocked door.
    """

    def __init__(
        self,
        room_size=9,
        num_rows=2,
        num_cols=1,
        seed=None,
        agent_view_size=9
    ):
        self.achievement_door = False
        self.achievement_key = False

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

        # Add an object
        color = self._rand_color()
        self.obj = Key(color)
        obj_pos = np.array((self.room_size // 2, self.room_size // 2))
        self.grid.set(*obj_pos, self.obj)
        self.obj.init_pos = obj_pos
        self.obj.cur_pos = obj_pos
        self.get_room(0, 0).objs.append(self.obj)

        # Add an unlocked door
        self.door = Door(color, is_locked=False)
        door_pos = np.array((self.room_size // 2, self.room_size - 1))
        self.grid.set(*door_pos, self.door)
        self.door.cur_pos = door_pos
        room1 = self.get_room(0, 0)
        room1.door_pos[1] = door_pos
        room1.doors[1] = self.door
        room2 = self.get_room(0, 1)
        room2.door_pos[3] = door_pos
        room2.doors[3] = self.door

        self.mission = "pick up the %s %s" % (self.obj.color, self.obj.type)

    def step(self, action):
        obs, reward, done, info = super().step(action)

        if action == self.actions.toggle:
            if not self.achievement_door and self.door.is_open:
                self.achievement_door = True
                reward = self._reward() * 0.5

        if action == self.actions.pickup:
            if self.carrying and self.carrying == self.obj:
                self.achievement_obj = True
                reward = self._reward()
                done = True

        info['achievement_door'] = self.achievement_door
        info['achievement_key'] = self.achievement_key

        return obs, reward, done, info

class ColorDistV1R5(ColorDistV1):
    def __init__(self, seed=None):
        super().__init__(
            room_size=5,
            agent_view_size=9,
            seed=seed,
        )

class ColorDistV1R7(ColorDistV1):
    def __init__(self, seed=None):
        super().__init__(
            room_size=7,
            agent_view_size=9,
            seed=seed,
        )

class ColorDistV1R9(ColorDistV1):
    def __init__(self, seed=None):
        super().__init__(
            room_size=9,
            agent_view_size=9,
            seed=seed,
        )

class ColorDistV1R11(ColorDistV1):
    def __init__(self, seed=None):
        super().__init__(
            room_size=11,
            agent_view_size=9,
            seed=seed,
        )

class ColorDistV1R13(ColorDistV1):
    def __init__(self, seed=None):
        super().__init__(
            room_size=13,
            agent_view_size=9,
            seed=seed,
        )

class ColorDistV1R15(ColorDistV1):
    def __init__(self, seed=None):
        super().__init__(
            room_size=15,
            agent_view_size=9,
            seed=seed,
        )

register(
    id='MiniGrid-ColorDistR5-v1',
    entry_point='gym_minigrid.envs:ColorDistV1R5'
)

register(
    id='MiniGrid-ColorDistR7-v1',
    entry_point='gym_minigrid.envs:ColorDistV1R7'
)

register(
    id='MiniGrid-ColorDistR9-v1',
    entry_point='gym_minigrid.envs:ColorDistV1R9'
)

register(
    id='MiniGrid-ColorDistR11-v1',
    entry_point='gym_minigrid.envs:ColorDistV1R11'
)

register(
    id='MiniGrid-ColorDistR13-v1',
    entry_point='gym_minigrid.envs:ColorDistV1R13'
)

register(
    id='MiniGrid-ColorDistR15-v1',
    entry_point='gym_minigrid.envs:ColorDistV1R15'
)
