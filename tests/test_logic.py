import json, random
import pytest
from logic import forward_chain, explain
from report_rules import CLAUSES
import validate as valid
from validate import validate, to_facts

def load(path="data/reports.jsonl"):
    with open(path) as f:
        return {r["id"]: r for r in map(json.loads, f)}

REPORTS = load()

def test_chain_derives_transitively():
    known, _ = forward_chain({"a"}, [(frozenset({"a"}), "b"), (frozenset({"b"}), "c")])
    assert known == {"a", "b", "c"}

@pytest.mark.timeout(5)
def test_cycle_terminates():
    # TODO: facts {"a"}, clauses a -> b and b -> a. Assert the call returns
    # and that known == {"a", "b"}. If your loop condition is wrong, this
    # test hangs instead of failing, so run it with `pytest --timeout=5`
    # if you have pytest-timeout installed.
    facts = {"a"}
    clauses = [(frozenset({"a"}), "b"), (frozenset({"b"}), "a")]
    known, why = forward_chain(facts, clauses)
    assert known == {"a", "b"}

def test_clause_order_irrelevant():
    facts = to_facts(REPORTS["r9"])
    expected, _ = forward_chain(facts, CLAUSES)
    for seed in range(20):
        shuffled = CLAUSES[:]
        random.Random(seed).shuffle(shuffled)
        got, _ = forward_chain(facts, shuffled)
        assert got == expected

@pytest.mark.parametrize("rid", ["r1", "r3", "r5", "r7"])
def test_valid_reports_accepted(rid):
    ok, reasons, _ = validate(REPORTS[rid])
    assert ok and reasons == []

@pytest.mark.parametrize("rid,reason", [
    ("r2", "invalid:structural_risk_marked_minor"),
    ("r4", "invalid:rot_on_inorganic"),
    ("r6", ["invalid:corrosion_marked_minor", "invalid:corrosion_on_organic"]),
    ("r8", "invalid:none_but_damaged"),
    ("r12", "invalid:corrosion_marked_minor"), #Added this to parameterized test for part E
    ("r13", "invalid:textile_cracked") #Added this to parameterized test for part E
    # TODO: add r6 and r8 with their reasons from the self-check table
])
def test_each_rule_fires_alone(rid, reason):
    ok, reasons, _ = validate(REPORTS[rid])
    if len(reasons) > 1:
        assert reasons == reason
    else:
        assert reasons == [reason]
    assert not ok

def test_multiple_violations_all_reported():
    # TODO: r9 violates two rules. Assert validate() returns BOTH reasons,
    # in sorted order.
    ok, reasons, proofs = validate(REPORTS["r9"])
    assert not ok
    assert reasons == ["invalid:rot_on_inorganic", "invalid:structural_risk_marked_minor"]

@pytest.mark.parametrize("rid,frag", [("r10", "missing field"), ("r11", "unknown material")])
def test_schema_errors_are_not_logic_errors(rid, frag):
    ok, reasons, proofs = validate(REPORTS[rid])
    assert not ok and reasons[0].startswith("schema:") and frag in reasons[0] and proofs == {}

def test_proofs_bottom_out_in_given_facts():
    # TODO: take r2's proof lines. Every line that does NOT contain
    # "because" is a leaf; assert there is at least one leaf and that
    # every leaf contains "(given)".
    ok, reasons, proofs = validate(REPORTS["r2"])
    assert not ok
    lines = []
    for proof in proofs.values():
        for line in proof:
            lines.append(line)
    leaves = []
    for line in lines:
        if "because" not in line:
            leaves.append(line)
    assert leaves
    assert all("(given)" in ln for ln in leaves)

def test_deleting_a_rule_is_caught():
    # TODO: this is the important one. Temporarily replace validate.CLAUSES
    # with a copy that omits the `invalid:rot_on_inorganic` rule (use
    # try/finally to restore it). Assert that report r4 is now WRONGLY
    # accepted. Then restore the rules and assert r4 is rejected again.
    # You are proving two things: the rule matters, and that
    # test_each_rule_fires_alone would catch its removal.
    target = "invalid:rot_on_inorganic"
    original = valid.CLAUSES
    weakened = [c for c in original if c[1] != target]
    assert len(weakened) < len(original)

    try:
        valid.CLAUSES = weakened
        ok, reasons, _ = validate(REPORTS["r4"])
        assert ok and reasons == []
    finally:
        valid.CLAUSES = original

    ok, reasons, proofs = validate(REPORTS["r4"])
    assert not ok
    assert reasons == [target]