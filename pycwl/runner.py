import logging

from pycwl.parser import Parser

logger = logging.getLogger(__name__)


class Runner:
    def __init__(self, args):
        logger.info('runner class')
        workflow = Parser.parse_cwlstream(args.workflow)
        if args.job_object:
            job_object = Parser.parse_job_object(args.job_object)
        else:
            # empty job_object
            job_object = JobObject()
