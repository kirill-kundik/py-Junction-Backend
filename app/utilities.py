class Singleton(type):
    """Singleton pattern realization with meta programming"""
    instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__call__(*args, **kwargs)

        return cls.instance
