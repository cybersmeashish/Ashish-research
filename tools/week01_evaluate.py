"""Expand original evidence scope and compare the proposed boundary independently."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import platform
from week01_review import (ROOT, WEEK, load, run_fixture, baseline_row, missing_class,
                           flow_documented, write_csv, manifest)
from week01_boundary import controlled_read

def evaluate(fixture, orders):
    original = run_fixture(fixture, orders)
    proposed = controlled_read(fixture, orders)
    assets = {a["asset_id"]: a for a in fixture["declared_assets"]}
    declared = {(f["source"], f["destination"]): f for f in fixture["declared_flows"]}
    paths = {pair: {"origins": ["declared"], "documented": flow_documented(f)}
             for pair, f in declared.items()}
    for origin, records in (("observed_local", original["trace"]),
                            ("configuration_only", fixture["configuration_candidates"])):
        for record in records:
            pair = (record["source"], record["destination"])
            entry = paths.setdefault(pair, {"origins": [], "documented": flow_documented(declared.get(pair))})
            if origin not in entry["origins"]:
                entry["origins"].append(origin)
            for asset_id in pair:
                assets.setdefault(asset_id, {"asset_id": asset_id, "classification": None,
                                             "proposed_owner_role": None})
    missing_assets = sorted(aid for aid, a in assets.items() if missing_class(a))
    missing_paths = sorted(pair for pair, item in paths.items() if not item["documented"])
    observed_missing = [pair for pair in missing_paths if "observed_local" in paths[pair]["origins"]]
    candidate_missing = [pair for pair in missing_paths if "configuration_only" in paths[pair]["origins"]
                         and "observed_local" not in paths[pair]["origins"]]
    baseline = baseline_row(fixture, original)
    row = {
        "fixture_id": fixture["fixture_id"], "fixture_type": fixture["review_label"],
        "procedure_version": "v2-evidence-union",
        "original_decision": original["decision"], "original_evidence_state": original["evidence_state"],
        "proposed_control_decision": proposed["decision"], "proposed_control_reason": proposed["reason"],
        "baseline_assets": baseline["declared_assets"], "identified_assets": len(assets),
        "unclassified_assets": len(missing_assets), "unclassified_asset_ids": ";".join(missing_assets),
        "baseline_flows": baseline["declared_flows"], "identified_flows": len(paths),
        "undocumented_flows": len(missing_paths),
        "undocumented_observed_local_flows": len(observed_missing),
        "undocumented_configuration_only_flows": len(candidate_missing),
        "undocumented_flow_pairs": ";".join("->".join(pair) for pair in missing_paths),
        "original_backend_decidable": "no" if original["evidence_state"] == "missing_evidence" else "bounded-local-only",
        "missing_evidence": "; ".join(fixture["missing_evidence"]),
    }
    detail = {"original": original, "proposed_control": proposed,
              "expanded_assets": list(assets.values()),
              "expanded_flows": [{"source": s, "destination": d, **v}
                                 for (s, d), v in sorted(paths.items())]}
    return row, detail

def execute(output):
    data = load()
    orders = {o["order_id"]: o for o in data["authoritative_synthetic_orders"]}
    rows, details = [], {}
    for fixture in data["fixtures"]:
        row, detail = evaluate(fixture, orders)
        rows.append(row)
        details[fixture["fixture_id"]] = detail
    output.mkdir(parents=True, exist_ok=True)
    write_csv(output / "review-results.csv", rows)
    totals = {key: sum(row[key] for row in rows) for key in (
        "baseline_assets", "identified_assets", "unclassified_assets", "baseline_flows",
        "identified_flows", "undocumented_flows", "undocumented_observed_local_flows",
        "undocumented_configuration_only_flows")}
    report = {"procedure": "v2-evidence-union", "executed_at": datetime.now(timezone.utc).isoformat(),
              "runtime": {"python": platform.python_version(), "system": platform.system(),
                          "machine": platform.machine()},
              "count_scope": "fixture instances; shared identifiers counted per fixture, not a unique estate",
              "totals": totals, "observations": details}
    (output / "observations.json").write_text(json.dumps(report, indent=2) + "\n")
    (output / "source-manifest.json").write_text(json.dumps(manifest([
        WEEK / "review-fixtures.json", ROOT / "tools/week01_review.py",
        ROOT / "tools/week01_boundary.py", Path(__file__)]), indent=2) + "\n")
    return rows, report

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    rows, report = execute(parser.parse_args().out)
    print(json.dumps({"totals": report["totals"],
                      "original_decisions": {r["fixture_id"]: r["original_decision"] for r in rows},
                      "proposed_decisions": {r["fixture_id"]: r["proposed_control_decision"] for r in rows}},
                     indent=2))
