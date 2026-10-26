#!/usr/bin/env python3
"""M27 data-only original target readback consistency preflight.

This does NOT execute workflows, authenticate sensors/humans, or qualify effects.
Neither a PASS nor any supplied observation file grants milestone or release standing.
"""
import argparse
import hashlib
import json
import os
import re
from pathlib import Path

SCHEMA = 'va-m27-target-readback-candidate/1.0'
DIGEST = re.compile(r'^[0-9a-f]{64}$')
TOKEN = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.-]{2,100}$')
MAX_FILE = 2_000_000


def demand(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def token(value, label):
    demand(isinstance(value, str) and bool(TOKEN.fullmatch(value)), 'Invalid ' + label)
    return value


def source(root, ref, label, used):
    demand(isinstance(ref, dict), 'Missing ' + label)
    path, claimed = ref.get('path'), ref.get('sha256')
    demand(isinstance(path, str) and 0 < len(path) < 250 and '\\' not in path,
           'Unsafe path: ' + label)
    rel = Path(path)
    demand(not rel.is_absolute() and '..' not in rel.parts and rel.as_posix() == path,
           'Unsafe path: ' + label)
    demand(isinstance(claimed, str) and DIGEST.fullmatch(claimed),
           'Invalid digest: ' + label)
    p = root
    for part in rel.parts:
        p = p / part
        demand(not p.is_symlink(), 'Symlink refused: ' + label)
    resolved = p.resolve()
    demand(resolved.is_relative_to(root) and resolved.is_file(), 'Missing source: ' + label)
    demand(resolved.stat().st_size <= MAX_FILE, 'Source too large: ' + label)
    demand(path not in used, 'A source path was reused: ' + label)
    used.add(path)
    data = resolved.read_bytes()
    demand(sha(data) == claimed, 'Source digest mismatch: ' + label)
    return data


def object_from(root, ref, label, used):
    raw = source(root, ref, label, used)
    try:
        value = json.loads(raw.decode('utf-8'))
    except (ValueError, UnicodeError) as exc:
        raise ValueError('Invalid JSON: ' + label) from exc
    demand(isinstance(value, dict), 'JSON object required: ' + label)
    return value


def snapshot(root, ref, case, stage, used):
    item = object_from(root, ref, 'snapshot-' + stage, used)
    demand(item.get('schema') == 'va-m27-target-snapshot/1.0' and
           item.get('caseId') == case['caseId'] and item.get('stage') == stage,
           'Snapshot identity/stage mismatch')
    for k in ('route', 'targetId', 'observerId', 'instrumentId'):
        token(item.get(k), 'snapshot ' + k)
        demand(item[k] == case[k], 'Snapshot diverges from case: ' + k)
    demand(item.get('measurementSource') == 'SEPARATE_TARGET_READBACK' and
           item.get('decisionLabelIsMeasurement') is False,
           'Snapshot is not declared separate target readback')
    demand(isinstance(item.get('calibrationOrAuditReference'), str) and
           len(item['calibrationOrAuditReference'].strip()) >= 8,
           'Instrument validation reference missing')
    demand(type(item.get('sequence')) is int and item['sequence'] >= 0,
           'Invalid acquisition sequence')
    raw = source(root, item.get('rawCapture'), 'raw-' + stage, used)
    demand(len(raw) > 0, 'Empty external raw capture')
    demand(item.get('readbackSHA256') == sha(raw), 'Snapshot/readback source disagreement')
    return item, sha(raw)


def inspect(packet, original=None):
    root = Path(packet).absolute()
    demand(root.is_dir() and not root.is_symlink(), 'Missing/linked packet root')
    root = root.resolve()
    mp = root / 'manifest.json'
    demand(mp.is_file() and not mp.is_symlink() and mp.stat().st_size <= MAX_FILE,
           'Missing/oversized/symlink manifest')
    manifest = json.loads(mp.read_text(encoding='utf-8'))
    demand(isinstance(manifest, dict) and manifest.get('schema') == SCHEMA,
           'Wrong M27 packet schema')
    demand(manifest.get('classification') == 'PRIVATE_CUSTODIAL_REVIEW' and
           manifest.get('releaseAuthorized') is False and
           manifest.get('independentEffectsQualified') is False,
           'Source packet cannot self-promote human or publication standing')
    frozen = manifest.get('originalFrozenSHA256')
    demand(isinstance(frozen, str) and DIGEST.fullmatch(frozen),
           'Missing original frozen SHA-256')
    original_checked = False
    if original is not None:
        p = Path(original).absolute()
        demand(p.is_file() and not p.is_symlink() and p.stat().st_size <= 1_000_000_000,
               'Original bytes unavailable/invalid')
        h = hashlib.sha256()
        with p.open('rb') as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b''):
                h.update(block)
        demand(h.hexdigest() == frozen, 'Frozen original byte identity mismatch')
        original_checked = True
    routes = manifest.get('declaredRoutes')
    demand(isinstance(routes, list) and 1 <= len(routes) <= 20 and
           all(isinstance(r, str) and TOKEN.fullmatch(r) for r in routes) and
           len(set(routes)) == len(routes), 'Invalid route inventory')
    cases = manifest.get('cases')
    demand(isinstance(cases, list) and len(cases) == 2 and
           {x.get('kind') for x in cases if isinstance(x, dict)} == {'ALLOW', 'REFUSE'},
           'M27 requires exactly one permitted and one refused source case')
    used = set()
    observed = {}
    for case in cases:
        kind = case['kind']
        for k in ('caseId', 'candidateId', 'route', 'targetId', 'observerId', 'instrumentId'):
            token(case.get(k), 'case ' + k)
        demand(case['route'] in routes, 'Case route undeclared')
        condition = case.get('governingConditionSHA256')
        demand(isinstance(condition, str) and DIGEST.fullmatch(condition),
               'Unbound governing condition')
        demand(case.get('readbackOutsideDecisionProcess') is True,
               'Readback must be separately collected')
        receipt = object_from(root, case.get('receipt'), 'receipt', used)
        decision = 'EXECUTE' if kind == 'ALLOW' else 'REFUSE'
        for k, expected in [('caseId', case['caseId']), ('candidateId', case['candidateId']),
                            ('route', case['route']), ('targetId', case['targetId']),
                            ('governingConditionSHA256', condition),
                            ('originalFrozenSHA256', frozen), ('decision', decision)]:
            demand(receipt.get(k) == expected, 'Original receipt inconsistent: ' + k)
        before, before_value = snapshot(root, case.get('before'), case, 'before', used)
        after, after_value = snapshot(root, case.get('after'), case, 'after', used)
        demand(after['sequence'] > before['sequence'],
               'Before/after readback acquisition order not established')
        demand((before_value != after_value) is (kind == 'ALLOW'),
               'Readback did not match permitted change/refused non-change')
        observed[kind] = dict(case=case, before=before_value, after=after_value)
    a, b = observed['ALLOW']['case'], observed['REFUSE']['case']
    for k in ('candidateId', 'route', 'targetId'):
        demand(a[k] == b[k], 'Not one bounded consequence: ' + k)
    demand(a['caseId'] != b['caseId'], 'Reused case identity')
    demand(a['governingConditionSHA256'] != b['governingConditionSHA256'],
           'No distinguishable governing condition for refusal')
    examined_routes = {a['route']}
    gaps = sorted(set(routes) - examined_routes)
    demand(manifest.get('unexaminedRoutes') == gaps,
           'Unexamined effect routes not exactly declared')
    return {
        'schema': 'va-m27-target-readback-preflight/1.0',
        'result': 'SOURCE_RECORDS_INTERNALLY_CONSISTENT_HUMAN_QUALIFICATION_PENDING',
        'caseClassesChecked': ['ALLOW', 'REFUSE'],
        'sameCandidateRouteTarget': True,
        'permittedReadbackChanged': True,
        'refusedReadbackUnchanged': True,
        'sourceFileRecordsVerified': len(used),
        'frozenOriginalBytesRechecked': original_checked,
        'unexaminedEffectRoutes': gaps,
        'instrumentTruthAuthenticated': False,
        'independentObserverIdentityAuthenticated': False,
        'nativeVALineageQualified': False,
        'realWorldEffectIndependentlyProvedByThisTool': False,
        'M27CompletedByThisTool': False,
        'M28AuthorizedByThisTool': False,
        'publicationAuthorized': False,
        'note': ('This checks supplied raw readback bytes, recorded ordering, receipts, '
                 'candidate/route identity and source hashes. A synthetic fixture can pass. '
                 'Human examiners must inspect actual sensor provenance, calibration, route '
                 'completeness, frozen native identity, observation independence, rights and '
                 'safety before any M27 promotion.')
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--packet', required=True, help='Private candidate packet folder')
    p.add_argument('--original', help='Original frozen file for full-file digest check')
    p.add_argument('--out', help='Private new output file (exclusive create, outside packet)')
    a = p.parse_args()
    try:
        result = inspect(a.packet, a.original)
        if a.out:
            dest = Path(a.out).absolute()
            demand(not dest.exists() and not dest.is_symlink() and
                   not dest.resolve().is_relative_to(Path(a.packet).resolve()),
                   'Output file exists, linked, or inside packet')
            fd = os.open(dest, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2)
                f.write('\n')
        print(json.dumps(result, indent=2))
    except (ValueError, OSError, TypeError, KeyError, json.JSONDecodeError) as exc:
        p.exit(2, 'REFUSED: ' + str(exc) + '\n')


if __name__ == '__main__':
    main()
