from gym_minigrid.roomgrid import RoomGrid
from gym_minigrid.register import register
from gym_minigrid.minigrid import Door, Key, Floor, spaces
import numpy as np

class EColiV1(RoomGrid):
    """
    One room with random distribution of colored tiles.
    E. coli can navigate towards or away from chemical gradients in their environment.
    """

    def __init__(
        self,
        room_size=11,
        num_rows=1,
        num_cols=1,
        seed=None,
        agent_view_size=5
    ):
        super().__init__(
            room_size=room_size,
            num_rows=num_rows,
            num_cols=num_cols,
            max_steps=200,
            seed=seed,
            agent_view_size=agent_view_size,
        )

        # Range of possible rewards
        self.reward_range = (-1, 1)

        # Allow only 3 actions permitted: left, right, forward
        self.action_space = spaces.Discrete(self.actions.forward + 1)

        self.agent_life_max = 10.0
        self.agent_life = self.agent_life_max

    def _gen_grid(self, width, height):
        super()._gen_grid(width, height)

        self.target_color = "green"
        self.mission = f"survive by eating {self.target_color} nutrients"

        self.target_count = self.colorize_room()

        self.achievement_obj = False
        self.achievement_all = False

    def colorize_room(self):
        target_count = 0
        room = self.get_room(0, 0)

        top = room.top
        size = room.size

        # chemical gradients
        mass_point = (self._rand_int(top[0] + 1, top[0] + size[0] - 1),
                      self._rand_int(top[1] + 1, top[1] + size[1] - 1))

        for w in range(top[0] + 1, top[0] + size[0] - 1):
            for h in range(top[1] + 1, top[1] + size[1] - 1):
                distance = (abs(mass_point - np.array((w, h)))).sum()
                if self._rand_float(0, 1.0) < distance / 6:
                    color = self._rand_color()
                else:
                    color = self.target_color

                if color == self.target_color:
                    target_count += 1

                obj = Floor(color)
                self.put_obj(obj, w, h)

        start_cell = self.grid.get(*self.agent_pos)
        start_cell.color = 'grey'

        return target_count

    def step(self, action):
        obs, reward, done, info = super().step(action)

        visit_cell = self.grid.get(*self.agent_pos)
        if visit_cell.color == self.target_color:
            self.achievement_obj += 1
            reward += 1.0
            visit_cell.color = 'grey'

        info['achievement_obj'] = self.achievement_obj
        info['achievement_all'] = (self.achievement_obj == self.target_count)

        return obs, reward, done, info

class EColiV1R11(EColiV1):
    def __init__(self, seed=None):
        super().__init__(
            room_size=11,
            agent_view_size=5,
            seed=seed,
        )

register(
    id='MiniGrid-EColiR11-v1',
    entry_point='gym_minigrid.envs:EColiV1R11'
)
