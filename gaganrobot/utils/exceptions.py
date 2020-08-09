# pylint: disable=missing-module-docstring

class StopConversation(Exception):
    """ raise if conversation has terminated """


class ProcessCanceled(Exception):
    """ raise if thread has terminated """


class GaganRobotBotNotFound(Exception):
    """ raise if gaganrobot bot not found """
