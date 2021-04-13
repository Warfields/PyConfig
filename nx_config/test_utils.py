from contextlib import contextmanager

# noinspection PyProtectedMember
from nx_config._core.naming_utils import (
    mutable_section_attr as _mutable_attr,
    section_validators_attr as _section_validators_attr,
)
from nx_config.config import Config
from nx_config.section import ConfigSection


@contextmanager
def mutable_config(config: Config):
    sections = tuple(getattr(config, s) for s in getattr(type(config), "__annotations__", {}))

    for section in sections:
        setattr(section, _mutable_attr, True)

    try:
        yield
    finally:
        for section in sections:
            setattr(section, _mutable_attr, False)

    try:
        for section in sections:
            for validator in getattr(type(section), _section_validators_attr):
                validator(section)
    except AttributeError as xcp:
        raise AttributeError(
            f"Error validating sections after leaving 'mutable_config' context: {xcp}"
        ) from xcp


def update_section(section: ConfigSection, **kwargs):
    setattr(section, _mutable_attr, True)

    try:
        for k, v in kwargs.items():
            setattr(section, k, v)
    finally:
        setattr(section, _mutable_attr, False)

    try:
        for validator in getattr(type(section), _section_validators_attr):
            validator(section)
    except AttributeError as xcp:
        raise AttributeError(
            f"Error validating section at the end of 'test_utils.update_section' call: {xcp}"
        ) from xcp
