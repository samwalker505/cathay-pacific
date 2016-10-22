class Util(object):
    @staticmethod
    def from_timestamp(time):
        from datetime import datetime
        return datetime.fromtimestamp(time)
