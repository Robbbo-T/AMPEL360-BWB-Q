# DET - Digital Evidence Twin
# Immutable evidence collection and PQC-secured audit trail

"""
Digital Evidence Twin (DET): Provides immutable, cryptographically secured
evidence collection for safety cases and certification compliance.
Implements Post-Quantum Cryptography (PQC) for future-proof security.
"""

import hashlib
import time
import json
import threading
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, field, asdict
import logging
from pathlib import Path
import sqlite3
from queue import Queue, Empty
import hmac

class EvidenceType(Enum):
    KERNEL_TRACE = "kernel_trace"
    VOTER_DECISION = "voter_decision"
    CCMF_CYCLE = "ccmf_cycle"
    SAFETY_VALIDATION = "safety_validation"
    ENERGY_POLICY = "energy_policy"
    FDI_EVENT = "fdi_event"
    SYSTEM_STATE = "system_state"
    PERFORMANCE_METRIC = "performance_metric"

class CriticalityLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
    SAFETY_CRITICAL = 5

@dataclass
class EvidenceRecord:
    """Immutable evidence record"""
    id: str
    timestamp: float
    evidence_type: EvidenceType
    criticality: CriticalityLevel
    source_component: str
    event_data: Dict[str, Any]
    context: Dict[str, Any] = field(default_factory=dict)
    hash_chain_previous: str = ""
    record_hash: str = ""
    pqc_signature: str = ""

class PQCSigningEngine:
    """Post-Quantum Cryptography signing engine"""
    
    def __init__(self):
        self.logger = logging.getLogger("DET-PQC")
        # In production, this would use actual PQC libraries like Kyber/Dilithium
        self.signing_key = "PQC_SIGNING_KEY_PLACEHOLDER"
        
    def sign_evidence(self, evidence: EvidenceRecord) -> str:
        """Sign evidence record with PQC signature"""
        
        # Create canonical representation for signing
        signing_data = {
            "id": evidence.id,
            "timestamp": evidence.timestamp,
            "evidence_type": evidence.evidence_type.value,
            "criticality": evidence.criticality.value,
            "source_component": evidence.source_component,
            "event_data": evidence.event_data,
            "context": evidence.context,
            "hash_chain_previous": evidence.hash_chain_previous
        }
        
        canonical_json = json.dumps(signing_data, sort_keys=True, separators=(',', ':'))
        
        # In production: actual PQC signature (Dilithium, etc.)
        # For now: HMAC simulation
        signature = hmac.new(
            self.signing_key.encode(),
            canonical_json.encode(),
            hashlib.sha256
        ).hexdigest()
        
        self.logger.debug(f"PQC signed evidence {evidence.id}")
        return f"PQC_{signature}"
    
    def verify_signature(self, evidence: EvidenceRecord, signature: str) -> bool:
        """Verify PQC signature"""
        expected_signature = self.sign_evidence(evidence)
        return hmac.compare_digest(signature, expected_signature)

