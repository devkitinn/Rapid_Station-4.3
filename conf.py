#!/usr/bin/python
import os.path
import configparser
import sys, getopt
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0

# instantiate config
config = ConfigParser()

def get_conf():
    if os.path.exists('rapid.ini') == False:
        # Create a new rapid.ini file
        # Part Settings
        config['PART SETTINGS'] = {}
        partini = config['PART SETTINGS']
        partini['edit'] = 'False'
        partini['new'] = 'False'
        # Visible Stations
        config['VISIBLE STATIONS'] = {}
        stationini = config['VISIBLE STATIONS']
        stationini['allocations'] = 'True'
        stationini['bay_drops'] = 'True'
        stationini['purchasing'] = 'True'
        stationini['receiving'] = 'True'
        stationini['create_nest'] = 'True'
        stationini['nesting'] = 'True'
        stationini['holzma'] = 'True'
        stationini['edging'] = 'True'
        stationini['hinging'] = 'True'
        stationini['special'] = 'True'
        stationini['benchtops'] = 'True'
        stationini['dispatch'] = 'True'
        stationini['recut_complete'] = 'False'
        # Division section (new)
        config['DIVISION'] = {}
        config['DIVISION']['allowed'] = 'both'  # default
        # PostgreSQL connection
        config['POSTGRESQL'] = {}
        config['POSTGRESQL']['host']     = '172.16.16.46'
        config['POSTGRESQL']['database'] = 'rapid'
        config['POSTGRESQL']['user']     = 'ki'
        config['POSTGRESQL']['password'] = 'Link3061'
        with open('rapid.ini', 'w') as configfile:
            config.write(configfile)
            configfile.close()
    # Now read the config file
    config.read('rapid.ini')

    # --- DIVISION defaults if missing ---
    if not config.has_section('DIVISION'):
        config.add_section('DIVISION')
    if not config.has_option('DIVISION', 'allowed'):
        # default to both divisions when not set
        config.set('DIVISION', 'allowed', 'both')


def _normalize_divisions(raw: str):
    """
    Turn 'Q', 'V', 'O', 'both', 'Q,V', 'Q,O', 'V,O', 'Q,V,O' into a canonical list.
    Returns ['Q'], ['V'], ['O'], or combinations like ['Q','V'] / ['Q','V','O'].
    """
    if not raw:
        return ['Q', 'V']  # default visible divisions
    val = raw.strip().upper()
    if val == 'BOTH':
        return ['Q', 'V']
    # accept comma-separated tokens
    parts = [p.strip() for p in val.split(',') if p.strip()]
    if not parts:
        parts = [val]
    allowed = []
    for p in parts:
        if p.startswith('Q'):
            allowed.append('Q')
        elif p.startswith('V'):
            allowed.append('V')
        elif p.startswith('O') or p.startswith('OTHER'):
            allowed.append('O')
    # deduplicate while preserving order
    seen = set()
    canonical = []
    for d in allowed:
        if d not in seen:
            canonical.append(d)
            seen.add(d)
    return canonical or ['Q', 'V']


def get_allowed_divisions():
    """
    Read DIVISION.allowed from config and return list ['Q','V','O'] subset.
    """
    try:
        raw = config.get('DIVISION', 'allowed')
    except Exception:
        raw = 'both'
    return _normalize_divisions(raw)


