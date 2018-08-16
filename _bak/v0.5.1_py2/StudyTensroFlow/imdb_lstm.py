from keras.models import Sequential
from keras.layers import Dense, Activation, Embedding
from keras.layers import LSTM
# 构建 LSTM 模型
model = Sequential()
model.add(Embedding(max_features, 128, dropout=0.2)) # 词嵌入
model.add(LSTM(128, dropout_W=0.2, dropout_U=0.2)) # LSTM 层
model.add(Dense(1)) # 二分类层
model.add(Activation('sigmoid')) # Sigmoid 
model.summary() # 打印模型
model.compile(loss='binary_crossentropy',
optimizer='adam',
metrics=['accuracy']) # 生成模型