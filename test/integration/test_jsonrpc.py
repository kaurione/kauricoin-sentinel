import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from kauricoind import KauricoinDaemon
from kauricoin_config import KauricoinConfig


def test_kauricoind():
    config_text = KauricoinConfig.slurp_config_file(config.kauricoin_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'00000c1e7a1563dde823100b6e34d078ac5f96404b1f0b83953de8c923b119c2'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000c1e7a1563dde823100b6e34d078ac5f96404b1f0b83953de8c923b119c2'

    creds = KauricoinConfig.get_rpc_creds(config_text, network)
    kauricoind = KauricoinDaemon(**creds)
    assert kauricoind.rpc_command is not None

    assert hasattr(kauricoind, 'rpc_connection')

    # Kauricoin testnet block 0 hash == 00000c1e7a1563dde823100b6e34d078ac5f96404b1f0b83953de8c923b119c2
    # test commands without arguments
    info = kauricoind.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert kauricoind.rpc_command('getblockhash', 0) == genesis_hash
