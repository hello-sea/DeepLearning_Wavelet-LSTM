# -*- coding:utf-8 -*-
import tensorflow as tf
import numpy as np


def LSTM():
    ######################################################################
    #首先设置好模型用到的各个超参数


    # 每个时刻的输入特征是28维的，就是每个时刻输入一行，一行有 28 个像素
    input_size = 28
    # 时序持续长度为28，即每做一次预测，需要先输入28行
    timestep_size = 28
    
    # 每个隐含层的节点数
    hidden_size = 256
    # LSTM layer 的层数
    layer_num = 2
    # 最后输出分类类别数量，如果是回归预测的话应该是 1
    class_num = 10

    # 在训练和测试的时候，我们想用不同的 batch_size.所以采用占位符的方式
    batch_size = tf.placeholder(tf.int32, []) # 注意类型必须为 tf.int32


    _X = tf.placeholder(tf.float32, [None, 784])
    y = tf.placeholder(tf.float32, [None, class_num])
    keep_prob = tf.placeholder(tf.float32)


    # 把784个点的字符信息还原成 28 * 28 的图片
    # 下面几个步骤是实现 RNN / LSTM 的关键
    #################################################################### 
    
    # **步骤1：RNN 的输入shape = (batch_size, timestep_size, input_size) 
    X = tf.reshape(_X, [-1, 28, 28])

    # **步骤2：定义一层 LSTM_cell，只需要说明 hidden_size, 它会自动匹配输入的 X 的维度
    lstm_cell = tf.contrib.rnn.BasicLSTMCell(num_units=hidden_size, forget_bias=1.0, state_is_tuple=True)

    # **步骤3：添加 dropout layer, 一般只设置 output_keep_prob
    lstm_cell = tf.contrib.rnn.DropoutWrapper(cell=lstm_cell, input_keep_prob=1.0, output_keep_prob=keep_prob)

    # **步骤4：调用 MultiRNNCell 来实现多层 LSTM
    mlstm_cell = tf.contrib.rnn.MultiRNNCell([lstm_cell] * layer_num, state_is_tuple=True)

    # **步骤5：用全零来初始化state
    init_state = mlstm_cell.zero_state(batch_size, dtype=tf.float32)

    # **步骤6：方法一，调用 dynamic_rnn() 来让我们构建好的网络运行起来
    # ** 当 time_major==False 时， outputs.shape = [batch_size, timestep_size, hidden_size] 
    # ** 所以，可以取 h_state = outputs[:, -1, :] 作为最后输出
    # ** state.shape = [layer_num, 2, batch_size, hidden_size], 
    # ** 或者，可以取 h_state = state[-1][1] 作为最后输出
    # ** 最后输出维度是 [batch_size, hidden_size]
    # outputs, state = tf.nn.dynamic_rnn(mlstm_cell, inputs=X, initial_state=init_state, time_major=False)
    # h_state = outputs[:, -1, :]  # 或者 h_state = state[-1][1]

    # *************** 为了更好的理解 LSTM 工作原理，我们把上面 步骤6 中的函数自己来实现 ***************
    # 通过查看文档你会发现， RNNCell 都提供了一个 __call__()函数（见最后附），我们可以用它来展开实现LSTM按时间步迭代。
    # **步骤6：方法二，按时间步展开计算
    outputs = list()
    state = init_state
    with tf.variable_scope('RNN'):
        for timestep in range(timestep_size):
            if timestep > 0:
                tf.get_variable_scope().reuse_variables()
            # 这里的state保存了每一层 LSTM 的状态
            (cell_output, state) = mlstm_cell(X[:, timestep, :], state)
            outputs.append(cell_output)
    h_state = outputs[-1]
