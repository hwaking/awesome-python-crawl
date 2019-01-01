# encoding=utf8
import logging
import os
import codecs


class Config(object):
    def __init__(self):
        if not os.path.exists('log'):
            os.mkdir('log')
        self.path_log = './log/log.txt'
        self.url_file = './log/urllib.txt'
        self.logger = self.get_logger(self.path_log)
        self.save_to_urllib() # 生成 urllib.txt 文件
        self.urllib = self.load_urllib(self.url_file)

    def load_urllib(self, url_file):
        '''加载已抓取的url列表，并通过该列表过滤
        :param url_file: str, urllib位置
        :return: list, url列表
        '''
        with codecs.open(url_file, 'r', 'utf8') as urllib:
            data = [url.strip() for url in urllib.read().strip().split('\n')]
            return data

    def save_to_urllib(self, data=''):
        """抓取完成的url保存到urllib，避免重复抓取
        :param url_file: str, urllib位置
        """
        with codecs.open(self.url_file, 'a+', 'utf8') as in_file:
            in_file.write(data)

    def get_logger(self, logfile):
        """Return a logger instance that writes in filename
        Args:
            filename: (string) path to log.txt
        Returns:
            logger: (instance of logger)
        """
        logger = logging.getLogger('logger')
        logger.setLevel(logging.INFO)
        logging.basicConfig(format='%(message)s', level=logging.INFO)
        form = '%(asctime)s:%(levelname)s: %(message)s'
        handler = logging.FileHandler(logfile, encoding="utf-8")
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter(form))
        logging.getLogger().addHandler(handler)

        return logger
