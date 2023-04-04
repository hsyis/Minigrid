from gym_minigrid.minigrid import *
from gym_minigrid.register import register
from operator import add

class MoveItEnv(MiniGridEnv):
    """
    Empty grid environment, no obstacles, sparse reward
    """

    def __init__(
        self,
        size=11,
        agent_start_pos=None,
        agent_start_dir=None,
        n_obstacles=8,
        n_colors=4,
        max_steps=200,
        agent_view_size=5,
    ):
        if agent_start_pos != None:
            self.agent_start_pos = agent_start_pos
        else:
            self.agent_start_pos = (size // 2, size // 2)

        if agent_start_dir != None:
            self.agent_start_dir = agent_start_dir
        else:
            self.agent_start_dir = 0

        self.n_obstacles = n_obstacles
        self.n_colors = n_colors

        super().__init__(
            grid_size=size,
            max_steps=max_steps,
            # Set this to True for maximum speed
            see_through_walls=True,
            agent_view_size=agent_view_size,
        )

        # Allow only 3 actions permitted: left, right, forward
        self.action_space = spaces.Discrete(self.actions.forward + 1)

    def _gen_grid(self, width, height):
        # Create an empty grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Place the agent
        if self.agent_start_pos is not None:
            self.agent_pos = self.agent_start_pos
            self.agent_dir = self.agent_start_dir
        else:
            self.place_agent()

        # Order: red, green, blue, yellow, pruple, grey
        colors = list(COLORS.keys())
        colors[3], colors[4] = colors[4], colors[3]
        colors = colors[:self.n_colors]

        # Place obstacles
        self.obstacles = []
        self.movings = []

        p_top = tuple(map(add, self.agent_pos, (-1, -1)))
        p_size = (3, 3)
        for i_obst in range(self.n_obstacles):
            cnum = self._rand_int(0, len(colors))
            self.obstacles.append(Ball(colors[cnum]))
            self.place_obj(self.obstacles[i_obst], top=p_top, size=p_size, max_tries=100)
            self.movings.append(cnum % 2 + 1)  # 0 or 1

        self.mission = "push the obstacles"

    def step(self, action):
        # Invalid action
        if action >= self.action_space.n:
            action = 2

        # Check if there is an obstacle in front of the agent
        front_cell = self.grid.get(*self.front_pos)

        # Update obstacle positions if the agent tried to push an obstacle
        if action == self.actions.forward and front_cell in self.obstacles:
            old_pos = front_cell.cur_pos
            cur_pos = old_pos
            new_pos = old_pos
            for move in range(self.movings[self.obstacles.index(front_cell)]):
                cur_pos = tuple(map(add, cur_pos, self.dir_vec))
                if self.grid.get(*cur_pos) == None:
                    new_pos = cur_pos
                else:
                    break
            if self.grid.get(*new_pos) == None:
                self.grid.set(*new_pos, front_cell)
                self.grid.set(*old_pos, None)
                front_cell.init_pos = new_pos
                front_cell.cur_pos = new_pos

        # Update the agent's position/direction
        obs, reward, done, info = MiniGridEnv.step(self, action)

        return obs, reward, done, info

class MoveItEnv9x9c3(MoveItEnv):
    def __init__(self, **kwargs):
        super().__init__(size=9, agent_view_size=5, n_colors=3, **kwargs)

class MoveItEnv11x11c3(MoveItEnv):
    def __init__(self, **kwargs):
        super().__init__(size=11, agent_view_size=5, n_colors=3, **kwargs)

class MoveItEnv9x9c4(MoveItEnv):
    def __init__(self, **kwargs):
        super().__init__(size=9, agent_view_size=5, n_colors=4, **kwargs)

class MoveItEnv11x11c4(MoveItEnv):
    def __init__(self, **kwargs):
        super().__init__(size=11, agent_view_size=5, n_colors=4, **kwargs)

register(
    id='MiniGrid-MoveIt-9x9c3-v0',
    entry_point='gym_minigrid.envs:MoveItEnv9x9c3'
)

register(
    id='MiniGrid-MoveIt-11x11c3-v0',
    entry_point='gym_minigrid.envs:MoveItEnv11x11c3'
)

register(
    id='MiniGrid-MoveIt-9x9c4-v0',
    entry_point='gym_minigrid.envs:MoveItEnv9x9c4'
)

register(
    id='MiniGrid-MoveIt-11x11c4-v0',
    entry_point='gym_minigrid.envs:MoveItEnv11x11c4'
)
