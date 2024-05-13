import logging

from mock import MagicMock, call, patch

from .data import SimpleJob

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@patch('logging.Logger._log')
def test_main(
    mock_log: MagicMock,
) -> None:
    SimpleJob().main()

    assert mock_log.call_args_list == [
        call(logging.INFO, 'Start', ()),
        call(logging.INFO, {'key1': 1, 'key2': 2, 'key3': 3}, ()),
        call(logging.INFO, 'Stop', ()),
    ]
