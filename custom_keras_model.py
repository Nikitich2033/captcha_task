import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Load and preprocess your data
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    'sorted_training/train',
    image_size=(224, 224),
    batch_size=32)

test_ds = tf.keras.preprocessing.image_dataset_from_directory(
    'sorted_training/test',
    image_size=(224, 224),
    batch_size=32)

# Build your model
model = keras.Sequential([
    layers.experimental.preprocessing.Rescaling(1./255),
    layers.Conv2D(32, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(32, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(10)
])

# Compile your model
model.compile(
    optimizer='adam',
    loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy'])

# Train your model
model.fit(train_ds, validation_data=test_ds, epochs=5)

# Evaluate your model
loss, accuracy = model.evaluate(test_ds)
print(f'Test accuracy: {accuracy}')
