import numpy as np
import tensorflow as tf
import os
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'


def test_grad():
    keras = tf.keras
    K = keras.backend
    KL = keras.layers
    Lambda, Input, Flatten, Dense = KL.Lambda, KL.Input, KL.Flatten, KL.Dense
    KO = keras.optimizers
    Adam = KO.Adam
    Model = keras.Model

    c = np.array([-40, -10, 0, 8, 15, 22, 38])
    f = np.array([-40, 14, 32, 46, 59, 72, 100])

    model = keras.Sequential()

    model.add(Input(shape=(4)))
    model.add(Dense(units=1, activation='linear'))
    model.compile(loss='mean_squared_error', optimizer=Adam(0.1))

    history = model.fit(c, f, epochs=500, verbose=False)

    # plt.plot(history.history['loss'])
    # plt.grid(True)
    # plt.show()

    prediction = model.predict(np.array([100, 34, 28]))
    print(prediction)

    print(model.get_weights())
