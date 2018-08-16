
from __future__ import print_function

import tensorflow as tf
from tensorflow.contrib import rnn
import numpy as np
import matplotlib.pyplot as plt
import pickle as pickle     # python pkl 文件读写

from tensorflow_LSTMs import MyNetworks

def MyTrain():
    train_data = np.array(pickle.load(open('tf_model_lstm/train_seg_data.plk', 'rb')) )
    train_labels = np.array(pickle.load(open('tf_model_lstm/train_seg_labels.plk', 'rb')) )

    print( type(train_data) )
    print( train_data.shape )
    # ndarray
    
    ''' ********************************************************************************** '''
    batch_size = len(train_data)
    # Training Parameters:
    learning_rate = 0.05  # 0.1 , 0.001
    training_steps = 1  # 200 , 400
    display_step = 50

    # Network Parameters
    num_input = 1
    timesteps = 83 # timesteps
    num_hidden = 200 # hidden layer num of features
    num_classes = 4 # MNIST total classes (1-4 digits)
    
    # 定义神经网络
    train_op, loss_op, prediction, accuracy, X, Y = MyNetworks(learning_rate, num_input, timesteps, num_hidden, num_classes)


    # 声明tf.train.Saver类用于保存/加载模型
    saver = tf.train.Saver() 

    with tf.Session() as sess:

        # Initialize the variables (i.e. assign their default value)
        # 初始化变量（即分配它们的默认值）
        init = tf.global_variables_initializer()
    
        # Run the initializer
        # 运行初始化程序
        sess.run(init)

        # Start training
        # 开始训练
        for step in range(1, training_steps+1):
            # batch_x, batch_y = mnist.train.next_batch(batch_size)
            batch_x = train_data
            batch_y = train_labels

            batch_x = batch_x.reshape((batch_size, timesteps, num_input))
            # Run optimization op (backprop)  
            # 运行优化操作（backprop）
            sess.run(train_op, feed_dict={X: batch_x, Y: batch_y})
            if step % display_step == 0 or step == 1:
                # Calculate batch loss and accuracy 
                # 计算批次损失和准确性
                loss, acc = sess.run([loss_op, accuracy], feed_dict={X: batch_x,
                                                                    Y: batch_y})
                print("Step " + str(step) + ", Minibatch Loss= " + \
                    "{:.4f}".format(loss) + ", Training Accuracy= " + \
                    "{:.3f}".format(acc))

        print("Optimization Finished(优化完成)!")

        # 保存训练的模型
        saver_path = saver.save(sess, "tf_model_lstm/model.ckpt")  # 将模型保存到save/model.ckpt文件
        print("Model saved in file:", saver_path)

        # 测试集正确率
        print("Testing Accuracy(测试集正确率):", \
            sess.run(accuracy, feed_dict={X: batch_x, Y: batch_y}))


        # 分类
        out = []
        for i in range(batch_size):
            test_data = train_data[i]
            # test_label = train_labels[i]

            test_data = test_data.reshape((1, timesteps, num_input))

            # print(test_data.shape, test_label)

            # print("分类:", sess.run(prediction, feed_dict={X: test_data}))
            out_tag = sess.run(prediction, feed_dict={X: test_data})
            # 获取矩阵值(概率)最大下标
            j = np.unravel_index( out_tag[0].argmax(), out_tag[0].shape )
            # print(j)
            j = j[0]+1
            out.append(j)
        
        plt.plot( out )
        plt.show() 



if __name__=='__main__':
    MyTrain()


