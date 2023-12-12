import logging
logger = logging.getLogger('jade')
logger.setLevel('DEBUG')

# logger = logging.root    # 等效
# if __name__ == '__main__':
#     logger.info('hi , this is log from another module')   #rootlogger的默认级别是warning  默认handler列表为空，默认内部会再指向自己，它的特殊handler: stderrhandler存放在logging.lastResort,所以此行不输出
#     logger.warning('a warning from test')
#     logger.error('an error from tess')

import pdfkit
import wkhtmltopdf
pdfkit.from_file('resume.html', 'dgf.pdf')