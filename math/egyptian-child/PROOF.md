# V.A. public mathematical exhibit — six exact unit-fraction corridors

**Public-safe bounded theorem.** This is elementary external arithmetic, not
the protected NEW K / URK parent kernel, not a native parent-to-child proof,
and not a resolution of the unrestricted Erdős–Straus conjecture.

For every positive integer `n >= 2` whose residue modulo 120 is **not**
`1`, `49`, or `73`, the following six *direct* formulas supply positive
integers `x, y, z` satisfying `4/n = 1/x + 1/y + 1/z`.

1. **Even n:** `(n/2, n, n)`; the unit fractions sum to `2/n+1/n+1/n=4/n`.
2. **n ≡ 3 mod 4:** `((n+1)/4, n(n+1)/2, n(n+1)/2)`; the sum is
   `4/(n+1)+4/[n(n+1)]=4/n`.
3. **n ≡ 5 mod 8:** `((n+3)/4, n(n+3)/4, n(n+3)/8)`; `n+3` is divisible
   by 8, and the sum is `4/(n+3)+12/[n(n+3)]=4/n`.
4. **n ≡ 0 mod 3:** `(n/3, 2n, 2n)`; the sum is `3/n+1/(2n)+1/(2n)=4/n`.
5. **n ≡ 2 mod 3:** `((n+1)/3, n, n(n+1)/3)`; the sum is
   `3/(n+1)+1/n+3/[n(n+1)]=4/n`.
6. **Remaining n ≡ 1 mod 24 with 5 | n(n+3):**
   `((n+3)/4, n(n+3)/2, n(n+3)/10)`; these are integers and the sum is
   `4/(n+3)+12/[n(n+3)]=4/n`.

The six conditions cover the 117 residue classes modulo 120 excluding
`1`, `49`, and `73`. Those three classes are left **unresolved by these
formulas**. This does not assert absence of witnesses in those classes.

## Executable evidence

- [Direct browser formula module](child_formula.mjs)
- [Independent Node.js checks](test_child_formula.mjs)
- Replay: `node --test test_child_formula.mjs`
- Exactly verified: 9,750 outputs for `2 <= n <= 10000`.
- Held open: 249 inputs in the same finite range.
- Negative control: `(n,x,y,z)=(5,2,10,6)` rejected.
- Exact verification uses the integer equation
  `4xyz = n(xy+xz+yz)`; no floating-point arithmetic or factor search.

This public release preserves the distinction between a direct elementary
construction, a verified implementation, and a separately authenticated
native NEW K / URK formula-generation lineage. No private operator is included.
