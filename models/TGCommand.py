class TGCommand(object):
    def __init__(self, cid, game_id, header, function, visibility=None):
        self.cid = cid
        self.game_id = game_id
        self.header = header
        self.function = function
        self.visibility = visibility
        self.payload = None

    @staticmethod
    def from_dict(source):
        cmd = TGCommand(cid=source['cid'], game_id=source['game_id'], header=source['header'], function=source['function'])
        if 'payload' in source:
            cmd.payload = source['payload']
        return cmd

    def to_dict(self):
        return {
            'cid': self.cid,
            'game_id': self.game_id,
            'header': self.header,
            'function': self.function,
            'payload': self.payload,
            'visibility': self.visibility
        }

    def __repr__(self):
        return f'TGCommand(cid={self.cid}, header={self.header}, function={self.function}, \
        payload={self.payload}), visibility={self.visibility}'
