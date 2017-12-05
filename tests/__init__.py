

##__________________________________________________________________||
import logging
log_handler = logging.StreamHandler()
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_formatter)

names_for_logger = ['scribblers']
for n in names_for_logger:
    log_level = logging.getLevelName('ERROR') # ['DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL']
    logger = logging.getLogger(n)
    logger.setLevel(log_level)
    logger.handlers[:] = [ ]
    logger.addHandler(log_handler)

##__________________________________________________________________||
