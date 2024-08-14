from unittest.mock import patch

from webcrawler.utils.parse_args import parse_args


def test_parse_args():
    with patch('sys.argv', ['script.py', '--domain', 'https://test.com', '--max_depth', '5', '--conc', '20']):
        args = parse_args()
        assert args.domain == 'https://test.com'
        assert args.max_depth == 5
        assert args.conc == 20
