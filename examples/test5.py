import numpy as np
import tensorflow as tf
import os
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Init keras
keras = tf.keras
K = keras.backend
KL = keras.layers
KO = keras.optimizers
KD = keras.datasets
KU = keras.utils
Lambda, Input, Flatten, Dense = KL.Lambda, KL.Input, KL.Flatten, KL.Dense

Adam = KO.Adam
Model = keras.Model
mnist = KD.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Нормализация входных данных
x_train = x_train / 255
x_test = x_test / 255

y_train_cat = KU.to_categorical(y_train, 10)
y_test_cat = KU.to_categorical(y_test, 10)

plt.figure(figsize=(10, 5))
for i in range(25):
    plt.subplot(5, 5, i + 1)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(x_train[i])

plt.show()

model = keras.Sequential([
    Flatten(input_shape=(28, 28, 1)),
    Dense(128, activation='relu'),
    Dense(10, activation='softmax'),
])

print(model.summary())

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'],
              )

model.fit(x_train, y_train_cat, batch_size=32, epochs=5, validation_split=0.2)


n = 120
x = np.expand_dims(x_test[n], axis=0)
res = model.predict(x)
print(res)
print(f"Распознанная цифра: {np.argmax(res)}")

plt.imshow(x_test[n])
plt.show()
