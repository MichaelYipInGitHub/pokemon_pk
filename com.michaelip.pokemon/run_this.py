from pokemon_env import Pokemon
from RL_brain_DQN import DeepQNetwork
# from RL_brain_DoubleDQN import DoubleDQN
import tensorflow.compat.v1 as tf
tf.compat.v1.disable_eager_execution()

def run_pokemon():
    step = 0    # 用来控制什么时候学习
    win_count = 0
    for episode in range(5000):
        # 初始化环境
        observation = env.reset()
        print('episode:%s start'%(episode+1))
        while True:
            # 刷新环境
            env.render()

            # DQN 根据观测值选择行为
            action = RL.choose_action(observation)

            # 环境根据行为给出下一个 state, reward, 是否终止
            observation_, reward, done, _ = env.step(action)

            # DQN 存储记忆
            RL.store_transition(observation, action, reward, observation_)

            # 控制学习起始时间和频率 (先累积一些记忆再开始学习)
            if (step > 200) and (step % 5 == 0):
                RL.learn()

            # 将下一个 state_ 变为 下次循环的 state
            observation = observation_

            # 如果终止, 就跳出循环
            if done:
                if reward > 1000:
                    win_count += 1
                break
            step += 1   # 总步数

        if ((episode+1) % 1000 == 0):
            print('胜率：%s/1000'%(win_count))
            win_count = 0

    # end of game
    print('game over')
    env.destroy()


if __name__ == "__main__":
    env = Pokemon()
    RL = DeepQNetwork(env.n_actions, env.n_features,
                      learning_rate=0.01,
                      reward_decay=0.9,
                      e_greedy=1.0,
                      replace_target_iter=200,  # 每 200 步替换一次 target_net 的参数
                      memory_size=2000, # 记忆上限
                      e_greedy_increment=0.0001,#每次训练完后 Epsilon  增加的值
                      # output_graph=True   # 是否输出 tensorboard 文件
                      )
    # RL = DoubleDQN(
    #     n_actions=env.n_actions, n_features=7, memory_size=3000,
    #     e_greedy_increment=0.001, double_q=True,  output_graph=False)
    env.after(100, run_pokemon)
    env.mainloop()
    RL.plot_cost()  # 观看神经网络的误差曲线