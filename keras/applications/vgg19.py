# -*- coding: utf-8 -*-
'''VGG19 model for Keras.

# Reference:

- [Very Deep Convolutional Networks for Large-Scale Image Recognition](https://arxiv.org/abs/1409.1556)

'''
from __future__ import print_function
from __future__ import absolute_import

import warnings

from ..models import Model
from ..layers import Flatten, Dense, Input
from ..layers import Convolution2D, MaxPooling2D
from ..utils.layer_utils import convert_all_kernels_in_model
from ..utils.data_utils import get_file
from .. import backend as K
from .imagenet_utils import decode_predictions, preprocess_input


TH_WEIGHTS_PATH = 'https://github.com/fchollet/deep-learning-models/releases/download/v0.1/vgg19_weights_th_dim_ordering_th_kernels.h5'
TF_WEIGHTS_PATH = 'https://github.com/fchollet/deep-learning-models/releases/download/v0.1/vgg19_weights_tf_dim_ordering_tf_kernels.h5'
TH_WEIGHTS_PATH_NO_TOP = 'https://github.com/fchollet/deep-learning-models/releases/download/v0.1/vgg19_weights_th_dim_ordering_th_kernels_notop.h5'
TF_WEIGHTS_PATH_NO_TOP = 'https://github.com/fchollet/deep-learning-models/releases/download/v0.1/vgg19_weights_tf_dim_ordering_tf_kernels_notop.h5'


