import tensorflow as tf


def main():
    print(tf.__version__)
    for device in tf.config.list_physical_devices():
        print(device)


if __name__ == '__main__':
    main()
