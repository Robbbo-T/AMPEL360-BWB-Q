# AMPEL360 Ledger System

This directory contains the production-grade ledger system for tracking UTCS (Unified Technology Configuration Specification) artifacts across all Configuration Items (CIs) in the AMPEL360 H2-BWB project.

## Overview

The ledger system provides:
- **Automated artifact tracking** with SHA256 integrity verification
- **Fabric blockchain integration** for immutable audit trails
- **CI/CD workflow integration** with PR validation and merge automation
- **Security hardening** with proper secret management and rollback capabilities
- **Observability** through metrics, audit logs, and notifications

## Files

### Configuration
- `ledger_watch.yaml` - Defines which file patterns to track across UTCS phases
- `plan.schema.json` - JSON Schema validation for ledger plans

### Scripts
- `make_plan.py` - Generates ledger plans from changed artifacts with streaming SHA256
- `ci-ledger.sh` - Fabric chaincode interface with retry logic and TLS support
- `pre-commit-hook.sh` - Git hook for automatic plan updates

### Data
- `ledger-plan.json` - Current ledger plan (auto-generated, do not edit manually)

## Workflows

### PR Validation (`.github/workflows/ledger-plan-validate.yml`)
- Detects changed CI artifacts
- Validates ledger plan schema
- Checks artifact coverage and SHA256 integrity
- Optional S3 object existence verification

### Merge Automation (`.github/workflows/ledger-link-on-merge.yml`)
- Links evidence to Fabric blockchain on main branch merges
- Implements mutex-based concurrency control
- Automatic rollback on failures
- Audit trail generation with S3 storage
- Metrics push to Prometheus Pushgateway
- Slack notifications on failures

## Security Features

1. **MSP Material Handling**: Fabric MSP certificates stored in `runner.temp` with immediate cleanup
2. **No Secret Exposure**: Secrets never logged or echoed
3. **Streaming Hash Computation**: Efficient for large files with progress reporting
4. **Retry Logic**: Exponential backoff for network operations
5. **Mutex Protection**: Prevents concurrent ledger modifications
6. **Automatic Rollback**: Git revert on failure with force-with-lease

## Usage

### Manual Plan Generation
```bash
# Generate plan for specific files
python T-TECHNOLOGICAL/LEDGER/cli/make_plan.py path/to/file1.md path/to/file2.yaml

# Generate plan for all changed files in a commit
git diff --name-only HEAD~1 | xargs python T-TECHNOLOGICAL/LEDGER/cli/make_plan.py
```

### Git Hook Installation
```bash
# Install pre-commit hook
cp T-TECHNOLOGICAL/LEDGER/cli/pre-commit-hook.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### Fabric Operations
```bash
# Link evidence (requires Fabric env setup)
./T-TECHNOLOGICAL/LEDGER/cli/ci-ledger.sh linkEvidence CI-ID PHASE '{"artifact_json"}'

# Freeze baseline
./T-TECHNOLOGICAL/LEDGER/ci-ledger.sh freezeBaseline CI-ID PHASE

# Query events
./T-TECHNOLOGICAL/LEDGER/cli/ci-ledger.sh queryEvents CI-ID
```

## Configuration Secrets

The following GitHub secrets must be configured for full functionality:

### Required for Fabric Integration
- `FABRIC_MSP_PATH` - Base64-encoded MSP material (tar.gz)
- `FABRIC_ORDERER` - Orderer endpoint
- `FABRIC_CC_CHANNEL` - Chaincode channel name
- `FABRIC_CC_NAME` - Chaincode name
- `FABRIC_PEER_ADDR` - Peer address
- `FABRIC_MSPID` - MSP ID
- `FABRIC_TLS_CERT` - TLS certificate (optional)

### Optional for Enhanced Features
- `AWS_ROLE_TO_ASSUME` - AWS IAM role for S3 operations
- `AWS_REGION` - AWS region
- `AUDIT_S3_BUCKET` - S3 bucket for audit logs
- `PUSHGATEWAY_URL` - Prometheus Pushgateway endpoint
- `SLACK_WEBHOOK_URL` - Slack webhook for notifications

## Phase Mapping

The system maps directory structures to UTCS phases:

| Directory Pattern | UTCS Phase |
|------------------|------------|
| `01-Requirements` | 01-Requirements |
| `02-Architecture` | 02-Design |
| `02-Design` | 02-Design |
| `03-Building-Prototyping` | 03-Building-Prototyping |
| `04-Executables-Packages` | 04-Executables-Packages |
| `05-Integration` | 05-Verification-Validation |
| `05-Verification-Validation` | 05-Verification-Validation |
| `06-Integration-Qualification` | 06-Integration-Qualification |
| `07-Deployment` | 07-Certification-Security |
| `07-Certification-Security` | 07-Certification-Security |
| `08-Production-Scale` | 08-Production-Scale |
| `09-Maintenance` | 09-Ops-Services |
| `09-Ops-Services` | 09-Ops-Services |
| `10-MRO` | 10-MRO |
| `11-Sustainment-Recycle` | 11-Sustainment-Recycle |

## Monitoring

### Metrics
- `ledger_link_duration_seconds` - Time taken for ledger operations
- Custom labels: `ci`, `phase`

### Audit Logs
- CSV format: `timestamp,actor,operation,ci_id,phase,sha256,duration`
- Stored in S3 with monthly partitioning: `s3://bucket/ledger/YYYY-MM/audit-SHA.csv`

### Alerts
- Slack notifications on workflow failures
- GitHub workflow status checks on PRs

## Troubleshooting

### Common Issues

1. **SHA256 Mismatch**: File modified after plan generation
   - Solution: Regenerate plan with `make_plan.py`

2. **Missing from Plan**: New file not included in ledger
   - Solution: Add file path to `make_plan.py` execution

3. **Fabric Connection Issues**: Network or certificate problems
   - Check Fabric secrets configuration
   - Verify network connectivity to peers/orderers

4. **S3 Access Denied**: AWS credentials issues
   - Verify AWS role and permissions
   - Check regional settings

### Debug Mode
Set `RUNNER_DEBUG: 1` in workflows for verbose output.

## Contributing

1. All changes to tracked artifacts must update the ledger plan
2. Pre-commit hooks are recommended to automate plan updates
3. Test changes with `make_plan.py` before committing
4. Ensure workflows pass PR validation

---
*Generated by AMPEL360 H₂-BWB-Q Framework*
