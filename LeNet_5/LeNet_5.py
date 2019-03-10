from tensorflow.examples.tutorials.mnist import input_data
import numpy as np
import os
import tensorflow as tf
from tensorflow.contrib.layers import flatten

image_size = 28
num_labels = 10
num_channels = 1
EPOCHS = 10
BATCH_SIZE = 128

def LeNet(x):
    # Hyperparameters
    mu = 0
    sigma = 0.1
    layer_depth = {
        'layer_1': 6,
        'layer_2': 16,
        'layer_3': 120,
        'layer_f1': 84
    }
    # TODO: Layer 1: Convolutional. Input = 1@32x32. Output = 6@28x28.
    conv1_w = tf.Variable(tf.truncated_normal(shape=[5, 5, 1, 6], mean=mu, stddev=sigma))
    conv1_b = tf.Variable(tf.zeros(6))
    conv1 = tf.nn.conv2d(x, conv1_w, strides=[1, 1, 1, 1], padding='VALID') + conv1_b
    # TODO: Activation.
    conv1 = tf.nn.relu(conv1)

    # TODO: Pooling(Subsampling). Input = 6@28x28. Output = 6@14x14.
    pool_1 = tf.nn.max_pool(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='VALID')

    # TODO: Layer 2: Convolutional. Input = 6@14x14. Output = 16@10x10.
    conv2_w = tf.Variable(tf.truncated_normal(shape=[5, 5, 6, 16], mean=mu, stddev=sigma))
    conv2_b = tf.Variable(tf.zeros(16))
    conv2 = tf.nn.conv2d(pool_1, conv2_w, strides=[1, 1, 1, 1], padding='VALID') + conv2_b
    # TODO: Activation.
    conv2 = tf.nn.relu(conv2)

    # TODO: Pooling. Input = 16@10x10. Output = 16@5x5.
    pool_2 = tf.nn.max_pool(conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='VALID')

    # TODO: Flatten. Input = 16@5x5. Output = 400 == 16*5*5
    fc1 = flatten(pool_2)

    # TODO: Layer 3: Fully Connected. Input = 400. Output = 120.
    fc1_w = tf.Variable(tf.truncated_normal(shape=(400, 120), mean=mu, stddev=sigma))
    fc1_b = tf.Variable(tf.zeros(120))
    fc1 = tf.matmul(fc1, fc1_w) + fc1_b # basic multiple

    # TODO: Activation.
    fc1 = tf.nn.relu(fc1)

    # TODO: Layer 4: Fully Connected. Input = 120. Output = 84.
    fc2_w = tf.Variable(tf.truncated_normal(shape=(120, 84), mean=mu, stddev=sigma))
    fc2_b = tf.Variable(tf.zeros(84))
    fc2 = tf.matmul(fc1, fc2_w) + fc2_b
    # TODO: Activation.
    fc2 = tf.nn.relu(fc2)

    # TODO: Layer 5: Fully Connected. Input = 84. Output = 10.
    fc3_w = tf.Variable(tf.truncated_normal(shape=(84, 10), mean=mu, stddev=sigma))
    fc3_b = tf.Variable(tf.zeros(10))
    logits = tf.matmul(fc2, fc3_w) + fc3_b

    return logits

def reformat(dataset, labels):
 dataset = dataset.reshape((-1, image_size, image_size, num_channels)).astype(np.float32)
 return dataset, labels

mnist = input_data.read_data_sets("MNIST_data/")
X_train, y_train = mnist.train.images, mnist.train.labels
X_train, y_train = reformat(X_train, y_train)
X_validation, y_validation = mnist.validation.images, mnist.validation.labels
X_validation, y_validation = reformat(X_validation, y_validation)
X_test, y_test = mnist.test.images, mnist.test.labels
X_test, y_test=reformat(X_test, y_test)

assert(len(X_train) == len(y_train))
assert(len(X_validation) == len(y_validation))
assert(len(X_test) == len(y_test))

print()
print("Image Shape: {}".format(X_train[0].shape))
print()
print("Training Set:   {} samples".format(len(X_train)))
print("Validation Set: {} samples".format(len(X_validation)))
print("Test Set:       {} samples".format(len(X_test)))

# Pad images with 0s
X_train = np.pad(X_train, ((0, 0), (2, 2), (2, 2), (0, 0)), 'constant')
X_validation = np.pad(X_validation, ((0, 0), (2, 2), (2, 2), (0, 0)), 'constant')
X_test = np.pad(X_test, ((0, 0), (2, 2), (2, 2), (0, 0)), 'constant')

print("Updated Image Shape: {}".format(X_train[0].shape))

x = tf.placeholder(tf.float32, (None, 32, 32, 1))
y = tf.placeholder(tf.int32, (None))
one_hot_y = tf.one_hot(y, 10)

rate = 0.001

logits = LeNet(x)

cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits = logits, labels=one_hot_y)
loss_operation = tf.reduce_mean(cross_entropy)
optimizer = tf.train.AdamOptimizer(learning_rate = rate)
training_operation = optimizer.minimize(loss_operation)

correct_prediction = tf.equal(tf.argmax(logits, 1), tf.argmax(one_hot_y, 1))
accuracy_operation = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

SAVER_DIR = os.getcwd()+'/model'
SAVER_DIR_2 = SAVER_DIR+'/train'
saver = tf.train.Saver()
ckpt = tf.train.get_checkpoint_state(SAVER_DIR)
ckpt_2 = tf.train.latest_checkpoint(SAVER_DIR)

def evaluate(X_data, y_data):
    num_examples = len(X_data)
    total_accuracy = 0
    sess = tf.get_default_session()
    for offset in range(0, num_examples, BATCH_SIZE):
        batch_x, batch_y = X_data[offset:offset+BATCH_SIZE], y_data[offset:offset+BATCH_SIZE]
        accuracy = sess.run(accuracy_operation, feed_dict={x: batch_x, y: batch_y})
        total_accuracy += (accuracy * len(batch_x))
    return total_accuracy / num_examples

with tf.Session() as sess:
    sess.run(tf.initialize_all_variables())

    if ckpt and ckpt.model_checkpoint_path:
        saver.restore(sess, ckpt_2)
        test_accuracy = evaluate(X_test, y_test)
        print("Stored Test Accuracy = {:.3f}".format(test_accuracy))
        sess.close()
        exit()

    num_examples = len(X_train)

    print("Training...")
    print()
    for i in range(EPOCHS):
        #X_train, y_train = tf.random.shuffle(X_train, y_train)
        for offset in range(0, num_examples, BATCH_SIZE):
            end = offset + BATCH_SIZE
            batch_x, batch_y = X_train[offset:end], y_train[offset:end]
            sess.run(training_operation, feed_dict={x: batch_x, y: batch_y})


        validation_accuracy = evaluate(X_validation, y_validation)
        print("EPOCH {} ...".format(i + 1))
        print("Validation Accuracy = {:.3f}".format(validation_accuracy))
        print()
        saver.save(sess, SAVER_DIR_2, global_step=i)

    print("Model saved")
    test_accuracy = evaluate(X_test, y_test)
    print("Test Accuracy = {:.3f}".format(test_accuracy))

