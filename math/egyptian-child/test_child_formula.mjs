import test from 'node:test';
import assert from 'node:assert/strict';
import { deriveChild, verifyExact } from './child_formula.mjs';

test('direct witnesses for the six public-safe corridors', () => {
  const cases = [
    [2n, [1n,2n,2n]], [3n, [1n,6n,6n]],
    [5n, [2n,10n,5n]], [7n, [2n,28n,28n]],
    [9n, [3n,18n,18n]], [17n, [6n,17n,102n]],
    [25n, [7n,350n,70n]], [97n, [25n,4850n,970n]],
    [145n, [37n,10730n,2146n]]
  ];
  for (const [n, expected] of cases) {
    const got=deriveChild(n);
    assert.equal(got.status, 'CANDIDATE_EXACT');
    assert.deepEqual([got.x,got.y,got.z], expected);
    assert.equal(verifyExact(n,got.x,got.y,got.z),true);
    assert.equal(got.nativeAuthenticated,false);
  }
});

test('unresolved residue is a pause, not a nonexistent-solution claim', () => {
  for (const n of [49n,73n,121n,169n]) {
    const got=deriveChild(n);
    assert.equal(got.status,'PAUSE');
    assert.equal(got.x,undefined);
  }
});

test('bounded exact replay does not use floating point', () => {
  let resolved=0;
  for(let i=2;i<=10000;i++){
    const n=BigInt(i), got=deriveChild(n);
    if([1n,49n,73n].includes(n%120n)) assert.equal(got.status,'PAUSE');
    else {
      assert.equal(got.status,'CANDIDATE_EXACT');
      assert.equal(verifyExact(n,got.x,got.y,got.z),true);
      resolved++;
    }
  }
  assert.equal(resolved,9750);
});

test('negative and invalid controls refuse', () => {
  assert.equal(verifyExact(5n,2n,10n,6n),false);
  assert.equal(verifyExact(5n,2n,10n,0n),false);
  assert.equal(verifyExact(5n,2n,10n,5),false);
  for(const n of [1n,-1n,5,'5',5.5]) assert.throws(()=>deriveChild(n),/integer.*2/);
});
