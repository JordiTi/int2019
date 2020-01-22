# Trains algorithms

from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.ensemble import RandomForestClassifier
import tensorflow as tf
from tensorflow import keras
import numpy as np
from numpy import array


# Trains random forest classifier
def trainRF(train_data, test_data, train_labels, test_labels, objectid,
            label, rebinning):

    # Initialize and train random forest
    classifier = RandomForestClassifier(n_estimators=200, min_samples_leaf=20,
                                        min_samples_split=50, max_features=30)
    classifier.fit(train_data, train_labels)
    y_pred_per_obs = classifier.predict_proba(test_data)
    accuracylist = y_pred_per_obs[:, int(label)]
    y_pred_general = classifier.predict(test_data)

    # Save results
    with open('./trainresults/RF' + str(rebinning) + 'cut3.txt', 'a') as results:
        results.write(str(objectid) + '\n\n' + str(confusion_matrix(test_labels, y_pred_general)) + '\n\n'
                      + str(accuracy_score(test_labels, y_pred_general)) + '\n'
                      + '_______________________________________' + '\n\n'
                      )
    return accuracylist


# Train neural network
def trainNN(train_data, test_data, train_labels, test_labels, objectid, label, rebinning, nodes):

    # Format training data
    train_data = array(train_data)
    test_data = array(test_data)
    datamean = np.append(train_data, test_data).mean()
    datastd = np.append(train_data, test_data).std()

    train_data = train_data.reshape([-1, nodes, 1])
    test_data = test_data.reshape([-1, nodes, 1])

    train_data = (train_data - datamean) / datastd
    test_data = (test_data - datamean) / datastd

    train_labels = keras.utils.to_categorical(train_labels, num_classes=2)

    # Initialize neural network
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv1D(input_shape=(nodes, 1), filters=128,
                               kernel_size=32,
                               strides=2, use_bias=True,
                               activation=tf.nn.relu),
        tf.keras.layers.Dropout(rate=0.8),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation=tf.nn.relu),
        tf.keras.layers.Dense(2, activation=tf.nn.softmax)
    ])

    adam = keras.optimizers.Adam(lr=0.0005, beta_1=0.9, beta_2=0.999,
                                 epsilon=1e-08)
    # Compile and train netowrk
    model.compile(optimizer=adam,
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    history = model.fit(train_data, train_labels, epochs=150, batch_size=64,
                        validation_split=0.05, shuffle=True)
    prediction = model.predict(test_data, batch_size=1)
    one_hot_test_labels = keras.utils.to_categorical(test_labels, num_classes=2)
    accuracy = model.evaluate(test_data, one_hot_test_labels, batch_size=1)
    accuracylist = prediction[:, int(label)]
    y_pred = model.predict_classes(test_data)

    con_mat = tf.math.confusion_matrix(labels=test_labels, predictions=y_pred)
    with tf.compat.v1.Session():
        print('Confusion Matrix: \n\n', tf.Tensor.eval(con_mat, feed_dict=None,
                                                       session=None))
    # Save data
    with open('./trainresults/NN' + str(rebinning) + '2.txt', 'a') as results:
        results.write(str(objectid) + '\n\n' + str(confusion_matrix(test_labels,
            y_pred)) + '\n\n' +
            str(accuracy) + '\n' + '________________________\n')

    return accuracylist

