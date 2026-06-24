from src.data_loader import load_data
from src.engines.health_score import calculate_health_score
from src.engines.ma_scanner import scan_targets
from src.engines.valuation import comparable_valuation, dcf_valuation


def test_health_score_range():
    bundle = load_data()
    score = calculate_health_score(bundle.financials, bundle.customers, bundle.risks)
    assert 0 <= score["overall"] <= 100
    assert set(score["dimensions"]) == {"growth", "profitability", "liquidity", "customer", "execution", "risk"}


def test_dcf_outputs_positive_value():
    bundle = load_data()
    dcf = dcf_valuation(bundle.financials)
    comps = comparable_valuation(bundle.financials, bundle.competitors)
    assert dcf["enterprise_value"] > 0
    assert comps["enterprise_value"] > 0
    assert len(dcf["forecast"]) == 5


def test_ma_scanner_ranks_targets():
    bundle = load_data()
    scored = scan_targets(bundle.targets)
    assert scored.iloc[0]["fit_score"] >= scored.iloc[-1]["fit_score"]
    assert "deal_recommendation" in scored.columns

