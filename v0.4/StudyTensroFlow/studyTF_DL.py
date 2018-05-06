# -*- coding: utf-8 -*-

import tensorflow as tf

'''
常用超参数
    - steps：是指训练迭代的总次数。一步计算一批样本产生的损失，然后使用该值修改模型的权重一次。
    - batch size：是指单步的样本数量（随机选择）。例如，SGD 的批量大小为 1
方便变量
    - periods：控制报告的粒度。
      例如，如果 periods 设为 7 且 steps 设为 70，则练习将每 10 步（或 7 次）输出一次损失值。
      与超参数不同，我们不希望您修改 periods 的值。请注意，修改 periods 不会更改您的模型所学习的内容。
'''
# Set up a linear classifier.
# classifier = tf.estimator.LinearClassifier()

# Train the model on some example data.
# classifier.train(input_fn=train_input_fn, steps=2000)

# Use it to predict.
# predictions = classifier.predict(input_fn=predict_input_fn)






