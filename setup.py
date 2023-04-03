from setuptools import setup

setup(
    name='gym_minigrid',
    version='1.0.3',
    keywords='memory, environment, agent, rl, openaigym, openai-gym, gym',
    url='https://github.com/maximecb/gym-minigrid',
    description='Minimalistic gridworld package for OpenAI Gym',
    packages=['gym_minigrid', 'gym_minigrid.envs'],
    install_requires=[
        'setuptools==65.7.0',
        'gym==0.21.0',
        'matplotlib==3.7.1',
        'numpy>=1.15.0'
    ]
)
