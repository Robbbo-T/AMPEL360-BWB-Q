#!/usr/bin/env bash
set -euo pipefail

CC_NAME=${CC_NAME:-ci-ledger}
CC_CHANNEL=${CC_CHANNEL:-ampel}

JQ=${JQ:-jq}

invoke() {
  local f="$1"; shift
  local args_json
  args_json=$($JQ -n --arg f "$f" --args '{Args:[$f] + ($ARGS.positional)}' "$@")
  peer chaincode invoke \
    -o "$ORDERER" -C "$CC_CHANNEL" -n "$CC_NAME" \
    -c "$args_json" \
    --waitForEvent \
    ${CORE_PEER_TLS_ROOTCERT_FILE:+ --tls --cafile "$CORE_PEER_TLS_ROOTCERT_FILE"}
}

linkEvidence(){
  local CIID="$1"; local PHASE="$2"; local ART="$3"
  local PAYLOAD=$($JQ -n --arg p "$PHASE" --argjson a "$ART" '{utcsPhase:$p,eventKind:"EvidenceLink",artifact:$a}')
  invoke "linkEvidence" --arg "$CIID" --arg "$PAYLOAD"
}

freezeBaseline(){
  local CIID="$1"; local PHASE="$2"
  local PAYLOAD=$($JQ -n --arg p "$PHASE" '{utcsPhase:$p,eventKind:"BaselineFreeze"}')
  invoke "freezeBaseline" --arg "$CIID" --arg "$PAYLOAD"
}

queryEvents(){
  local CIID="$1"
  peer chaincode query -C "$CC_CHANNEL" -n "$CC_NAME" \
    -c "$($JQ -n --arg f "queryEvents" --arg i "$CIID" '{Args:[$f,$i]}')"
}

"$@"