
from __future__ import print_function

import random
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
    batch_num = len(train_data)
    batch_size = len(train_data[0])
    # Training Parameters:
    learning_rate = 0.02  # 0.1; 0.001; 0.02
    training_steps = 1500  # 200 , 400 , 500
    display_step = 10

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
            a  = random.randint(0, batch_num-1)
            batch_x = train_data[a]
            batch_y = train_labels[a]

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

            # 保存训练的模型
            the_number = 200
            if step == the_number:
                saver_path = saver.save(sess, "tf_model_lstm/model_"+ str(the_number) +".ckpt")  # 将模型保存到save/model.ckpt文件
                print("Model saved in file:", saver_path)
            
            the_number = 500
            if step == the_number:
                saver_path = saver.save(sess, "tf_model_lstm/model_"+ str(the_number) +".ckpt")  # 将模型保存到save/model.ckpt文件
                print("Model saved in file:", saver_path)
            
            the_number = 1000
            if step == the_number:
                saver_path = saver.save(sess, "tf_model_lstm/model_"+ str(the_number) +".ckpt")  # 将模型保存到save/model.ckpt文件
                print("Model saved in file:", saver_path)

            the_number = 1500
            if step == the_number:
                saver_path = saver.save(sess, "tf_model_lstm/model_"+ str(the_number) +".ckpt")  # 将模型保存到save/model.ckpt文件
                print("Model saved in file:", saver_path)        

        print("Optimization Finished(优化完成)!")

        # 保存训练的模型
        saver_path = saver.save(sess, "tf_model_lstm/model.ckpt")  # 将模型保存到save/model.ckpt文件
        print("Model saved in file:", saver_path)

        # 测试集正确率
        print("Testing Accuracy(测试集正确率):", \
            sess.run(accuracy, feed_dict={X: batch_x, Y: batch_y}))

import datetime

if __name__=='__main__':
    startTime = datetime.datetime.now()
    
    MyTrain()
    
    endTime = datetime.datetime.now()
    print('running time:', (endTime - startTime).seconds)




