# *** Class decorators ***
def validate_class_parameters(method_name, expected_params=None):
    def decorator(cls):
        original_method = getattr(cls, method_name)

        def wrapper(self, event_log, *args, **kwargs):
            params = kwargs.keys()
            missing_params = [param for param in expected_params or [] if param not in params]
            if missing_params:
                raise TypeError(
                    f"Parameters {missing_params} are missing in the '{method_name}' method of {cls.__name__}")
            if method_name == 'validate' and not isinstance(event_log, dict):
                raise TypeError(f"Parameter 'event_log' is not a dict in the '{method_name}' method of {cls.__name__}")
            return original_method(self, event_log, *args, **kwargs)

        setattr(cls, method_name, wrapper)
        return cls

    return decorator


def generate_repr(cls):
    def __repr__(self):
        return f'{cls.__name__}({", ".join(f"{k}={v}" for k, v in self.__dict__.items())})'

    setattr(cls, '__repr__', __repr__)
    return cls


def generate_error_message(expected, received, details, field):
    return (
        f"[ERROR] El valor esperado de '{field}' no coincide con el recibido ."
        f"\n[DETALLE]:"
        f"\n [SKU]: {details}"
        f"\n [Expected {field}]: {expected}"
        f"\n [Received {field}]: {received}"
    )
