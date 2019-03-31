import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
import yaml
import yamlordereddictloader

from sklearn.preprocessing import MultiLabelBinarizer


def categorize(words):
    raw_test = [str(words).strip().replace('\n', ' ')]
    predict_input_fn = tf.estimator.inputs.numpy_input_fn({'text': np.array(raw_test).astype(np.str)},
                                                          shuffle=False)
    results = estimator.predict(predict_input_fn)

    arr = []
    for result in results:
        probs = result['probabilities']
        prob = probs.argsort()[::-1]
        for category in prob:
            if probs[category] < 0.7:
                continue

            text_category = encoder.classes_[category]
            arr.append(text_category)

        if len(arr) < 1:
            arr.append(encoder.classes_[prob[0]])

    return arr

#
# def read_data():
#     text = []
#     categories = []
#
#     with open("meeeeeem.yaml") as f:
#         yaml_data = yaml.load(f, Loader=yamlordereddictloader.Loader)
#         for mem in yaml_data:
#             text.append(mem)
#             categories.append(yaml_data[mem])
#
#     return {
#         'text': text,
#         'categories': categories
#     }
#
#
# data = pd.DataFrame(read_data(), columns=['text', 'categories'])
#
# text = data['text']
# categories = data['categories']
#
# encoder = MultiLabelBinarizer()
# encoder.fit_transform(categories)
# train_encoded = encoder.transform(categories)
# num_classes = len(encoder.classes_)
#
# multi_label_head = tf.contrib.estimator.multi_label_head(
#     num_classes,
#     loss_reduction=tf.losses.Reduction.SUM_OVER_BATCH_SIZE
# )
#
# # takes time
# text_embeddings = hub.text_embedding_column(
#     "text",
#     module_spec="https://tfhub.dev/google/universal-sentence-encoder/2",
#     trainable=False
# )
#
# features = {
#     "text": np.array(text).astype(np.str)
# }
# labels = np.array(train_encoded).astype(np.int32)
#
# train_input_fn = tf.estimator.inputs.numpy_input_fn(
#     features,
#     labels,
#     shuffle=True,
#     batch_size=5,
#     num_epochs=500
# )
#
# estimator = tf.estimator.DNNEstimator(
#     head=multi_label_head,
#     hidden_units=[10],
#     feature_columns=[text_embeddings]
# )
#
# estimator.train(input_fn=train_input_fn)
