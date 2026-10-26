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

SCHEMA = 'va-m27-target-readback-candidate/1.2'
DIGEST = re.compile(r'^[0-9a-f]{64}$')
TOKEN = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.-]{2,100}$')
MAX_FILE = 2_000_000
STATE = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.:-]{0,99}$')


def demand(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def strict_json(raw, label):
    # Different readers can disagree on duplicated keys, even if bytes match.
    def pairs(items):
        obj = {}
        for key, value in items:
            demand(key not in obj, 'Duplicate JSON key in ' + label + ': ' + key)
            obj[key] = value
        return obj
    try:
        return json.loads(raw.decode('utf-8'), object_pairs_hook=pairs,
                          parse_constant=lambda _: demand(False, 'Invalid number in ' + label))
    except (ValueError, UnicodeError) as exc:
        raise ValueError('Invalid/ambiguous JSON: ' + label) from exc


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
    value = strict_json(raw, label)
    demand(isinstance(value, dict), 'JSON object required: ' + label)
    return value


def snapshot(root, ref, case, stage, used, observable_id, capture_ids):
    item = object_from(root, ref, 'snapshot-' + stage, used)
    demand(item.get('schema') == 'va-m27-target-snapshot/1.1' and
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
    # Raw capture is a source-hashed, target-scoped sensor-export envelope. Its
    # diagnostic metadata may vary without indicating a changed protected state.
    capture = strict_json(raw, 'protected-target capture')
    demand(isinstance(capture, dict) and
           capture.get('schema') == 'va-m27-target-state-capture/1.0',
           'Protected-target capture format is missing')
    for k in ('caseId', 'candidateId', 'route', 'targetId', 'instrumentId'):
        demand(capture.get(k) == case[k], 'Capture identity disagreement: ' + k)
    demand(capture.get('observableId') == observable_id,
           'Capture measures wrong protected-state observable')
    demand(capture.get('sequence') == item['sequence'],
           'Capture/snapshot acquisition order disagreement')
    capture_id = token(capture.get('captureId'), 'capture ID')
    demand(capture_id not in capture_ids, 'Reused target acquisition ID')
    capture_ids.add(capture_id)
    value = capture.get('observedValue')
    demand(isinstance(value, str) and STATE.fullmatch(value),
           'Invalid protected-state reading')
    return item, value


def inspect(packet, original=None, anchor=None):
    root = Path(packet).absolute()
    demand(root.is_dir() and not root.is_symlink(), 'Missing/linked packet root')
    root = root.resolve()
    mp = root / 'manifest.json'
    demand(mp.is_file() and not mp.is_symlink() and mp.stat().st_size <= MAX_FILE,
           'Missing/oversized/symlink manifest')
    # A packet's internal SHA-256 references are not a freeze. Require a
    # separately held manifest digest, read from a path outside this packet.
    demand(anchor is not None, 'Separate pre-existing anchor is required')
    anchor_path = Path(anchor).absolute()
    demand(anchor_path.is_file() and not anchor_path.is_symlink() and
           anchor_path.stat().st_size <= MAX_FILE and
           not anchor_path.resolve().is_relative_to(root),
           'Freeze anchor must be a separate, non-linked external file')
    anchor_record = strict_json(anchor_path.read_bytes(), 'external freeze anchor')
    demand(isinstance(anchor_record, dict) and
           anchor_record.get('schema') == 'va-m27-external-freeze-anchor/1.0' and
           isinstance(anchor_record.get('anchorId'), str) and
           TOKEN.fullmatch(anchor_record['anchorId']) and
           anchor_record.get('nativeEffectQualified') is False and
           anchor_record.get('publicationAuthorized') is False,
           'Freeze anchor invalid or self-promoting')
    manifest_bytes = mp.read_bytes()
    demand(anchor_record.get('manifestSHA256') == sha(manifest_bytes) and
           anchor_record.get('manifestByteCount') == len(manifest_bytes),
           'Source manifest changed relative to separate freeze anchor')
    manifest = strict_json(manifest_bytes, 'manifest')
    demand(isinstance(manifest, dict) and manifest.get('schema') == SCHEMA,
           'Wrong M27 packet schema')
    demand(manifest.get('classification') == 'PRIVATE_CUSTODIAL_REVIEW' and
           manifest.get('releaseAuthorized') is False and
           manifest.get('independentEffectsQualified') is False,
           'Source packet cannot self-promote human or publication standing')
    frozen = manifest.get('originalFrozenSHA256')
    demand(isinstance(frozen, str) and DIGEST.fullmatch(frozen),
           'Missing original frozen SHA-256')
    demand(anchor_record.get('originalFrozenSHA256') == frozen,
           'Freeze anchor and claimed original identity disagree')
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
    observable = manifest.get('protectedStateObservable')
    demand(isinstance(observable, dict), 'Missing protected-state observable definition')
    observable_id = token(observable.get('observableId'), 'protected observable')
    baseline, permitted = observable.get('baselineValue'), observable.get('permittedValue')
    demand(isinstance(baseline, str) and bool(STATE.fullmatch(baseline)) and
           isinstance(permitted, str) and bool(STATE.fullmatch(permitted)) and
           baseline != permitted, 'Protected-state baseline/permit readings not defined')
    cases = manifest.get('cases')
    demand(isinstance(cases, list) and len(cases) == 2 and
           {x.get('kind') for x in cases if isinstance(x, dict)} == {'ALLOW', 'REFUSE'},
           'M27 requires exactly one permitted and one refused source case')
    used, capture_ids = set(), set()
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
        before, before_value = snapshot(root, case.get('before'), case, 'before', used, observable_id, capture_ids)
        after, after_value = snapshot(root, case.get('after'), case, 'after', used, observable_id, capture_ids)
        demand(after['sequence'] > before['sequence'],
               'Before/after readback acquisition order not established')
        # Both trials must begin with the protected effect ABSENT. Otherwise
        # REFUSE may appear to hold only because the prohibited effect was
        # already present before the refused action was attempted.
        demand(before_value == baseline, 'Pre-case protected effect not at baseline')
        demand(after_value == (permitted if kind == 'ALLOW' else baseline),
               'Protected state did not match permitted effect/refused non-effect')
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
        'schema': 'va-m27-target-readback-preflight/1.2',
        'result': 'SOURCE_RECORDS_INTERNALLY_CONSISTENT_HUMAN_QUALIFICATION_PENDING',
        'caseClassesChecked': ['ALLOW', 'REFUSE'],
        'sameCandidateRouteTarget': True,
        'permittedReadbackChanged': True,
        'protectedObservableId': observable_id,
        'baselineStateRequiredBeforeBothCases': True,
        'stateValueComparedNotRawContainerHash': True,
        'refusedReadbackUnchanged': True,
        'sourceFileRecordsVerified': len(used),
        'outOfPacketManifestFreezeCompared': True,
        'freezeAnchorIdentityAuthenticatedByThisTool': False,
        'originalFreezeChronologyAuthenticatedByThisTool': False,
        'duplicateJSONKeysRejected': True,
        'captureCandidateIdentityBound': True,
        'frozenOriginalBytesRechecked': original_checked,
        'unexaminedEffectRoutes': gaps,
        'instrumentTruthAuthenticated': False,
        'independentObserverIdentityAuthenticated': False,
        'nativeVALineageQualified': False,
        'realWorldEffectIndependentlyProvedByThisTool': False,
        'M27CompletedByThisTool': False,
        'M28AuthorizedByThisTool': False,
        'publicationAuthorized': False,
        'note': ('This checks an out-of-packet file digest, not independent freeze authority or chronology. It compares source-hashed protected-state readings rather than raw-file diffs; checks recorded ordering, receipts, '
                 'candidate/route identity and source hashes. A synthetic fixture can pass. '
                 'Human examiners must inspect actual sensor provenance, calibration, route '
                 'completeness, frozen native identity, observation independence, rights and '
                 'safety before any M27 promotion.')
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--packet', required=True, help='Private candidate packet folder')
    p.add_argument('--original', help='Original frozen file for full-file digest check')
    p.add_argument('--anchor', required=True, help='Previously held separate freeze anchor file, outside packet')
    p.add_argument('--out', help='Private new output file (exclusive create, outside packet)')
    a = p.parse_args()
    try:
        result = inspect(a.packet, a.original, a.anchor)
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
