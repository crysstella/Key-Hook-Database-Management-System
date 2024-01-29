def building_type_validator() -> dict:
    return {
        'validator': {
            '$jsonSchema': {
                'bsonType': 'object',
                'description': 'Building Type',
                'required': ['type'],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'type': {
                        'bsonType': 'string',
                        'description': 'The type of building'
                    },
                    'rooms': {
                        'bsonType': 'array',
                        'description': 'The rooms of the building type',
                        'items': {
                            'bsonType': 'objectId',
                            'description': 'The room of the building type',
                        }
                    }
                }
            }
        }
    }


def room_validator() -> dict:
    return {
        'validator': {
            '$jsonSchema': {
                'bsonType': 'object',
                'description': 'Room need to be requested',
                'required': ['number', 'building_type'],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'number': {
                        'bsonType': 'int',
                        'description': 'The number of the room'
                    },
                    'building_type': {
                        'bsonType': 'objectId',
                        'description': 'The type of building'
                    },
                    'doors': {
                        'bsonType': 'array',
                        'description': 'The doors of the room',
                        'items': {
                            'bsonType': 'objectId',
                            'description': 'The door of the room',
                        }
                    },
                    'requests': {
                        'bsonType': 'array',
                        'description': 'The requests of the room',
                        'items': {
                            'bsonType': 'objectId',
                            'description': 'The request of the room',
                        }
                    }
                }
            }
        }
    }


def door_name_validator() -> dict:
    return {
        'validator': {
            '$jsonSchema': {
                'bsonType': 'object',
                'description': 'The name of the door',
                'required': ['location'],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'location': {
                        'bsonType': 'string',
                        'enum': ['south', 'north', 'east', 'west'],
                        'description': 'The name should be in the list'
                    },
                    'doors': {
                        'bsonType': 'array',
                        'description': 'The doors of this location',
                        'items': {
                            'bsonType': 'objectId',
                            'description': 'The door of this location',
                        }
                    }
                }
            }
        }
    }


def door_validator() -> dict:
    return {
        'validator': {
            '$jsonSchema': {
                'bsonType': 'object',
                'description': 'The door',
                'required': ['location', 'room'],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'location': {
                        'bsonType': 'objectId',
                        'description': 'The location of the door'
                    },
                    'room': {
                        'bsonType': 'objectId',
                        'description': 'The room of the door'
                    }
                }
            }
        }
    }


def hook_validator() -> dict:
    return {
        'validator': {
            '$jsonSchema': {
                'bsonType': 'object',
                'description': 'The hook',
                'required': ['id'],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'id': {
                        'bsonType': 'int',
                        'description': 'The id of the hook'
                    },
                    'key_copies': {
                        'bsonType': 'array',
                        'description': 'The key copies of the hook',
                        'items': {
                            'bsonType': 'objectId',
                            'description': 'The key copy of the hook',
                        }
                    }
                }
            }
        }
    }


def door_hook_validator() -> dict:
    return {
        'validator': {
            '$jsonSchema': {
                'bsonType': 'object',
                'description': 'The door hook junction',
                'required': ['door', 'hook'],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'door': {
                        'bsonType': 'objectId',
                        'description': 'The door'
                    },
                    'hook': {
                        'bsonType': 'objectId',
                        'description': 'The hook'
                    }
                }
            }
        }
    }


def key_copy_validator() -> dict:
    return {
        'validator': {
            '$jsonSchema': {
                'bsonType': 'object',
                'description': 'The key copy of the hook',
                'required': ['key_id', 'hook'],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'key_id': {
                        'bsonType': 'int',
                        'description': 'The id of the key'
                    },
                    'hook': {
                        'bsonType': 'objectId',
                        'description': 'The hook of the key copy'
                    },
                    'requests': {
                        'bsonType': 'array',
                        'description': 'The requests of the key copy'
                    }
                }
            }
        }
    }


def employee_validator() -> dict:
    return {
        'validator': {
            '$jsonSchema': {
                'bsonType': 'object',
                'description': 'The employee',
                'required': ['id', 'name'],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'id': {
                        'bsonType': 'int',
                        'description': 'The id of the employee'
                    },
                    'name': {
                        'bsonType': 'string',
                        'description': 'The name of the employee'
                    },
                    'requests': {
                        'bsonType': 'array',
                        'description': 'The requests of the employee',
                        'items': {
                            'bsonType': 'objectId',
                            'description': 'The request of the employee',
                        }
                    }
                }
            }
        }
    }


def request_validator() -> dict:
    return {
        'validator': {
            '$jsonSchema': {
                'bsonType': 'object',
                'description': 'The request',
                'required': ['request_id', 'borrow_date', 'employee', 'room', 'key_copy'],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'borrow_date': {
                        'bsonType': 'date',
                        'description': 'The date that employee borrows the key'
                    },
                    'request_id': {
                        'bsonType': 'int',
                        'description': 'The id of the request'
                    },
                    'employee': {
                        'bsonType': 'objectId',
                        'description': 'The employee of the request'
                    },
                    'room': {
                        'bsonType': 'objectId',
                        'description': 'The room of the request'
                    },
                    'key_copy': {
                        'bsonType': 'objectId',
                        'description': 'The key can open the room requested'
                    }
                }
            }
        }
    }


def returned_request_validator():
    return {
        'validator': {
            '$jsonSchema': {
                'bsonType': 'object',
                'description': 'The returned request',
                'required': ['request', 'return_date'],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'request': {
                        'bsonType': 'objectId',
                        'description': 'The request that is returned'
                    },
                    'return_date': {
                        'bsonType': 'date',
                        'description': 'The date that the key is returned'
                    }
                }
            }
        }
    }


def loss_request_validator():
    return {
        'validator': {
            '$jsonSchema': {
                'bsonType': 'object',
                'description': 'The loss request',
                'required': ['request', 'loss_date'],
                'additionalProperties': False,
                'properties': {
                    '_id': {},
                    'request': {
                        'bsonType': 'objectId',
                        'description': 'The request that is returned'
                    },
                    'loss_date': {
                        'bsonType': 'date',
                        'description': 'The date that the key is returned'
                    }
                }
            }
        }
    }
