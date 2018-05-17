
"""
This code is a modified version of the code from this link:
https://github.com/aymericdamien/TensorFlow-Examples/blob/master/examples/3_NeuralNetworks/recurrent_network.py
His code is a very good one for RNN beginners. Feel free to check it out.
"""
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data


n_inputs = 28   # MNIST data input (img shape: 28*28)
n_steps = 28    # time steps
# n_inputs = 1   # data input (img shape: 28*28)
# n_steps = 256   # time steps
n_hidden_units = 128   # neurons in hidden layer
batch_size = 128

def RNN(X, weights, biases):
    # hidden layer for input to cell
    ########################################

    # transpose the inputs shape from
    # X ==> (128 batch * 28 steps, 28 inputs)
    X = tf.reshape(X, [-1, n_inputs])

    # into hidden
    # X_in = (128 batch * 28 steps, 128 hidden)
    X_in = tf.matmul(X, weights['in']) + biases['in']
    # X_in ==> (128 batch, 28 steps, 128 hidden)
    X_in = tf.reshape(X_in, [-1, n_steps, n_hidden_units])

    # cell
    ##########################################

    cell = tf.contrib.rnn.BasicLSTMCell(n_hidden_units)    
    # lstm cell is divided into two parts (c_state, h_state)
    init_state = cell.zero_state(batch_size, dtype=tf.float32)

    # You have 2 options for following step.
    # 1: tf.nn.rnn(cell, inputs);
    # 2: tf.nn.dynamic_rnn(cell, inputs).
    # If use option 1, you have to modified the shape of X_in, go and check out this:
    # https://github.com/aymericdamien/TensorFlow-Examples/blob/master/examples/3_NeuralNetworks/recurrent_network.py
    # In here, we go for option 2.
    # dynamic_rnn receive Tensor (batch, steps, inputs) or (steps, batch, inputs) as X_in.
    # Make sure the time_major is changed accordingly.
    outputs, final_state = tf.nn.dynamic_rnn(cell, X_in, initial_state=init_state, time_major=False)

    # hidden layer for output as the final results
    #############################################
    # results = tf.matmul(final_state[1], weights['out']) + biases['out']

    # # or
    # unpack to list [(batch, outputs)..] * steps
    # if int((tf.__version__).split('.')[1]) < 12 and int((tf.__version__).split('.')[0]) < 1:
    #     outputs = tf.unpack(tf.transpose(outputs, [1, 0, 2]))    # states is the last outputs
    # else:
    #     outputs = tf.unstack(tf.transpose(outputs, [1,0,2]))
    outputs = tf.unstack(tf.transpose(outputs, [1,0,2]))    
    results = tf.matmul(outputs[-1], weights['out']) + biases['out']    # shape = (128, 10)

    return results

def main():
    # set random seed for comparing the two result calculations
    tf.set_random_seed(1)

    # this is data
    mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

    # hyperparameters
    lr = 0.001
    training_iters = 100000

    n_classes = 10      # MNIST classes (0-9 digits)

    # tf Graph input
    x = tf.placeholder(tf.float32, [None, n_steps, n_inputs])
    y = tf.placeholder(tf.float32, [None, n_classes])

    # Define weights
    weights = {
        # (28, 128)
        'in': tf.Variable(tf.random_normal([n_inputs, n_hidden_units])),
        # (128, 10)
        'out': tf.Variable(tf.random_normal([n_hidden_units, n_classes]))
    }
    biases = {
        # (128, )
        'in': tf.Variable(tf.constant(0.1, shape=[n_hidden_units, ])),
        # (10, )
        'out': tf.Variable(tf.constant(0.1, shape=[n_classes, ]))
    }

    # 损失函数
    pred = RNN(x, weights, biases)
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
    train_op = tf.train.AdamOptimizer(lr).minimize(cost) # 定义AdamOptimizer对象用于求解模型
    

    # 损失函数
    correct_pred = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    ''' 训练 **************************************************** '''
    
    with tf.Session() as sess:
        # 初始化模型
        init = tf.global_variables_initializer()
        sess.run(init)
        
        step = 0
        while step * batch_size < training_iters:
            batch_xs, batch_ys = mnist.train.next_batch(batch_size)
            batch_xs = batch_xs.reshape([batch_size, n_steps, n_inputs])

            sess.run([train_op], feed_dict={  # feed_dict 字典填充
                x: batch_xs,
                y: batch_ys,
            })

            if step % 20 == 0:
                print(sess.run(accuracy, feed_dict={
                x: batch_xs,
                y: batch_ys,
                }))
            step += 1
    '''**************************************************** '''
    # 评价



    '''**************************************************** '''
    # 分类

    h_W, h_bias = sess.run([pred], feed_dict={
                x:X3, y_input: y_batch, keep_prob: 1.0, batch_size: 1})
    h_bias = h_bias.reshape([-1, 10])

    bar_index = range(class_num)
    for i in range(X3_outputs.shape[0]):
        plt.subplot(7, 4, i+1)
        X3_h_shate = X3_outputs[i, :].reshape([-1, hidden_size])
        pro = sess.run(tf.nn.softmax(tf.matmul(X3_h_shate, h_W) + h_bias))
        plt.bar(bar_index, pro[0], width=0.2 , align='center')
        plt.axis('off')
    plt.show()

if __name__ == "__main__":   
    main()

