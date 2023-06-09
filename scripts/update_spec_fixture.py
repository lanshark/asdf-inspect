#!/usr/bin/env python3
from __future__ import annotations

import json
import logging
import sys
import tarfile
from io import BytesIO
from pathlib import Path
from subprocess import check_output
from tempfile import TemporaryDirectory
from urllib.request import urlopen

from asdf_inspect.spec import ASDFPythonSpec, Implementation


REPO_ROOT = Path(__file__).parent.parent
FIXTURE_PATH = REPO_ROOT / 'tests' / 'spec_fixture-new.json'

GITHUB_API_ENDPOINT = (
    'https://api.github.com/repos/asdf-vm/asdf/releases/latest')


def fetch_asdf_release_info() -> dict:
    logging.info('fetching asdf release info')
    with urlopen(GITHUB_API_ENDPOINT) as response:
        return json.load(response)


def download_asdf_release(url: str) -> BytesIO:
    logging.info('downloading asdf release')
    with urlopen(url) as response:
        return BytesIO(response.read())


def unpack_asdf_release(release: BytesIO) -> TemporaryDirectory:
    logging.info('unpacking asdf release')
    tmp_dir = TemporaryDirectory()
    with tarfile.open(fileobj=release) as tarball:
        members = []
        while True:
            member = tarball.next()
            if not member:
                break
            name_parts = member.name.split('/')
            if name_parts[0] == '' or '..' in name_parts:
                raise ValueError(f'suspicious tarball file: {member.name}')
            member.name = '/'.join(name_parts[1:])
            members.append(member)
        tarball.extractall(tmp_dir.name, members=members)
    return tmp_dir


def run_asdf(asdf_dir: str, *args: str) -> str:
    return check_output(
        [f'{asdf_dir}/bin/asdf', *args], encoding='utf-8').strip()


def load_fixture_specs() -> dict:
    with open(FIXTURE_PATH) as fobj:
        return json.load(fobj)


def save_fixture_specs(fixture_specs: dict) -> None:
    with open(FIXTURE_PATH, 'w') as fobj:
        json.dump(fixture_specs, fobj, indent=4)
        fobj.write('\n')


def _main() -> None:
    release_info = fetch_asdf_release_info()
    with download_asdf_release(release_info['tarball_url']) as release:
        with unpack_asdf_release(release) as asdf_dir:
            asdf_version = run_asdf(asdf_dir, '--version').partition(' ')[2]
            asdf_specs: list[str] = [
                spec.strip() for spec
                in run_asdf(asdf_dir, 'install', '-l').splitlines()[1:]
            ]
    logging.info(
        'installed asdf %s with %s specs', asdf_version, len(asdf_specs))
    fixture = load_fixture_specs()
    logging.info(
        'loaded fixture %s with %s specs',
        fixture['asdf_version'], len(fixture['specs']),
    )
    fixture_specs_dict = {
        spec['string_spec']: spec for spec in fixture['specs']}
    new_fixture_specs: list[dict] = []
    not_checked_specs: list[str] = []
    for string_spec in asdf_specs:
        spec = ASDFPythonSpec.from_string_spec(string_spec)
        if spec.implementation != Implementation.CPYTHON:
            continue
        spec_dict = spec.to_dict()
        fixture_spec_dict = fixture_specs_dict.get(string_spec)
        checked = (
            fixture_spec_dict and fixture_spec_dict.get('_checked', True))
        if not checked:
            spec_dict['_checked'] = False
            not_checked_specs.append(string_spec)
        elif spec_dict != fixture_spec_dict:
            logging.warning(
                'spec has changed: %s -> %s', fixture_spec_dict, spec_dict)
        new_fixture_specs.append(spec_dict)
    if not_checked_specs:
        logging.warning(
            'not checked: %s %s', len(not_checked_specs), not_checked_specs)
    else:
        logging.info('all specs are checked')
    logging.info('saving fixture with %s specs', len(new_fixture_specs))
    save_fixture_specs({
        'asdf_version': asdf_version,
        'specs': new_fixture_specs,
    })


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] %(message)s', level=logging.INFO)
    try:
        _main()
    except Exception as exc:
        logging.exception('something went wrong: %s', exc)
        sys.exit(1)
