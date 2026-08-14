# Evaluation framework

The World Engine is useful only if its additional structure earns its complexity through prediction, calibration, adaptation, or ecosystem outcomes. Evaluation therefore separates executable simulation from evidence about real users.

## Staged program

### Stage I: synthetic recovery

Use synthetic worlds with known latent regimes to test whether the model recovers predictive state, distinguishes persistent from transient variables, and remains calibrated when exposure policy changes.

### Stage II: forward-split observational evaluation

Use temporally ordered application logs to test cold-start mapping, Signal generalization, natural context and preference shifts, and performance under policy change. Logged propensities should support exposure correction where possible.

### Stage III: prospective intervention

Randomize answer order, semantic distance, sequence structure, and controlled exploration where lawful and safe. Predefine primary outcomes and distinguish immediate interaction from delayed relevance, satisfaction, regret, and voluntary return.

### Stage IV: ecosystem evaluation

Measure creator exposure, concentration, minority-signal discovery, coordination, and long-term feedback across users, identities, content, and policy.

## Baselines

Comparisons should include, where applicable:

- collaborative filtering and strong global priors
- session and sequential recommenders
- transformer and state-space recommenders
- latent-intent models
- contextual bandits and model-based reinforcement learning
- capacity-matched generic recurrent state models
- language and multimodal representation baselines

All policies should share candidate pools, safety filters, exposure accounting, and comparable compute budgets.

## Central tests

| Claim | Test | Primary evidence | Failure criterion |
| --- | --- | --- | --- |
| Reduced history dependence | Cold start and history masking | Calibration, regret, adaptation speed | No gain over strong priors or sequence models |
| Signal Intelligence adds structure | Prospective pattern tests | Predictive lift after exposure and semantic controls | Signal vanishes under randomization |
| Digital Minds improve adaptation | Controlled goal, context, and preference shifts | Detection delay and predictive loss | Mixture is slower or less calibrated |
| Rollouts improve discovery | Low-similarity candidate sets | Delayed relevance, satisfaction, and regret | More immediate action but worse later outcomes |
| World State captures externality | Creator and user feedback loops | Exposure quality and concentration | Synthetic-policy result fails prospective transfer |

## Minimum reporting

Report confidence intervals, effect sizes, calibration, seed variance, compute budgets, exposure policy, negative results, privacy leakage, group disparities, and cases in which a simpler model wins.

Longer browsing is not sufficient evidence of benefit. It must be evaluated with relevance, control, delayed outcomes, and an absence of increased regret or fatigue.
