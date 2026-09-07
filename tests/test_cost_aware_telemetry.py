from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / 'skills/astra/cost-aware-coding/scripts/telemetry.py'
spec = importlib.util.spec_from_file_location('cost_telemetry', SCRIPT)
telemetry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(telemetry)
THREAD = '01a070fb-4ccb-75f2-88df-7e254446533e'


def session(tmp_path, records, suffix=b''):
    path = tmp_path / 'session.jsonl'
    header = {'type': 'session_meta', 'payload': {'id': THREAD}}
    path.write_bytes(b''.join(json.dumps(r).encode() + b'\n' for r in [header, *records]) + suffix)
    return path


def test_metadata_only_and_raw_nonadditive_counters(tmp_path):
    path = session(tmp_path, [
        {'type': 'response_item', 'payload': {'text': 'PRIVATE CONTENT'}},
        {'type': 'turn_context', 'timestamp': 'start',
         'payload': {'turn_id': 'turn', 'model': 'model', 'effort': 'medium', 'prompt': 'PRIVATE CONTENT'}},
        {'type': 'event_msg', 'timestamp': 'end', 'payload': {'type': 'token_count', 'info': {
            'total_token_usage': {'input_tokens': 100, 'cached_input_tokens': 80,
                                  'total_tokens': 110, 'secret': 'PRIVATE CONTENT'},
            'last_token_usage': {'input_tokens': 10, 'total_tokens': 12}}}},
    ])
    result = telemetry.observe(path, THREAD)
    assert result['status'] == 'observed'
    assert result['context']['effort'] == 'medium'
    assert result['usage']['counters']['total_token_usage']['total_tokens'] == 110
    assert result['usage']['counters']['last_token_usage']['total_tokens'] == 12
    assert 'PRIVATE CONTENT' not in json.dumps(result)


def test_wrong_identity_and_incomplete_record(tmp_path):
    path = session(tmp_path, [], b'{"type": "turn_context"')
    result = telemetry.observe(path, THREAD)
    assert 'incomplete_final_record' in result['warnings']
    assert result['context'] is None
    wrong = telemetry.observe(path, 'wrong')
    assert wrong['status'] == 'unavailable'
    assert wrong['usage'] is None


def test_bounded_tail_does_not_reconstruct_missing_context(tmp_path, monkeypatch):
    path = session(tmp_path, [
        {'type': 'turn_context', 'payload': {'model': 'old'}},
        {'type': 'response_item', 'payload': {'text': 'x' * 1000}},
        {'type': 'event_msg', 'payload': {'type': 'token_count', 'info': {
            'total_token_usage': {'total_tokens': 5}}}},
    ])
    monkeypatch.setattr(telemetry, 'TAIL_BYTES', 250)
    result = telemetry.observe(path, THREAD)
    assert result['context'] is None
    assert result['usage']['counters']['total_token_usage']['total_tokens'] == 5
    assert 'bounded_tail_not_full_history' in result['warnings']


def test_lookup_is_identity_specific_and_bounded(tmp_path, monkeypatch):
    dated = tmp_path / '2026/09/07'
    dated.mkdir(parents=True)
    expected = dated / f'rollout-{THREAD}.jsonl'
    expected.touch()
    (dated / 'unrelated.jsonl').touch()
    assert telemetry.locate(tmp_path, THREAD) == expected
    monkeypatch.setattr(telemetry, 'MAX_ENTRIES', 1)
    with pytest.raises(ValueError, match='lookup_limit'):
        telemetry.locate(tmp_path, THREAD)


def test_malformed_metadata_cannot_emit_nested_content(tmp_path):
    path = session(tmp_path, [
        {'type': 'turn_context', 'timestamp': {'text': 'PRIVATE'},
         'payload': {'model': {'text': 'PRIVATE'}, 'effort': ['PRIVATE']}},
    ], b'not-json\n')
    result = telemetry.observe(path, THREAD)
    assert result['context']['model'] is None
    assert result['context']['timestamp'] is None
    assert 'invalid_record' in result['warnings']
    assert 'PRIVATE' not in json.dumps(result)


def test_tail_preserves_record_at_exact_boundary(tmp_path, monkeypatch):
    record = {'type': 'turn_context', 'timestamp': 'now',
              'payload': {'turn_id': 'turn', 'model': 'model', 'effort': 'medium'}}
    path = session(tmp_path, [record])
    monkeypatch.setattr(telemetry, 'TAIL_BYTES', len(json.dumps(record).encode()) + 1)
    assert telemetry.observe(path, THREAD)['context']['model'] == 'model'


def test_empty_metadata_is_not_successful_coverage(tmp_path):
    path = session(tmp_path, [
        {'type': 'turn_context', 'payload': {}},
        {'type': 'event_msg', 'payload': {'type': 'token_count', 'info': {
            'total_token_usage': {'total_tokens': True, 'input_tokens': -1}}}},
    ])
    result = telemetry.observe(path, THREAD)
    assert result['status'] == 'partial'
    assert result['usage'] is None
    assert 'incomplete_context_metadata' in result['warnings']


def test_uuid_date_lookup_avoids_unrelated_archive(tmp_path, monkeypatch):
    # This UUIDv7 was created September 5 UTC; September 4 allows local dates.
    dated = tmp_path / '2026/09/04'
    dated.mkdir(parents=True)
    expected = dated / f'rollout-{THREAD}.jsonl'
    expected.touch()
    old = tmp_path / '2025/01/01'
    old.mkdir(parents=True)
    for index in range(10):
        (old / f'unrelated-{index}.jsonl').touch()
    monkeypatch.setattr(telemetry, 'MAX_ENTRIES', 2)
    assert telemetry.locate(tmp_path, THREAD) == expected


def test_cli_exact_session_and_invalid_id(tmp_path):
    path = session(tmp_path, [])
    for identity, status in [(THREAD, 'partial'), ('not-a-uuid', 'unavailable')]:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), '--thread-id', identity, '--session', str(path)],
            capture_output=True, text=True, check=True,
        )
        assert completed.stderr == ''
        assert json.loads(completed.stdout)['status'] == status
