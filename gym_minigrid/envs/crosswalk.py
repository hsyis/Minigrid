from gym_minigrid.minigrid import *
from gym_minigrid.register import register
from operator import add

class CrossWalkEnv(MiniGridEnv):
    """
    Empty grid environment, no obstacles, sparse reward
    """

    def __init__(
        self,
        width=100,
        height=7,
        agent_start_pos=None,
        agent_start_dir=None,
        max_steps=20,
        agent_view_size=5,
        counter_factual=True,
    ):
        if agent_start_pos != None:
            self.agent_start_pos = agent_start_pos
        else:
            self.agent_start_pos = (1, height // 2)

        if agent_start_dir != None:
            self.agent_start_dir = agent_start_dir
        else:
            self.agent_start_dir = 0

        super().__init__(
            width=width,
            height=height,
            max_steps=max_steps,
            # Set this to True for maximum speed
            see_through_walls=True,
            agent_view_size=agent_view_size,
        )

        # Allow only 2 actions permitted: left, right
        self.action_space = spaces.Discrete(self.actions.right + 1)
        self.reward_range = (-1, 1)

        self.counter_factual = counter_factual

    def _gen_grid(self, width, height):
        # Create an empty grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Place a goal square in the bottom-right corner
        self.grid.set(width - 2, height // 2, Goal())

        # Place the agent
        if self.agent_start_pos is not None:
            self.agent_pos = self.agent_start_pos
            self.agent_dir = self.agent_start_dir
        else:
            self.place_agent()

        ## Place pedestrians and crosswalk
        self.ped_lights = []
        self.pedestrians = []
        self.bg_cache = []
        for i in range(1, self.grid.width - 1):
            self.put_obj(Floor('grey'), i, 1)
            self.put_obj(Floor('grey'), i, self.grid.height - 2)

        for i in range(5, self.grid.width - 3, 5):
            for j in range(2, self.grid.height - 2):
                self.put_obj(CrossWalk(), i, j)
            self.ped_lights.append('red')
            self.pedestrians.append(Ball(self.ped_lights[-1]))
            self.bg_cache.append(self.grid.get(i, 1))
            self.put_obj(self.pedestrians[-1], i, 1)

        self.mission = "pass the crosswalk"

    def step(self, action):
        if action == 1:
            action = 2  # forward
        else:
            action = 6  # no-op

        # Update pedestrian: green -> red
        for i in range(len(self.pedestrians)):
            if self.ped_lights[i] == 'red':
                continue

            old_pos = self.pedestrians[i].cur_pos
            if old_pos[1] > (self.grid.height - 3):
                self.ped_lights[i] = 'red'
                self.pedestrians[i] = Ball(self.ped_lights[i])
                self.put_obj(self.pedestrians[i], *old_pos)

        # Update pedestrian: position
        for i in range(len(self.pedestrians)):
            old_pos = self.pedestrians[i].cur_pos
            if old_pos[1] > (self.grid.height - 3):
                continue

            if old_pos[1] < 2:
                if self.counter_factual:
                    if self.ped_lights[i] == 'red':
                        if self._rand_int(0, 9) < 8:
                            continue
                else:
                    if self.ped_lights[i] == 'red':
                        continue

            new_pos = tuple(map(add, old_pos, (0, 1)))
            if np.array_equal(new_pos, self.agent_pos):
                continue

            try:
                old_obj = self.bg_cache[i]
                self.bg_cache[i] = self.grid.get(*new_pos)
                self.put_obj(self.pedestrians[i], *new_pos)
                self.grid.set(*old_pos, old_obj)
            except:
                pass

        # Update pedestrian: red -> green
        for i in range(len(self.pedestrians)):
            if self.ped_lights[i] == 'green':
                continue

            cur_pos = self.pedestrians[i].cur_pos
            if cur_pos[1] < 2:
                if self._rand_int(0, 7) < 6:
                    continue

                self.ped_lights[i] = 'green'
                self.pedestrians[i] = Ball(self.ped_lights[i])
                self.put_obj(self.pedestrians[i], *cur_pos)

        # Check if there is an pedestrian in front of the agent
        front_cell = self.grid.get(*self.front_pos)
        accident = front_cell and front_cell.type == 'ball'

        # Update the agent's position/direction
        obs, reward, done, info = MiniGridEnv.step(self, action)

        # If the agent tried to walk over an pedestrian
        if action == self.actions.forward and accident:
            reward = -1
            done = True
            return obs, reward, done, info

        return obs, reward, done, info

class CrossWalkCounterFactualEnv21x9(CrossWalkEnv):
    def __init__(self, **kwargs):
        super().__init__(width=21, height=9, agent_view_size=7, counter_factual=True, **kwargs)

class CrossWalkEnv21x9(CrossWalkEnv):
    def __init__(self, **kwargs):
        super().__init__(width=21, height=9, agent_view_size=7, counter_factual=False, **kwargs)

register(
    id='MiniGrid-CrossWalk-CounterFactual-21x9-v0',
    entry_point='gym_minigrid.envs:CrossWalkCounterFactualEnv21x9'
)

register(
    id='MiniGrid-CrossWalk-21x9-v0',
    entry_point='gym_minigrid.envs:CrossWalkEnv21x9'
)
