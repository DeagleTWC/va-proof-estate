/**
 * Public-safe direct constructive identities for 4/n as three unit fractions.
 * These are elementary external arithmetic witnesses, NOT an authenticated
 * NEW K / URK parent-to-child execution or a solution of the unrestricted problem.
 * No factor searches, approximations, or floating-point operations occur.
 */

export function deriveChild(n) {
  if (typeof n !== 'bigint' || n < 2n) {
    throw new RangeError('n must be a BigInt integer >= 2');
  }
  let x, y, z, corridor;
  if (n % 2n === 0n) {
    [x, y, z] = [n / 2n, n, n];
    corridor = 'EVEN';
  } else if (n % 4n === 3n) {
    [x, y, z] = [(n + 1n) / 4n, n * (n + 1n) / 2n, n * (n + 1n) / 2n];
    corridor = 'THREE_MOD_FOUR';
  } else if (n % 8n === 5n) {
    [x, y, z] = [(n + 3n) / 4n, n * (n + 3n) / 4n, n * (n + 3n) / 8n];
    corridor = 'FIVE_MOD_EIGHT';
  } else if (n % 3n === 0n) {
    [x, y, z] = [n / 3n, 2n * n, 2n * n];
    corridor = 'ZERO_MOD_THREE';
  } else if (n % 3n === 2n) {
    [x, y, z] = [(n + 1n) / 3n, n, n * (n + 1n) / 3n];
    corridor = 'TWO_MOD_THREE';
  } else if (n % 5n === 0n || (n + 3n) % 5n === 0n) {
    [x, y, z] = [(n + 3n) / 4n, n * (n + 3n) / 2n, n * (n + 3n) / 10n];
    corridor = 'FIVE_DIVIDES_N_NPLUS3';
  } else {
    return { status: 'PAUSE', corridor: 'RESIDUES_1_49_73_MOD_120', nativeAuthenticated: false };
  }
  return { status: 'CANDIDATE_EXACT', corridor, x, y, z, nativeAuthenticated: false };
}

export function verifyExact(n, x, y, z) {
  if ([n, x, y, z].some(v => typeof v !== 'bigint' || v <= 0n)) return false;
  return 4n * x * y * z === n * (x * y + x * z + y * z);
}
