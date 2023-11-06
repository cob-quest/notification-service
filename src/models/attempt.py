from bson import ObjectId
from cerberus import Validator

class Attempt:
    """
    Define schema to validate input to prevent invalid formats.
    """
    schema = {
        '_id': {'type': 'string', 'required': False},
        'challengeName': {'type': 'string', 'required': True},
        'creatorName': {'type': 'string', 'required': True},
        'participant': {'type': 'string', 'required': True},
        'token': {'type': 'string', 'required': True, 'unique': True},
        'imageRegistryLink': {'type': 'string', 'required': False},
        'sshkey': {'type': 'string', 'required': False},
        'result': {'type': 'float', 'required': False},
        'ipaddress': {'type': 'string', 'required': False},
        'port': {'type': 'string', 'required': False},
    }

    def __init__(self, **kwargs):
        self._id = ObjectId(kwargs.get('_id', ObjectId()))
        self.challengeName = kwargs.get('challengeName')
        self.creatorName = kwargs.get('creatorName')
        self.participant = kwargs.get('participant')
        self.token = kwargs.get('token')
        self.imageRegistryLink = kwargs.get('imageRegistryLink', '')
        self.sshkey = kwargs.get('sshkey', '')
        self.result = kwargs.get('result', 0.0)
        self.ipaddress = kwargs.get('ipaddress', '')
        self.port = kwargs.get('port', '')

    def to_dict(self):
        return {
            "_id": str(self._id),
            "challengeName": self.challengeName,
            "creatorName": self.creatorName,
            "participant": self.participant,
            "token": self.token,
            "imageRegistryLink": self.imageRegistryLink,
            "sshkey": self.sshkey,
            "result": self.result,
            "ipaddress": self.ipaddress,
            "port": self.port,
        }

    def validate(self):
        validator = Validator(Attempt.schema)
        if not validator.validate(self.to_dict()):
            return False, validator.errors
        return True, []

