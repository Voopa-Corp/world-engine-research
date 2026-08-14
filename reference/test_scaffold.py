import unittest

try:
    from .world_engine_scaffold import (
        Candidate,
        MindState,
        Signal,
        WorldState,
        rank_candidates,
        transition,
    )
except ImportError:
    from world_engine_scaffold import (
        Candidate,
        MindState,
        Signal,
        WorldState,
        rank_candidates,
        transition,
    )


class ScaffoldTests(unittest.TestCase):
    def test_transition_is_bounded_and_reduces_uncertainty(self):
        state = MindState(attention=0.95, uncertainty=0.70)
        candidate = Candidate(
            "candidate",
            Signal("signal", 1.0, 1.0, 1.0, 1.0),
            {"attention": 1.0},
        )
        successor = transition(state, candidate)
        self.assertEqual(successor.attention, 1.0)
        self.assertLess(successor.uncertainty, state.uncertainty)

    def test_unknown_dimension_is_rejected(self):
        candidate = Candidate(
            "candidate",
            Signal("signal", 1.0, 1.0, 1.0, 1.0),
            {"private_intention": 1.0},
        )
        with self.assertRaises(ValueError):
            transition(MindState(), candidate)

    def test_ranking_prefers_better_expected_trajectory(self):
        state = MindState(saturation=0.75, novelty=0.60)
        world = WorldState()
        repetitive = Candidate(
            "repetitive",
            Signal("affinity", 0.8, 0.8, 0.8, 0.8),
            {"saturation": 0.20},
            diversity=0.05,
        )
        discovery = Candidate(
            "discovery",
            Signal("contextual novelty", 0.8, 0.8, 0.8, 0.8),
            {"attention": 0.15, "saturation": -0.20, "context_fit": 0.15},
            diversity=0.70,
        )
        ranked = rank_candidates(state, world, [repetitive, discovery])
        self.assertEqual(ranked[0][0].identifier, "discovery")


if __name__ == "__main__":
    unittest.main()
