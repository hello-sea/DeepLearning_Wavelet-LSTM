# 加载 Keras 模型相关的 Python 模块
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop

# 构建 MLP 网络
model = Sequential() 
model.add(Dense(512, input_shape=(784,))) # 全连接层
model.add(Activation('relu')) # ReLU
model.add(Dropout(0.2)) # Dropout
model.add(Dense(512)) # 全连接层
model.add(Activation('relu')) # ReLU
model.add(Dropout(0.2)) # Dropout
model.add(Dense(10)) # 分类层
model.add(Activation('softmax')) # Softmax
model.summary() # 打印模型
model.compile(loss='categorical_crossentropy',
optimizer=RMSprop(),
metrics=['accuracy']) # 生成模型