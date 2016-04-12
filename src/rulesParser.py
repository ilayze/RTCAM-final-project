
import logging
import logging.handlers
import argparse
class RulesParser:
    FORMAT = "%(asctime)-10s %(levelname)s: %(message)s"
    def __init__(self, parser):
        parser.add_argument('-l', '--log',
                            help='set the log level. default is INFO',
                            default="INFO",
                            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                            required=False)

        parser.add_argument('-lf', '--log-file',
                            help='Optional log file name',
                            required=False)

        self.args = parser.parse_args()

        self.log = self.args.log

        self.log_file = self.args.log_file

        self.numeric_level = getattr(logging, self.log.upper(), "INFO")

        # logging.basicConfig(format=SteeringBase.FORMAT, level=self.numeric_level)

        self.update_root_logger()

        RulesParser.logger = logging.getLogger("RulesParser")


    def update_root_logger(self):
        formatter = logging.Formatter(RulesParser.FORMAT)

        root_logger = logging.getLogger()
        root_logger.setLevel(self.numeric_level)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        root_logger.addHandler(console_handler)

        if self.log_file:
            file_handler = logging.handlers.RotatingFileHandler(self.log_file, mode='w', backupCount=10)
            file_handler.doRollover()
            # filename, mode='a', maxBytes=0, backupCount=0, encoding=None, delay=0)
            # file_handler = logging.FileHandler(self.log_file)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)

    def parseRules(self):
        with open('community-rules') as f:
            lines = f.readlines()
        all_signatures=dict()
        for line in lines:
            if line.startswith('#') | line.startswith('\n'):
                RulesParser.logger.debug("skipping line: %s",line)
                continue

            contents=line.split('content:')
            if contents.__len__()==1:
                RulesParser.logger.debug("line: %s has no content", line)
                continue
            RulesParser.logger.info('parsing line: %s',line)
            for idx, content in enumerate(contents):
                if idx == 0:
                    continue
                signature=content.split(';')[0]
                RulesParser.logger.info('new signature: %s ',signature)
                hexSignature=signature.encode("hex")
                all_signatures[signature]=hexSignature
        return all_signatures

def main():
    argParser = argparse.ArgumentParser()

    rulesParser = RulesParser(argParser)

    rulesParser.parseRules()

if __name__ == '__main__':
    main()