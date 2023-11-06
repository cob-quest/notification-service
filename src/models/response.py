from bson import ObjectId
from cerberus import Validator

class Response:
    """ 
    Define schema to validate input to prevent invalid formats.
    """
    schema = {
        '_id': {'type': 'string', 'required': False},
        'corId': {'type': 'string', 'required': True},
        'challengeName': {'type': 'string', 'required': True},
        'creatorName': {'type': 'string', 'required': True},
        'duration': {'type': 'integer', 'required': True},
        'participants': {
            'type': 'list', 
            'schema': {'type': 'string'}, 
            'required': True
        }
    }

    def __init__(self, **kwargs):
        self._id = ObjectId(kwargs.get('_id', ObjectId()))
        self.corId = kwargs.get('corId')
        self.challengeName = kwargs.get('challengeName')
        self.creatorName = kwargs.get('creatorName')
        self.duration = kwargs.get('duration')
        self.participants = kwargs.get('participants', [])

    def to_dict(self):
        return {
            "_id": str(self._id),
            "corId": self.corId,
            "challengeName": self.challengeName,
            "creatorName": self.creatorName,
            "duration": self.duration,
            "participants": self.participants
        }
    
    def validate(self):
        validator = Validator(Response.schema)
        if not validator.validate(self.to_dict()):
            return False, validator.errors
        return True, []