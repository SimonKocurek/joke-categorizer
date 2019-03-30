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
            text_category = encoder.classes_[category]
            arr.append(f'''{text_category}: {str(round(probs[category] * 100, 2))}%''')

    print(arr)
    return arr


def read_data():
    text = []
    categories = []

    with open("meeeeeem.yaml") as f:
        yaml_data = yaml.load(f, Loader=yamlordereddictloader.Loader)
        for mem in yaml_data:
            text.append(mem)
            categories.append(yaml_data[mem])

    return {
        'text': text,
        'categories': categories
    }


data = pd.DataFrame(read_data(), columns=['text', 'categories'])

text = data['text']
categories = data['categories']

encoder = MultiLabelBinarizer()
encoder.fit_transform(categories)
train_encoded = encoder.transform(categories)
num_classes = len(encoder.classes_)

multi_label_head = tf.contrib.estimator.multi_label_head(
    num_classes,
    loss_reduction=tf.losses.Reduction.SUM_OVER_BATCH_SIZE
)

# takes time
text_embeddings = hub.text_embedding_column(
    "text",
    module_spec="https://tfhub.dev/google/universal-sentence-encoder/2",
    trainable=False
)

# Format our data for the numpy_input_fn
features = {
    "text": np.array(text).astype(np.str)
}
labels = np.array(train_encoded).astype(np.int32)

train_input_fn = tf.estimator.inputs.numpy_input_fn(
    features,
    labels,
    shuffle=False,
    batch_size=32,
    num_epochs=100
)

estimator = tf.estimator.DNNEstimator(
    head=multi_label_head,
    hidden_units=[10],
    feature_columns=[text_embeddings]
)

estimator.train(input_fn=train_input_fn)
categorize('We must do the homework, but we hates it!!!:')