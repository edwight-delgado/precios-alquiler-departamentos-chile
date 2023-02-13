import logging, coloredlogs


class Log():
    """
        clase log recibe logging (warning, info, error) y el mensaje 
        su salida es un log 
    """
    def __init__(self,filename='app'):
        log = logging.getLogger(__name__)
        coloredlogs.install(level='DEBUG')
        self.log = logging
        #self.log.basicConfig(level=logging.DEBUG)
        #self.log.basicConfig(filename=f'{filename}.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s - %(asctime)s')
        coloredlogs.install(level='DEBUG', logger=log)
        self.log.basicConfig(level=logging.DEBUG)

    def get_log(self,level:str,msg:str)->str:
        if level == 'info':
            return self.log.info(msg)
        if level == 'warning':
            return self.log.warning(msg)
        if level == 'error':
            return self.log.error(msg)
        if level == 'critical':
            return self.log.critical(msg)
        if level == 'debug':
            return self.log.debug(msg)
        else:
            return self.log.error('argumento no especificado')

def main():
    print('--'*12)

    log = Log()
    log.get_log(level='info',msg='this is a test')
    log.get_log(level='warning',msg='this is a warning')
if __name__ == '__main__':
    main()
