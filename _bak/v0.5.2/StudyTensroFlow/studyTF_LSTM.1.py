import warnings
warnings.filterwarnings('ignore')  # 不打印 warning 

import tensorflow as tf
import numpy as np



# 用tensorflow 导入数据
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets('../data/MNIST_data', one_hot=True) 

# 看看咱们样本的数量
print(mnist.test.labels.shape)
print(mnist.train.labels.shape)


# # 设置GPU按需增长
# config = tf.ConfigProto()
# config.gpu_options.allow_growth = True
# sess = tf.Session(config=config)
sess = tf.Session()

'''
一、首先设置好模型用到的各个超参数
'''

lr  =  1e-3
input_sizeinput_s  = 28      # 每个时刻的输入特征是28维的，就是每个时刻输入一行，一行有 28 个像素
timestep_size = 28   # 时序持续长度为28，即每做一次预测，需要先输入28行
hidden_size = 256    # 隐含层的数量
layer_num = 2        # LSTM layer 的层数
class_num = 10       # 最后输出分类类别数量，如果是回归预测的话应该是 1
cell_type = "lstm"   # lstm 或者 block_lstm

X_input = tf.placeholder(tf.float32, [None, 784])
y_input = tf.placeholder(tf.float32, [None, class_num])
# 在训练和测试的时候，我们想用不同的 batch_size.所以采用占位符的方式
batch_size = tf.placeholder(tf.int32, [])  # 注意类型必须为 tf.int32, batch_size = 128
keep_prob = tf.placeholder(tf.float32, [])




'''
二、开始搭建 LSTM 模型，其实普通 RNNs 模型也一样
'''
# 把784个点的字符信息还原成 28 * 28 的图片
# 下面几个步骤是实现 RNN / LSTM 的关键

# **步骤1：RNN 的输入shape = (batch_size, timestep_size, input_size) 
X = tf.reshape(X_input, [-1, 28, 28])

# ** 步骤2：创建 lstm 结构
def lstm_cell(cell_type, num_nodes, keep_prob):
    assert(cell_type in ["lstm", "block_lstm"], "Wrong cell type.")
    if cell_type == "lstm":
        cell = tf.contrib.rnn.BasicLSTMCell(num_nodes)
    else:
        cell = tf.contrib.rnn.LSTMBlockCell(num_nodes)
    cell = tf.contrib.rnn.DropoutWrapper(cell, output_keep_prob=keep_prob)
    return cell

mlstm_cell = tf.contrib.rnn.MultiRNNCell([lstm_cell(cell_type, hidden_size, keep_prob) for _ in range(layer_num)], state_is_tuple = True)

# **步骤3：用全零来初始化state
init_state = mlstm_cell.zero_state(batch_size, dtype=tf.float32)

# **步骤4：方法一，调用 dynamic_rnn() 来让我们构建好的网络运行起来
# ** 当 time_major==False 时， outputs.shape = [batch_size, timestep_size, hidden_size] 
# ** 所以，可以取 h_state = outputs[:, -1, :] 作为最后输出
# ** state.shape = [layer_num, 2, batch_size, hidden_size], 
# ** 或者，可以取 h_state = state[-1][1] 作为最后输出
# ** 最后输出维度是 [batch_size, hidden_size]
outputs, state = tf.nn.dynamic_rnn(mlstm_cell, inputs=X, initial_state=init_state, time_major=False)
h_state = state[-1][1]

# # *************** 为了更好的理解 LSTM 工作原理，我们把上面 步骤4 中的函数自己来实现 ***************
# # 通过查看文档你会发现， RNNCell 都提供了一个 __call__()函数，我们可以用它来展开实现LSTM按时间步迭代。
# # **步骤4：方法二，按时间步展开计算
# outputs = list()
# state = init_state
# with tf.variable_scope('RNN'):
#     for timestep in range(timestep_size):
#         (cell_output, state) = mlstm_cell(X[:, timestep, :],state)
#         outputs.append(cell_output)
# h_state = outputs[-1]



