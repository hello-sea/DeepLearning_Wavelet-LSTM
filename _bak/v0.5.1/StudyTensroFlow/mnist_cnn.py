# 加载 Keras 模型相关的 Python 模块
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
# 构建 CNN 网络

model = Sequential()
model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1],
border_mode='valid',
input_shape=input_shape)) # 卷积层
model.add(Activation('relu')) # ReLU
model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1])) # 卷积层
model.add(Activation('relu')) # ReLU
model.add(MaxPooling2D(pool_size=pool_size)) # Maxpooling
model.add(Dropout(0.25)) # Dropout
model.add(Flatten()) # 将响应转换为一维向量
model.add(Dense(128)) # 全连接层
model.add(Activation('relu')) # ReLU
model.add(Dropout(0.5)) # Dropout
model.add(Dense(nb_classes)) # 分类层
model.add(Activation('softmax')) # Softmax

model.compile(loss='categorical_crossentropy',
optimizer='adadelta',
metrics=['accuracy']) # 生成模型