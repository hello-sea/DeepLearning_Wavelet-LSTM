
from tensorflow.examples.tutorials.mnist import input_data


if __name__ == "__main__":  


    
    batch_size = 128
    
    # this is data
    mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
    batch_xs, batch_ys = mnist.train.next_batch(batch_size)

    print(batch_xs.shape) # (128, 784)
    print('done!')
    print(batch_ys.shape) # (128, 784)
    print('done!')
    print(batch_ys)


