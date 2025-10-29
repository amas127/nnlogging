import logging

from nnlogging.utils import LoggerConfig, evolve_, get_logging_logger


def test_get_logging_logger(
    logger_config,
    logger_name,
    logger_level,
    logger_propagate,
):
    logger = get_logging_logger(
        logger_config,
        name=logger_name,
        level=logger_level,
        propagate=logger_propagate,
    )
    target_config = evolve_(
        logger_config or LoggerConfig(),
        name=logger_name,
        level=logger_level,
        propagate=logger_propagate,
    )
    assert logger.name == target_config.name
    assert (
        logger.level == getattr(logging, target_config.level)
        if isinstance(target_config.level, str)
        else target_config.level
    )
    assert logger.propagate == target_config.propagate