class WORMStorage:
    """Write-Once-Read-Many immutable storage"""
    
    def __init__(self, storage_path: str):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.db_path = self.storage_path / "evidence.db"
        self.logger = logging.getLogger("DET-WORM")
        
        self._init_database()
    
    def _init_database(self):
        """Initialize WORM database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS evidence_records (
            id TEXT PRIMARY KEY,
            timestamp REAL NOT NULL,
            evidence_type TEXT NOT NULL,
            criticality INTEGER NOT NULL,
            source_component TEXT NOT NULL,
            event_data TEXT NOT NULL,
            context TEXT NOT NULL,
            hash_chain_previous TEXT NOT NULL,
            record_hash TEXT NOT NULL,
            pqc_signature TEXT NOT NULL,
            written_at REAL NOT NULL
        )
        ''')
        
        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_timestamp ON evidence_records(timestamp)
        ''')
        
        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_evidence_type ON evidence_records(evidence_type)
        ''')
        
        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_criticality ON evidence_records(criticality)
        ''')
        
        conn.commit()
        conn.close()
        
        self.logger.info(f"WORM storage initialized at {self.db_path}")
    
    def store_evidence(self, evidence: EvidenceRecord) -> bool:
        """Store evidence record (write-once)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if record already exists (write-once enforcement)
            cursor.execute("SELECT id FROM evidence_records WHERE id = ?", (evidence.id,))
            if cursor.fetchone():
                self.logger.error(f"Evidence {evidence.id} already exists - WORM violation")
                return False
            
            # Insert new record
            cursor.execute('''
            INSERT INTO evidence_records (
                id, timestamp, evidence_type, criticality, source_component,
                event_data, context, hash_chain_previous, record_hash,
                pqc_signature, written_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                evidence.id,
                evidence.timestamp,
                evidence.evidence_type.value,
                evidence.criticality.value,
                evidence.source_component,
                json.dumps(evidence.event_data),
                json.dumps(evidence.context),
                evidence.hash_chain_previous,
                evidence.record_hash,
                evidence.pqc_signature,
                time.time()
            ))
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Stored evidence {evidence.id} in WORM storage")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to store evidence {evidence.id}: {e}")
            return False
    
    def retrieve_evidence(self, record_id: str) -> Optional[EvidenceRecord]:
        """Retrieve evidence record"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT id, timestamp, evidence_type, criticality, source_component,
                   event_data, context, hash_chain_previous, record_hash, pqc_signature
            FROM evidence_records WHERE id = ?
            ''', (record_id,))
            
            row = cursor.fetchone()
            conn.close()
            
            if not row:
                return None
                
            return EvidenceRecord(
                id=row[0],
                timestamp=row[1],
                evidence_type=EvidenceType(row[2]),
                criticality=CriticalityLevel(row[3]),
                source_component=row[4],
                event_data=json.loads(row[5]),
                context=json.loads(row[6]),
                hash_chain_previous=row[7],
                record_hash=row[8],
                pqc_signature=row[9]
            )
            
        except Exception as e:
            self.logger.error(f"Failed to retrieve evidence {record_id}: {e}")
            return None
    
    def query_evidence(self, evidence_type: Optional[EvidenceType] = None,
                      criticality: Optional[CriticalityLevel] = None,
                      start_time: Optional[float] = None,
                      end_time: Optional[float] = None) -> List[EvidenceRecord]:
        """Query evidence records with filters"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = '''
            SELECT id, timestamp, evidence_type, criticality, source_component,
                   event_data, context, hash_chain_previous, record_hash, pqc_signature
            FROM evidence_records WHERE 1=1
            '''
            params = []
            
            if evidence_type:
                query += " AND evidence_type = ?"
                params.append(evidence_type.value)
            
            if criticality:
                query += " AND criticality >= ?"
                params.append(criticality.value)
            
            if start_time:
                query += " AND timestamp >= ?"
                params.append(start_time)
            
            if end_time:
                query += " AND timestamp <= ?"
                params.append(end_time)
            
            query += " ORDER BY timestamp"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()
            
            records = []
            for row in rows:
                record = EvidenceRecord(
                    id=row[0],
                    timestamp=row[1],
                    evidence_type=EvidenceType(row[2]),
                    criticality=CriticalityLevel(row[3]),
                    source_component=row[4],
                    event_data=json.loads(row[5]),
                    context=json.loads(row[6]),
                    hash_chain_previous=row[7],
                    record_hash=row[8],
                    pqc_signature=row[9]
                )
                records.append(record)
            
            return records
            
        except Exception as e:
            self.logger.error(f"Failed to query evidence: {e}")
            return []

class EvidenceCollector:
    """Evidence collection agent"""
    
    def __init__(self, storage: WORMStorage, pqc_engine: PQCSigningEngine):
        self.storage = storage
        self.pqc_engine = pqc_engine
        self.logger = logging.getLogger("DET-Collector")
        
        self.collection_queue = Queue(maxsize=10000)
        self.last_hash = "GENESIS_HASH"
        self.collection_thread = None
        self.running = False
        
    def start_collection(self):
        """Start evidence collection thread"""
        if not self.running:
            self.running = True
            self.collection_thread = threading.Thread(target=self._collection_worker)
            self.collection_thread.daemon = True
            self.collection_thread.start()
            self.logger.info("Evidence collection started")
    
    def stop_collection(self):
        """Stop evidence collection"""
        self.running = False
        if self.collection_thread:
            self.collection_thread.join(timeout=5)
        self.logger.info("Evidence collection stopped")
    
    def collect_evidence(self, evidence_type: EvidenceType,
                        criticality: CriticalityLevel,
                        source_component: str,
                        event_data: Dict[str, Any],
                        context: Dict[str, Any] = None) -> str:
        """Collect evidence (async, non-blocking)"""
        
        evidence_id = f"{evidence_type.value}_{int(time.time() * 1000000)}"
        
        evidence = EvidenceRecord(
            id=evidence_id,
            timestamp=time.time(),
            evidence_type=evidence_type,
            criticality=criticality,
            source_component=source_component,
            event_data=event_data,
            context=context or {}
        )
        
        try:
            self.collection_queue.put(evidence, block=False)
            return evidence_id
        except:
            self.logger.error("Evidence collection queue full - dropping evidence")
            return ""
    
    def _collection_worker(self):
        """Background evidence processing worker"""
        while self.running:
            try:
                evidence = self.collection_queue.get(timeout=1.0)
                self._process_evidence(evidence)
                self.collection_queue.task_done()
            except Empty:
                continue
            except Exception as e:
                self.logger.error(f"Evidence processing error: {e}")
    
    def _process_evidence(self, evidence: EvidenceRecord):
        """Process and store evidence with hash chain and signatures"""
        
        # Set previous hash for chain
        evidence.hash_chain_previous = self.last_hash
        
        # Compute record hash
        hash_data = {
            "id": evidence.id,
            "timestamp": evidence.timestamp,
            "evidence_type": evidence.evidence_type.value,
            "event_data": evidence.event_data,
            "hash_chain_previous": evidence.hash_chain_previous
        }
        
        canonical_json = json.dumps(hash_data, sort_keys=True)
        evidence.record_hash = hashlib.sha256(canonical_json.encode()).hexdigest()
        
        # Update chain
        self.last_hash = evidence.record_hash
        
        # PQC sign
        evidence.pqc_signature = self.pqc_engine.sign_evidence(evidence)
        
        # Store in WORM
        success = self.storage.store_evidence(evidence)
        
        if success:
            self.logger.debug(f"Processed evidence {evidence.id}")
        else:
            self.logger.error(f"Failed to store evidence {evidence.id}")

class DETAuditEngine:
    """Audit engine for certification compliance"""
    
    def __init__(self, storage: WORMStorage, pqc_engine: PQCSigningEngine):
        self.storage = storage
        self.pqc_engine = pqc_engine
        self.logger = logging.getLogger("DET-Audit")
    
    def generate_safety_case_evidence(self, start_time: float, end_time: float) -> Dict[str, Any]:
        """Generate evidence package for safety case"""
        
        self.logger.info(f"Generating safety case evidence for period {start_time} to {end_time}")
        
        # Query critical evidence
        critical_evidence = self.storage.query_evidence(
            criticality=CriticalityLevel.SAFETY_CRITICAL,
            start_time=start_time,
            end_time=end_time
        )
        
        # Query all FDI events
        fdi_events = self.storage.query_evidence(
            evidence_type=EvidenceType.FDI_EVENT,
            start_time=start_time,
            end_time=end_time
        )
        
        # Query voter decisions
        voter_decisions = self.storage.query_evidence(
            evidence_type=EvidenceType.VOTER_DECISION,
            start_time=start_time,
            end_time=end_time
        )
        
        # Verify evidence integrity
        integrity_report = self._verify_evidence_integrity(critical_evidence + fdi_events + voter_decisions)
        
        return {
            "period": {"start": start_time, "end": end_time},
            "critical_evidence_count": len(critical_evidence),
            "fdi_events_count": len(fdi_events),
            "voter_decisions_count": len(voter_decisions),
            "integrity_verified": integrity_report["all_valid"],
            "integrity_details": integrity_report,
            "evidence_package": {
                "critical": [asdict(e) for e in critical_evidence],
                "fdi": [asdict(e) for e in fdi_events],
                "voter": [asdict(e) for e in voter_decisions]
            }
        }
    
    def _verify_evidence_integrity(self, evidence_list: List[EvidenceRecord]) -> Dict[str, Any]:
        """Verify evidence integrity and PQC signatures"""
        
        total_records = len(evidence_list)
        valid_signatures = 0
        hash_chain_valid = True
        
        previous_hash = None
        
        for evidence in sorted(evidence_list, key=lambda e: e.timestamp):
            # Verify PQC signature
            if self.pqc_engine.verify_signature(evidence, evidence.pqc_signature):
                valid_signatures += 1
            
            # Verify hash chain (simplified - in production would be more complex)
            if previous_hash and evidence.hash_chain_previous != previous_hash:
                hash_chain_valid = False
            
            previous_hash = evidence.record_hash
        
        return {
            "all_valid": (valid_signatures == total_records) and hash_chain_valid,
            "total_records": total_records,
            "valid_signatures": valid_signatures,
            "signature_rate": valid_signatures / total_records if total_records > 0 else 0,
            "hash_chain_valid": hash_chain_valid
        }

class DETManager:
    """Main DET system manager"""
    
    def __init__(self, storage_path: str = "./det_storage"):
        self.storage = WORMStorage(storage_path)
        self.pqc_engine = PQCSigningEngine()
        self.collector = EvidenceCollector(self.storage, self.pqc_engine)
        self.audit_engine = DETAuditEngine(self.storage, self.pqc_engine)
        
        self.logger = logging.getLogger("DET-Manager")
        
    def start(self):
        """Start DET system"""
        self.collector.start_collection()
        self.logger.info("DET system started")
    
    def stop(self):
        """Stop DET system"""
        self.collector.stop_collection()
        self.logger.info("DET system stopped")
    
    def log_evidence(self, evidence_type: EvidenceType,
                    criticality: CriticalityLevel,
                    source_component: str,
                    event_data: Dict[str, Any],
                    context: Dict[str, Any] = None) -> str:
        """Log evidence (main interface)"""
        return self.collector.collect_evidence(
            evidence_type, criticality, source_component, event_data, context
        )
    
    def get_evidence(self, record_id: str) -> Optional[EvidenceRecord]:
        """Retrieve evidence record"""
        return self.storage.retrieve_evidence(record_id)
    
    def generate_audit_report(self, hours_back: int = 24) -> Dict[str, Any]:
        """Generate audit report for recent period"""
        end_time = time.time()
        start_time = end_time - (hours_back * 3600)
        
        return self.audit_engine.generate_safety_case_evidence(start_time, end_time)

# Example usage
def main():
    logging.basicConfig(level=logging.INFO)
    
    det = DETManager()
    det.start()
    
    # Log some example evidence
    evidence_id = det.log_evidence(
        EvidenceType.VOTER_DECISION,
        CriticalityLevel.SAFETY_CRITICAL,
        "ACT-Voter",
        {
            "job_id": "flight_control_001",
            "vote_result": "unanimous",
            "cpu_result": "0x1234",
            "fpga_result": "0x1234",
            "dsp_result": "0x1234"
        },
        {"flight_phase": "cruise", "altitude_m": 10000}
    )
    
    print(f"Logged evidence: {evidence_id}")
    
    # Wait a moment for processing
    import time
    time.sleep(0.1)
    
    # Retrieve evidence
    evidence = det.get_evidence(evidence_id)
    if evidence:
        print(f"Retrieved evidence: {evidence.id}")
        print(f"Hash: {evidence.record_hash}")
        print(f"PQC Signature: {evidence.pqc_signature[:32]}...")
    
    # Generate audit report
    audit_report = det.generate_audit_report()
    print(f"Audit report: {audit_report['critical_evidence_count']} critical records")
    
    det.stop()

if __name__ == "__main__":
    main()