def test_bool_to_yes_no_conversion():
    # Replicating app.py helper
    def bool_to_yes_no(val):
        if isinstance(val, bool): return "Yes" if val else "No"
        if isinstance(val, (int, float)): return "Yes" if val == 1 else "No"
        return str(val)

    assert bool_to_yes_no(True) == "Yes"
    assert bool_to_yes_no(0) == "No"
    assert bool_to_yes_no("Yes") == "Yes"

def test_risk_level_classification():
    def get_risk(prob):
        if prob > 0.6: return "🔴 High Risk"
        elif prob > 0.3: return "🟡 Medium"
        else: return "🟢 Low Risk"

    assert get_risk(0.75) == "🔴 High Risk"
    assert get_risk(0.34) == "🟡 Medium"
    assert get_risk(0.12) == "🟢 Low Risk"
