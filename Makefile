# AMPEL360 H₂-BWB-Q Validation Makefile

# Configuration
CI_PATH = OPTIM-FRAMEWORK/T-TECHNOLOGICAL/AMEDEO-PELLICCIA/INTEGRATED/AMPEL360-H2-BWB-QNNN/A-ARCHITECTURE/CA-A-001-CENTER-BODY-BOX/CI-CA-A-001-001-CB-PRIMARY-GRID
PYTHON = python3

# Help target
.PHONY: help
help:
	@echo "AMPEL360 CI Validation Commands"
	@echo "================================"
	@echo ""
	@echo "Main Commands:"
	@echo "  validate           - Run full CI validation"
	@echo "  evidence-status    - Check evidence file status"
	@echo "  requirements       - Analyze requirements coverage"
	@echo "  all-reports        - Generate all reports"
	@echo ""
	@echo "Output Commands:"
	@echo "  validate-json      - Validation report in JSON format"
	@echo "  evidence-csv       - Evidence status as CSV"
	@echo "  evidence-checklist - Evidence completion checklist"
	@echo "  traceability       - Requirements traceability matrix"
	@echo ""
	@echo "CI-specific Commands:"
	@echo "  validate-primary-grid - Validate CI-CA-A-001-001-CB-PRIMARY-GRID"
	@echo ""

# Main validation commands
.PHONY: validate
validate:
	@echo "🔍 Running CI Artifact Validation..."
	$(PYTHON) OPTIM-FRAMEWORK/I-.INTELLIGENT/scripts/validate_artifacts.py --path $(CI_PATH) --check-links

.PHONY: validate-json
validate-json:
	@echo "🔍 Running CI Artifact Validation (JSON output)..."
	$(PYTHON) OPTIM-FRAMEWORK/I-.INTELLIGENT/scripts/validate_artifacts.py --path $(CI_PATH) --check-links --output-format json

.PHONY: evidence-status
evidence-status:
	@echo "📊 Checking Evidence Status..."
	$(PYTHON) OPTIM-FRAMEWORK/I-.INTELLIGENT/scripts/evidence_tracker.py $(CI_PATH)

.PHONY: evidence-csv
evidence-csv:
	@echo "📊 Exporting Evidence Status to CSV..."
	$(PYTHON) OPTIM-FRAMEWORK/I-.INTELLIGENT/scripts/evidence_tracker.py $(CI_PATH) --export-csv evidence-status.csv
	@echo "📄 Evidence status exported to evidence-status.csv"

.PHONY: evidence-checklist
evidence-checklist:
	@echo "📋 Generating Evidence Checklist..."
	$(PYTHON) OPTIM-FRAMEWORK/I-.INTELLIGENT/scripts/evidence_tracker.py $(CI_PATH) --checklist evidence-checklist.md
	@echo "📄 Evidence checklist generated: evidence-checklist.md"

.PHONY: requirements
requirements:
	@echo "📋 Analyzing Requirements Coverage..."
	$(PYTHON) OPTIM-FRAMEWORK/I-.INTELLIGENT/scripts/requirements_coverage.py $(CI_PATH)

.PHONY: traceability
traceability:
	@echo "🔗 Generating Requirements Traceability Matrix..."
	$(PYTHON) OPTIM-FRAMEWORK/I-.INTELLIGENT/scripts/requirements_coverage.py $(CI_PATH) --traceability traceability-matrix.md
	@echo "📄 Traceability matrix generated: traceability-matrix.md"

# Combined reports
.PHONY: all-reports
all-reports: validate evidence-status requirements validate-config-index

# Configuration Index validation
.PHONY: validate-config-index
validate-config-index:
	@echo "🔍 Validating Configuration Index..."
	$(PYTHON) tools/validate_config_index.py
	@echo ""
	@echo "✅ All validation reports completed!"

.PHONY: export-all
export-all: validate-json evidence-csv evidence-checklist traceability
	@echo ""
	@echo "📁 All reports exported to files!"

# CI-specific validation (can be extended for other CIs)
.PHONY: validate-primary-grid
validate-primary-grid: validate

# Clean generated files
.PHONY: clean
clean:
	@echo "🧹 Cleaning generated files..."
	rm -f validation-report.json
	rm -f evidence-status.csv
	rm -f evidence-checklist.md
	rm -f traceability-matrix.md
	@echo "✅ Clean completed!"

# Check dependencies
.PHONY: check-deps
check-deps:
	@echo "🔧 Checking dependencies..."
	$(PYTHON) -c "import yaml; print('✅ PyYAML available')"
	@echo "✅ All dependencies available"

# Development helpers
.PHONY: test-scripts
test-scripts: check-deps
	@echo "🧪 Testing validation scripts..."
	$(PYTHON) OPTIM-FRAMEWORK/I-.INTELLIGENT/scripts/validate_artifacts.py --help > /dev/null && echo "✅ validate_artifacts.py OK"
	$(PYTHON) OPTIM-FRAMEWORK/I-.INTELLIGENT/scripts/evidence_tracker.py --help > /dev/null && echo "✅ evidence_tracker.py OK"
	$(PYTHON) OPTIM-FRAMEWORK/I-.INTELLIGENT/scripts/requirements_coverage.py --help > /dev/null && echo "✅ requirements_coverage.py OK"
	$(PYTHON) tools/validate_config_index.py > /dev/null && echo "✅ validate_config_index.py OK"
	@echo "✅ All scripts tested successfully"