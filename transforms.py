from mido import (
    MetaMessage
)

from configman import (
    Namespace,
    RequiredConfig
)


class PassThrough(RequiredConfig):
    required_config = Namespace()

    def __init__(self, config):
        self.config = config

    def __call__(self, message):
        return message


class ScaleTempo(RequiredConfig):
    required_config = Namespace()
    required_config.add_option(
        name="factor",
        default=2.0,
        doc="Scale all tempo information by this number (>1.0 to speed up, <1.0 to slow down)"
    )

    def __init__(self, config):
        self.config = config

    def __call__(self, message):
        if isinstance(message, MetaMessage) and message.type == "set_tempo":
            message.tempo = int(message.tempo / self.config.factor)
        return message
