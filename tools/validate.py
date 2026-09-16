"""Local checks for PPCP documents and this repository's published artifacts."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = {
    version: json.loads((ROOT / 'schema' / f'profile-{version}.json').read_text())
    for version in ('0.1.0', '0.1.1')
}


def validate(profile):
    if not isinstance(profile, dict):
        return ['The profile must be a JSON object.']
    version = profile.get('ppcp_version')
    if not isinstance(version, str) or version not in SCHEMAS:
        return ['Unsupported or missing ppcp_version; supported: ' + ', '.join(SCHEMAS)]
    validator = Draft202012Validator(SCHEMAS[version], format_checker=FormatChecker())
    errors = [f"{'/'.join(map(str, error.absolute_path)) or '(root)'}: {error.message}"
              for error in validator.iter_errors(profile)]
    if errors:
        return errors
    text = profile['content']['text']
    try:
        digest = hashlib.sha256(text.encode('utf-8')).hexdigest()
    except UnicodeEncodeError:
        return ['content/text cannot be encoded as valid UTF-8.']
    if digest != profile['content']['markdown_sha256']:
        errors.append('content/markdown_sha256 does not match the exact UTF-8 Markdown.')
    section_ids = [section['id'] for section in profile['sections']]
    source_ids = [source['id'] for source in profile['sources']]
    if len(set(section_ids)) != len(section_ids):
        errors.append('Section IDs are not unique.')
    if len(set(source_ids)) != len(source_ids):
        errors.append('Source IDs are not unique.')
    for section in profile['sections']:
        if set(section['source_ids']) - set(source_ids):
            errors.append(f"Section {section['id']} references a missing source.")
    return errors


def check_repo():
    release = json.loads((ROOT / 'release.json').read_text())
    version = (ROOT / 'VERSION').read_text().strip()
    assert version == release['version']
    assert (ROOT / 'SPEC.md').read_bytes() == (ROOT / release['specification']).read_bytes()
    for path, expected in release['file_sha256'].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
    for version, schema in SCHEMAS.items():
        Draft202012Validator.check_schema(schema)
        profile = json.loads((ROOT / 'examples' / f'profile-{version}.json').read_text())
        assert profile['ppcp_version'] == version
        assert not validate(profile), validate(profile)
        mutants = []
        for bad_version in ('constructor', '__proto__', '0.1.2', None):
            mutant = copy.deepcopy(profile)
            mutant['ppcp_version'] = bad_version
            mutants.append(mutant)
        mutant = copy.deepcopy(profile)
        del mutant['subject']['name']
        mutants.append(mutant)
        mutant = copy.deepcopy(profile)
        mutant['content']['text'] += '\nChanged without updating the digest.'
        mutants.append(mutant)
        mutant = copy.deepcopy(profile)
        mutant['sections'].append(copy.deepcopy(mutant['sections'][0]))
        mutants.append(mutant)
        mutant = copy.deepcopy(profile)
        mutant['sections'][0]['source_ids'].append('missing-source-fixture')
        mutants.append(mutant)
        for mutant in mutants:
            assert validate(mutant), 'A negative fixture incorrectly passed.'
    print('PASS: published artifact hashes, current/versioned spec agreement, both examples, and 16 negative fixtures.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('profile', type=Path, nargs='?')
    parser.add_argument('--check-repo', action='store_true')
    args = parser.parse_args()
    if args.check_repo:
        check_repo()
    if args.profile:
        try:
            data = json.loads(args.profile.read_text(encoding='utf-8'))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            print(f'Cannot read profile JSON: {error}', file=sys.stderr)
            return 1
        errors = validate(data)
        if errors:
            print('\n'.join(errors), file=sys.stderr)
            return 1
        print(f"PASS: PPCP {data['ppcp_version']} structure, Markdown digest and local section/source references.")
        print('This does not verify claims, identity, approval, signatures or live MCP/host behavior.')
    elif not args.check_repo:
        parser.error('Provide a profile path or --check-repo.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
