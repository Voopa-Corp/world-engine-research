# Reference scaffold

The reference scaffold translates a small part of the paper into inspectable interfaces. It is intentionally simple and dependency-free.

It demonstrates:

- a Digital Mind state with typed, bounded dimensions
- multivariate Signals carrying strength and confidence
- candidate-conditioned state transition
- uncertainty-aware, multi-objective trajectory scoring
- ranking by expected transition rather than historical similarity alone

It does not demonstrate:

- a learned state representation
- real-user mapping
- production Signal extraction
- a neural or biological model
- empirical superiority over a recommender baseline
- the private Voopa application architecture

Run the example:

```bash
python3 reference/world_engine_scaffold.py
```

Run the tests:

```bash
python3 -m unittest reference/test_scaffold.py
```
