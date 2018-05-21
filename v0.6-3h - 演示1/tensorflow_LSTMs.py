
from __future__ import print_function

import tensorflow as tf
from tensorflow.contrib import rnn
import numpy as np
import matplotlib.pyplot as plt

import pickle as pickle     # python pkl 文件读写

def LSTMs(x, weights, biases, timesteps , num_hidden):
    # Prepare data shape to match `rnn` function requirements
    # Current data input shape: (batch_size, timesteps, n_input)
    # Required shape: 'timesteps' tensors list of shape (batch_size, n_input)

    # Unstack to get a list of 'timesteps' tensors of shape (batch_size, n_input)
    x = tf.unstack(x, timesteps, 1)

    # Define a lstm cell with tensorflow
    lstm_cell = rnn.BasicLSTMCell(num_hidden, forget_bias=1.0)

    # Get lstm cell output
    outputs, states = rnn.static_rnn(lstm_cell, x, dtype=tf.float32)

    # Linear activation, using rnn inner loop last output
    return tf.matmul(outputs[-1], weights['out']) + biases['out']


def MyNetworks(MyLearning_rate, MyNum_input, MyTimesteps, MyNum_hidden, MyNum_classes):

    learning_rate = MyLearning_rate
    # Network Parameters
    num_input = MyNum_input
    timesteps = MyTimesteps # timesteps
    num_hidden = MyNum_hidden # hidden layer num of features
    num_classes = MyNum_classes # MNIST total classes (1-4 digits)

    ''' ********************************************************************************** '''
    

    # tf Graph input
    X = tf.placeholder("float", [None, timesteps, num_input])
    Y = tf.placeholder("float", [None, num_classes])

    # Define weights
    weights = {
        'out': tf.Variable(tf.random_normal([num_hidden, num_classes]))
    }
    biases = {  
        'out': tf.Variable(tf.random_normal([num_classes]))
    }

    logits = LSTMs(X, weights, biases, timesteps , num_hidden)
    prediction = tf.nn.softmax(logits) # prediction-预测

    # Define loss and optimizer
    # 定义 损失函数 和 优化器
    loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
        logits=logits, labels=Y))
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
    train_op = optimizer.minimize(loss_op)

    # Evaluate model (with test logits, for dropout to be disabled)
    # 评估模型（使用测试日志，禁用dropout）
    correct_pred = tf.equal(tf.argmax(prediction, 1), tf.argmax(Y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    return train_op, loss_op, prediction, accuracy, X, Y