'''
三、最后设置 loss function 和 优化器，展开训练并完成测试
'''
############################################################################
# 以下部分其实和之前写的多层 CNNs 来实现 MNIST 分类是一样的。
# 只是在测试的时候也要设置一样的 batch_size.

# 上面 LSTM 部分的输出会是一个 [hidden_size] 的tensor，我们要分类的话，还需要接一个 softmax 层
# 首先定义 softmax 的连接权重矩阵和偏置

import time

# 开始训练和测试
W = tf.Variable(tf.truncated_normal([hidden_size, class_num], stddev=0.1), dtype=tf.float32)
bias = tf.Variable(tf.constant(0.1,shape=[class_num]), dtype=tf.float32)
y_pre = tf.nn.softmax(tf.matmul(h_state, W) + bias)


# 损失函数
cross_entropy = -tf.reduce_mean(y_input * tf.log(y_pre))
train_op = tf.train.AdamOptimizer(lr).minimize(cross_entropy)

# 损失函数
correct_prediction = tf.equal(tf.argmax(y_pre,1), tf.argmax(y_input,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))


''' 训练 **************************************************** '''
sess.run(tf.global_variables_initializer())
time0 = time.time()
for i in range(5000):
    _batch_size=100
    X_batch, y_batch = mnist.train.next_batch(batch_size=_batch_size)
    cost, acc,  _ = sess.run([cross_entropy, accuracy, train_op], feed_dict={X_input: X_batch, y_input: y_batch, keep_prob: 0.5, batch_size: _batch_size})
    if (i+1) % 500 == 0:
        # 分 100 个batch 迭代
        test_acc = 0.0
        test_cost = 0.0
        N = 100
        for j in range(N):
            X_batch, y_batch = mnist.test.next_batch(batch_size=_batch_size)
            _cost, _acc = sess.run([cross_entropy, accuracy], feed_dict={X_input: X_batch, y_input: y_batch, keep_prob: 1.0, batch_size: _batch_size})
            test_acc += _acc
            test_cost += _cost
        print("step {}, train cost={:.6f}, acc={:.6f}; test cost={:.6f}, acc={:.6f}; pass {}s".format(i+1, cost, acc, test_cost/N, test_acc/N, time.time() - time0))
        time0 = time.time()


'''
四、可视化看看 LSTM 的是怎么做分类的
'''

# 手写的结果 shape
_batch_size = 5
X_batch, y_batch = mnist.test.next_batch(_batch_size)
print(X_batch.shape, y_batch.shape)
_outputs, _state = np.array(sess.run([outputs, state],feed_dict={
            X_input: X_batch, y_input: y_batch, keep_prob: 1.0, batch_size: _batch_size}))
print('_outputs.shape =', np.asarray(_outputs).shape)
print('arr_state.shape =', np.asarray(_state).shape)
# 可见 outputs.shape = [ batch_size, timestep_size, hidden_size]
# state.shape = [layer_num, 2, batch_size, hidden_size]


import matplotlib.pyplot as plt

print(mnist.train.labels[10:20])
X3 = mnist.train.images[10]
img3 = X3.reshape([28, 28])
plt.imshow(img3, cmap='gray')
plt.show()



X3.shape = [-1, 784]
y_batch = mnist.train.labels[0]
y_batch.shape = [-1, class_num]

X3_outputs = np.array(sess.run(outputs, feed_dict={
            X_input: X3 , y_input: y_batch, keep_prob: 1.0, batch_size: 1}))
print(X3_outputs.shape)
X3_outputs.shape = [28, hidden_size]
print(X3_outputs.shape)


h_W, h_bias = sess.run([W, bias], feed_dict={
            X_input:X3, y_input: y_batch, keep_prob: 1.0, batch_size: 1})
h_bias = h_bias.reshape([-1, 10])

bar_index = range(class_num)
for i in range(X3_outputs.shape[0]):
    plt.subplot(7, 4, i+1)
    X3_h_shate = X3_outputs[i, :].reshape([-1, hidden_size])
    pro = sess.run(tf.nn.softmax(tf.matmul(X3_h_shate, h_W) + h_bias))
    plt.bar(bar_index, pro[0], width=0.2 , align='center')
    plt.axis('off')
plt.show()

