import logging
import coloredlogs

logger = logging.getLogger()
logger.setLevel('INFO')
# logging.FileHandler('output.log', 'w', 'utf-8')
handler = logging.StreamHandler()
logger.addHandler(handler)
coloredlogs.install(level='INFO', logger=logger,
                    fmt='%(asctime)s : %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
