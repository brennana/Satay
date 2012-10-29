# Defines exceptions for our game

class SettingsError(Exception):
    """Error in game settings"""
    pass

class EntityError(Exception):
    """Error creating entity"""
    pass

class PropertyError(Exception):
    """Error accessing property"""
    pass

class AmbiguityError(Exception):
    """Error resolving noun"""
    pass

class CommandError(Exception):
    """Error executing command"""
    pass

class CommandPropertyError(CommandError, PropertyError):
    """Error with command argument properties"""
    pass

class CommandTypeError(CommandError):
    """Error with command argument type"""
    pass

class CommandConjunctionError(CommandError):
    """Error with conjunctions (e.g. with, for, etc.) between commands"""
    pass

class CommandNoSuitableFormError(CommandError):
    """Error finding a suitable command form from args given"""
    pass

class CommandScopeError(CommandError):
    """Error finding entity in inv/curmap scopes"""
    pass
