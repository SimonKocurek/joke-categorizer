import os
import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
import json
import pickle
import urllib

from sklearn.preprocessing import MultiLabelBinarizer


def categorize(words):
    # nn stuff
    return ['politics', 'captain']


data = pd.read_csv('movies_metadata.csv')
data.head()

descriptions = data['overview']
genres = data['genres']

train_size = int(len(descriptions) * .9)

train_descriptions = descriptions[:train_size].astype('str')
train_genres = genres[:train_size]

test_descriptions = descriptions[train_size:].astype('str')
test_genres = genres[train_size:]

encoder = MultiLabelBinarizer()
encoder.fit_transform(train_genres)
train_encoded = encoder.transform(train_genres)
test_encoded = encoder.transform(test_genres)
num_classes = len(encoder.classes_)

multi_label_head = tf.contrib.estimator.multi_label_head(
    num_classes,
    loss_reduction=tf.losses.Reduction.SUM_OVER_BATCH_SIZE
)

# takes time
description_embeddings = hub.text_embedding_column(
    "descriptions",
    module_spec="https://tfhub.dev/google/universal-sentence-encoder/2",
    trainable=False
)

# Format our data for the numpy_input_fn
features = {
    "descriptions": np.array(train_descriptions).astype(np.str)
}
labels = np.array(train_encoded).astype(np.int32)

train_input_fn = tf.estimator.inputs.numpy_input_fn(
    features,
    labels,
    shuffle=False,
    batch_size=32,
    num_epochs=20
)

estimator = tf.estimator.DNNEstimator(
    head=multi_label_head,
    hidden_units=[64, 10],
    feature_columns=[description_embeddings]
)

estimator.train(input_fn=train_input_fn)

#############################

eval_input_fn = tf.estimator.inputs.numpy_input_fn({"descriptions": np.array(test_descriptions).astype(np.str)},
                                                   test_encoded.astype(np.int32), shuffle=False)
estimator.evaluate(input_fn=eval_input_fn)

raw_test = [
    "An examination of our dietary choices and the food we put in our bodies. Based on Jonathan Safran Foer's memoir.",
    # Documentary
    "A teenager tries to survive the last week of her disastrous eighth-grade year before leaving to start high school.",
    # Comedy
    "Ethan Hunt and his IMF team, along with some familiar allies, race against time after a mission gone wrong."
    # Action, Adventure
]

predict_input_fn = tf.estimator.inputs.numpy_input_fn({"descriptions": np.array(raw_test).astype(np.str)},
                                                      shuffle=False)

results = estimator.predict(predict_input_fn)

for movie_genres in results:
    top_2 = movie_genres['probabilities'].argsort()[-2:][::-1]
    for genre in top_2:
        text_genre = encoder.classes_[genre]
        print(text_genre + ': ' + str(round(movie_genres['probabilities'][genre] * 100, 2)) + '%')
