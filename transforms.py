from mido import (
    Message,
    MetaMessage
)

from configman import (
    Namespace,
    RequiredConfig
)

import random


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


class DropNotes(RequiredConfig):
    required_config = Namespace()
    required_config.add_option(
        name="ratio",
        default=1/4,
        doc="Proportion of notes to drop (1.0 for silence, 0.0 to drop nothing)"
    )

    def __init__(self, config):
        self.config = config
        self.stored_time = 0

    def __call__(self, message):
        if isinstance(message, Message) and message.type in ('note_on', 'note_off'):
            if message.type == "note_on" and random.random() < self.config.ratio:
                # Drop the note. But don't lose the time that would have been spent playing it!
                self.stored_time += message.time
                return None

            # If we get here, we are not dropping this note.
            # Recover any time "stored" from a previously dropped note.
            if self.stored_time:
                message = message.copy(time=message.time + self.stored_time)
                self.stored_time = 0
        return message
