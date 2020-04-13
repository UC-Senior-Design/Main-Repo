import tensorflow as tf
import pandas as pd;
import code
from sklearn.model_selection import train_test_split

LABEL_COLUMN = 'robx'
data_file_path = 'cleaned.csv'
drone_path = 'drone_cleaned.csv'

def split_df(df):
  data = df[['cam0x','cam0y','cam1x','cam1y','cam3x','camy3']].to_numpy()
  label = df[['robx', 'roby', 'robz']].to_numpy()
  return data, label

def load_csv(path):
  df = pd.read_csv(path).astype('float64')
  train, test = train_test_split(df, test_size=0.2)
  train_data, train_label = split_df(train)
  test_data, test_label = split_df(test)
  return train_data, train_label, test_data, test_label

def load_drone_csv(path):
  df = pd.read_csv(path)
  snap_indices = df[['snap_index']].astype('int64')
  data = df[['cam0x','cam0y','cam1x','cam1y','cam3x','camy3']].astype('float64')
  return snap_indices, data


def loss(target_y, predicted_y):
  return tf.math.sqrt(tf.reduce_sum(tf.square(target_y - predicted_y)))

def get_model():
  model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(32),
    tf.keras.layers.Dense(32),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(3)
  ])
  loss_fn = tf.keras.losses.MeanSquaredError()
  model.compile(optimizer='rmsprop', loss=loss)
  return model

train_data, train_label, test_data, test_label = load_csv(data_file_path)

model = get_model()
model.fit(train_data, train_label, epochs=70)
model.evaluate(test_data, test_label, verbose=2)

snap_indices, drone_data = load_drone_csv(drone_path)
result = model.predict(drone_data.to_numpy())

# Add snap indices back to dataframe and write to file
result_df = pd.DataFrame(result, columns=['robx', 'roby', 'robz'])
merged = drone_data.merge(result_df, left_index=True, right_index=True)
merged.insert(0, "snap_index", snap_indices)
merged.to_csv("result.csv", index=False)