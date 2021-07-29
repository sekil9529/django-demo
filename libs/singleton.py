# coding: utf-8

import threading


class SingletonType(type):
    def __init__(cls, name, bases, namespace):
        super(SingletonType, cls).__init__(name, bases, namespace)
        cls._instance = None
        cls._instance_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        # 避免每次都要加锁
        if cls._instance is None:
            # 线程安全
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instance
