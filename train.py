import numpy as np
import keras

inputs = np.loadtxt("input_cases")
expected_outputs = keras.activations.softmax(np.loadtxt("expected_output"))

model = keras.models.Sequential([
    keras.layers.Dense(64, activation=keras.activations.sigmoid),
    keras.layers.Dense(9, activation=keras.activations.sigmoid),
])

model.compile(
    optimizer = keras.optimizers.Adam(learning_rate = 0.0001), #change to adam, worked much better
    loss = keras.losses.mean_squared_error,
    metrics=[keras.metrics.MeanAbsolutePercentageError()],
)

model.fit(inputs, expected_outputs, epochs = 5000, verbose = 1)
model.save("tic_tac_toe.keras", overwrite = False)