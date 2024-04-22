class AbstractLogger:
    def __init__(self) -> None:
        raise NotImplementedError
    
    def log(message, **kwargs):
        raise NotImplementedError
    
    def success(message, **kwargs):
        raise NotImplementedError
    
    def info(message, **kwargs):
        raise NotImplementedError
    
    def error(message, **kwargs):
        raise NotImplementedError