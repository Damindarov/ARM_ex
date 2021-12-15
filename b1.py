import gym
import time

env = gym.make('MountainCar-v0')
observation = env.reset()
print(observation)
done = False
fitness = 0
step_counter = 0
while not done:
    action = env.action_space.sample()
    observation, reward, done, info = env.step(action)
    fitness += reward
    print(f"\nStep: {step_counter}\nObservation vector: {observation}\n"
        f"Action vector: {action}\nReward: {reward}\nFitness: {fitness}")
    if done:
        time.sleep(3)
    env.render()
    time.sleep(0.1)
    step_counter += 1
env.close()
print(fitness)