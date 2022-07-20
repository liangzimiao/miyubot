from utils.service import Service


__doc__ = '''
竞技场相关功能，目前只保留了详细查询
[详细查询 (uid)] 查询账号详细信息'''


class Arena(Service):
    def __init__(self):
        Service.__init__(self, "pcr_arena", __doc__)





