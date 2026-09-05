# Traffic-light belief-state control reference

This package is a small, fully inspectable partially observed decision model
used in the accompanying Traffic-Light Problem note. It is designed as a
research reference: every probability, cost and decision rule is exposed in
source. It is not a traffic-control system, autonomous-driving component, or
model of individual people.

## Computational formulation

The latent state is the response pair

\[
z_t \in \{\text{brake}, \text{proceed}\} \times \{\text{wait}, \text{launch early}\}.
\]

The controller observes a deliberately sparse vector

\[
o_t = (\text{approach speed cue}, \text{launch cue}),
\]

and updates a posterior using the fixed emission model:

\[
b_t(z) = P(z_t \mid o_t) \propto P(o_t \mid z_t) P(z_t).
\]

For each permissible phase action \(u\), it evaluates the expected toy loss

\[
Q(b_t, u) = \sum_z b_t(z) R(z, u)
\]

and selects \(\arg\min_u Q(b_t, u)\). The loss function is intentionally
simple: a simultaneous proceed and early launch receives a high fixed cost;
unnecessary clearance or delay carries a smaller cost.

## Package layout

- `model.py`: typed state, observation and action representations.
- `inference.py`: posterior belief update and uncertainty measurement.
- `environment.py`: seeded synthetic episode generator and fixed loss model.
- `policies.py`: single-signal replay, conservative and belief-state policies.
- `evaluation.py`: paired experiment design and summary metrics.

## Reproducibility

The experiment compares each policy against identical seeded episode streams.
It reports mean designed cost, the rate of high-cost conflicts under the toy
loss table, and the proportion of clearance actions. These outcomes are valid
only under the stipulated environment. A favourable result does not establish
traffic safety, human prediction, or performance in Voopa.

Run from the repository root:

```bash
python3 reference/run_traffic_light_experiment.py
python3 -m unittest reference/test_traffic_light_belief_control.py
```
