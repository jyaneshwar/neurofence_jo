from scanner.scanner import SecurityScanner
from scanner.state import ScanState
from scanner.threat_score import ThreatScore
from scanner.workflow import ScanWorkflow


def test_scanner_initialization():

    scanner = SecurityScanner()

    assert scanner is not None
    assert len(scanner.prompts) > 0


def test_threat_score():

    score = ThreatScore.calculate(
        suspicious_outputs=1,
        prompts_tested=4,
    )

    assert score == 25.0


def test_threat_level():

    assert ThreatScore.level(10) == "LOW"
    assert ThreatScore.level(50) == "MEDIUM"
    assert ThreatScore.level(90) == "HIGH"


def test_scan_workflow():

    workflow = ScanWorkflow(
        scan_id="test-001",
        model_path=".",
    )

    workflow.start()

    assert workflow.state == ScanState.LOADING

    workflow.begin_scanning()

    assert workflow.state == ScanState.SCANNING

    workflow.begin_analysis()

    assert workflow.state == ScanState.ANALYZING

    workflow.complete()

    assert workflow.state == ScanState.COMPLETED


def test_security_scan():

    scanner = SecurityScanner()

    result = scanner.scan(".")

    assert result.completed is True
    assert result.prompts_tested == 4
    assert result.suspicious_outputs == 0
    assert result.threat_score == 0.0
    assert result.threat_level == "LOW"
    assert result.errors == []