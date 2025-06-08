import logging

def setup_logger(log_to_file=False, log_file_path="errors.log"):
    logger = logging.getLogger("fastcsv")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
    logger.addHandler(console)
    
    if log_to_file:
        file = logging.FileHandler(log_file_path, mode="w")
        file.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logger.addHandler(file)
        
    return logger