def VGG19(include_top=True, weights='imagenet',
          input_tensor=None, layers_lr=1.0):
    '''Instantiate the VGG19 architecture,
    optionally loading weights pre-trained
    on ImageNet. Note that when using TensorFlow,
    for best performance you should set
    `image_dim_ordering="tf"` in your Keras config
    at ~/.keras/keras.json.

    The model and the weights are compatible with both
    TensorFlow and Theano. The dimension ordering
    convention used by the model is the one
    specified in your Keras config file.

    # Arguments
        include_top: whether to include the 3 fully-connected
            layers at the top of the network.
        weights: one of `None` (random initialization)
            or "imagenet" (pre-training on ImageNet).
        input_tensor: optional Keras tensor (i.e. output of `layers.Input()`)
            to use as image input for the model.
        layers_lr: common lr multiplier for all layers in the network.
            You can externally add new layers to the model with different learning rates.

    # Returns
        A Keras model instance.
    '''
    if weights not in {'imagenet', None}:
        raise ValueError('The `weights` argument should be either '
                         '`None` (random initialization) or `imagenet` '
                         '(pre-training on ImageNet).')
    # Determine proper input shape
    if K.image_dim_ordering() == 'th':
        if include_top:
            input_shape = (3, 224, 224)
        else:
            input_shape = (3, None, None)
    else:
        if include_top:
            input_shape = (224, 224, 3)
        else:
            input_shape = (None, None, 3)

    if input_tensor is None:
        img_input = Input(shape=input_shape)
    else:
        if not K.is_keras_tensor(input_tensor):
            img_input = Input(tensor=input_tensor, shape=input_shape)
        else:
            img_input = input_tensor
    # Block 1
    x = Convolution2D(64, 3, 3, activation='relu', border_mode='same', name='block1_conv1',
                      W_learning_rate_multiplier=layers_lr, b_learning_rate_multiplier=layers_lr)(img_input)
    x = Convolution2D(64, 3, 3, activation='relu', border_mode='same', name='block1_conv2',
                      W_learning_rate_multiplier=layers_lr, b_learning_rate_multiplier=layers_lr)(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block1_pool')(x)

    # Block 2
    x = Convolution2D(128, 3, 3, activation='relu', border_mode='same', name='block2_conv1',
                      W_learning_rate_multiplier=layers_lr, b_learning_rate_multiplier=layers_lr)(x)
    x = Convolution2D(128, 3, 3, activation='relu', border_mode='same', name='block2_conv2',
                      W_learning_rate_multiplier=layers_lr, b_learning_rate_multiplier=layers_lr)(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block2_pool')(x)

    # Block 3
    x = Convolution2D(256, 3, 3, activation='relu', border_mode='same', name='block3_conv1',
                      W_learning_rate_multiplier=layers_lr, b_learning_rate_multiplier=layers_lr)(x)
    x = Convolution2D(256, 3, 3, activation='relu', border_mode='same', name='block3_conv2',
                      W_learning_rate_multiplier=layers_lr, b_learning_rate_multiplier=layers_lr)(x)
    x = Convolution2D(256, 3, 3, activation='relu', border_mode='same', name='block3_conv3',
                      W_learning_rate_multiplier=layers_lr, b_learning_rate_multiplier=layers_lr)(x)
    x = Convolution2D(256, 3, 3, activation='relu', border_mode='same', name='block3_conv4',
                      W_learning_rate_multiplier=layers_lr, b_learning_rate_multiplier=layers_lr)(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block3_pool')(x)

    # Block 4
    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', name='block4_conv1',
                      W_learning_rate_multiplier=layers_lr, b_learning_rate_multiplier=layers_lr)(x)
    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', name='block4_conv2',
                      W_learning_rate_multiplier=layers_lr, b_learning_rate_multiplier=layers_lr)(x)
    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', name='block4_conv3',
                      W_learning_rate_multiplier=layers_lr, b_learning_rate_multiplier=layers_lr)(x)
    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', name='block4_conv4',
                      W_learning_rate_multiplier=layers_lr, b_learning_rate_multiplier=layers_lr)(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block4_pool')(x)

    # Block 5
    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', name='block5_conv1',
                      W_learning_rate_multiplier=layers_lr, b_learning_rate_multiplier=layers_lr)(x)
    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', name='block5_conv2',
                      W_learning_rate_multiplier=layers_lr, b_learning_rate_multiplier=layers_lr)(x)
    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', name='block5_conv3',
                      W_learning_rate_multiplier=layers_lr, b_learning_rate_multiplier=layers_lr)(x)
    x = Convolution2D(512, 3, 3, activation='relu', border_mode='same', name='block5_conv4',
                      W_learning_rate_multiplier=layers_lr, b_learning_rate_multiplier=layers_lr)(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block5_pool')(x)

    if include_top:
        # Classification block
        x = Flatten(name='flatten')(x)
        x = Dense(4096, activation='relu', name='fc1',
                  W_learning_rate_multiplier=layers_lr, b_learning_rate_multiplier=layers_lr)(x)
        x = Dense(4096, activation='relu', name='fc2',
                  W_learning_rate_multiplier=layers_lr, b_learning_rate_multiplier=layers_lr)(x)
        x = Dense(1000, activation='softmax', name='predictions',
                  W_learning_rate_multiplier=layers_lr, b_learning_rate_multiplier=layers_lr)(x)

    # Create model
    model = Model(img_input, x)

    # load weights
    if weights == 'imagenet':
        if K.image_dim_ordering() == 'th':
            if include_top:
                weights_path = get_file('vgg19_weights_th_dim_ordering_th_kernels.h5',
                                        TH_WEIGHTS_PATH,
                                        cache_subdir='models')
            else:
                weights_path = get_file('vgg19_weights_th_dim_ordering_th_kernels_notop.h5',
                                        TH_WEIGHTS_PATH_NO_TOP,
                                        cache_subdir='models')
            model.load_weights(weights_path)
            if K.backend() == 'tensorflow':
                warnings.warn('You are using the TensorFlow backend, yet you '
                              'are using the Theano '
                              'image dimension ordering convention '
                              '(`image_dim_ordering="th"`). '
                              'For best performance, set '
                              '`image_dim_ordering="tf"` in '
                              'your Keras config '
                              'at ~/.keras/keras.json.')
                convert_all_kernels_in_model(model)
        else:
            if include_top:
                weights_path = get_file('vgg19_weights_tf_dim_ordering_tf_kernels.h5',
                                        TF_WEIGHTS_PATH,
                                        cache_subdir='models')
            else:
                weights_path = get_file('vgg19_weights_tf_dim_ordering_tf_kernels_notop.h5',
                                        TF_WEIGHTS_PATH_NO_TOP,
                                        cache_subdir='models')
            model.load_weights(weights_path)
            if K.backend() == 'theano':
                convert_all_kernels_in_model(model)
    return model
