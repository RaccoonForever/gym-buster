import numpy as np
import tensorflow as tf
import sklearn.preprocessing

import gym_buster.envs.buster_env as env


class ActorCritic(object):

    def __init__(self, env, session, scaler):
        self.env = env
        self.session = session
        self.input_dims = env.observation_space.shape[0]
        self.scaler = scaler

    def value_function(self, state):
        n_hidden1 = 400
        n_hidden2 = 400
        n_outputs = self.env.action_space.shape[0]

        with tf.variable_scope("value_network"):
            hidden1 = tf.layers.dense(state, n_hidden1, tf.nn.elu, tf.contrib.layers.xavier_initializer())
            hidden2 = tf.layers.dense(hidden1, n_hidden2, tf.nn.elu, tf.contrib.layers.xavier_initializer())
            value = tf.layers.dense(hidden2, n_outputs, None, tf.contrib.layers.xavier_initializer())

        return value

    def policy_network(self, state):
        n_hidden1 = 40
        n_hidden2 = 40
        n_outputs = self.env.action_space.shape[0]

        with tf.variable_scope("policy_network"):
            init_xavier = tf.contrib.layers.xavier_initializer()

            hidden1 = tf.layers.dense(state, n_hidden1, tf.nn.elu, init_xavier)
            hidden2 = tf.layers.dense(hidden1, n_hidden2, tf.nn.elu, init_xavier)
            mu = tf.layers.dense(hidden2, n_outputs, None, init_xavier)
            sigma = tf.layers.dense(hidden2, n_outputs, None, init_xavier)
            sigma = tf.nn.softplus(sigma) + 1e-5
            norm_dist = tf.contrib.distributions.Normal(mu, sigma)
            action_tf_var = tf.squeeze(norm_dist.sample(1), axis=0)
            action_tf_var = tf.clip_by_value(action_tf_var, environment.action_space.low[0],
                                             environment.action_space.high[0])
        return action_tf_var, norm_dist

    def scale_state(self, state):
        scaled = self.scaler.transform([state])
        return scaled


if __name__ == '__main__':
    environment = env.BusterEnv()
    environment.seed(123)

    # state normalization
    state_space_samples = np.array(
        [environment.observation_space.sample() for x in range(10000)])
    scaler = sklearn.preprocessing.StandardScaler()
    scaler.fit(state_space_samples)

    with tf.Session() as session:

        ac = ActorCritic(environment, session, scaler)

        lr_actor = 0.00002
        lr_critic = 0.001

        action_placeholder = tf.placeholder(tf.float32)
        delta_placeholder = tf.placeholder(tf.float32)
        target_placeholder = tf.placeholder(tf.float32)
        state_placeholder = tf.placeholder(tf.float32, [None, ac.input_dims])

        action_tf_var, norm_dist = ac.policy_network(state_placeholder)
        value = ac.value_function(state_placeholder)

        loss_actor = -tf.log(norm_dist.prob(action_placeholder) + 1e-5) * delta_placeholder
        training_op_actor = tf.train.AdamOptimizer(lr_actor, name='actor_optimizer').minimize(loss_actor)

        loss_critic = tf.reduce_mean(tf.squared_difference(tf.squeeze(value), target_placeholder))
        training_op_critic = tf.train.AdamOptimizer(lr_critic, name='critic_optimizer').minimize(loss_critic)

        gamma = 0.99

        episodes = 0
        session.run(tf.global_variables_initializer())
        episodes_history = []

        while episodes < 10000:
            state = environment.reset()
            environment.render()

            reward_total = 0
            done = False

            while not done:
                action = session.run(action_tf_var, feed_dict={state_placeholder: ac.scale_state(state)})

                next_state, reward, done, _ = environment.step(np.squeeze(action, axis=0))

                reward_total += reward

                V_of_next_state = session.run(value, feed_dict={state_placeholder: ac.scale_state(next_state)})

                target = reward + gamma * np.squeeze(V_of_next_state)

                td_error = target - np.squeeze(session.run(value, feed_dict={state_placeholder: ac.scale_state(state)}))

                _, loss_actor_val = session.run(
                    [training_op_actor, loss_actor],
                    feed_dict={action_placeholder: np.squeeze(action),
                               state_placeholder: ac.scale_state(state),
                               delta_placeholder: td_error}
                )

                _, loss_critic_val = session.run(
                    [training_op_critic, loss_critic],
                    feed_dict={state_placeholder: ac.scale_state(state),
                               target_placeholder: target}
                )

                state = next_state

                environment.render()

            episodes += 1
            episodes_history.append(reward_total)
            print("Episode: {}, Number of Steps: {}, Cumulative reward: {}".format(episodes, environment.current_step,
                                                                                   reward_total))

            environment.close()

            if episodes // 100 == 0:
                print("****************Solved***************")
                print("Mean cumulative reward over 100 episodes:{:0.2f}".format(
                    np.mean(episodes_history[-100:])))
