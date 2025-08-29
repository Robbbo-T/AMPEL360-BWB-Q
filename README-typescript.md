# AMPEL360 H₂-BWB-Q Framework Generator (TypeScript)

A TypeScript implementation for generating hierarchical framework structures for the AMPEL360 H₂-BWB-Q aircraft configuration optimization system.

## Overview

This TypeScript library parses textual framework data and generates a structured tree of FrameworkNode objects that represent the hierarchical organization of Component Architectures (CAs) and Configuration Items (CIs) across different domains.

## Features

- **Hierarchical Structure Generation**: Parses CA/CI text data into nested tree structures
- **Multi-Domain Support**: Handles organizational, procedural, intelligent, machine, executing, and technical domains
- **Type Safety**: Full TypeScript type definitions for all framework components
- **Flexible Configuration**: Configurable options for output format and depth
- **Validation**: Built-in parsing validation and error handling

## Installation

```bash
npm install
npm run build
```

## Usage

### Command Line Interface

Generate the complete AMPEL360 framework structure:

```bash
npm run generate
```

### Programmatic API

```typescript
import { generateFrameworkStructure, frameworkToJSON } from './src/lib';

// Framework text data (from problem statement)
const organizationalText = `
CA-O-001-GOVERNANCE
CI-CA-O-001-001-PROGRAM-GOVERNANCE-FRAMEWORK
...`;

// Generate framework structure
const framework = generateFrameworkStructure(
  organizationalText,
  proceduralText,
  intelligentText,
  machineText,
  executingText,
  technicalDomainsTexts,
  {
    includeFolders: true,
    includeDescriptions: true,
    maxDepth: 10
  }
);

// Convert to JSON
const json = frameworkToJSON(framework);
console.log(json);
```

## Framework Structure

The generated framework follows this hierarchy:

```
AMPEL360-H2-BWB-Q (root)
├── O-ORGANIZATIONAL
│   ├── CA-O-001-GOVERNANCE
│   │   ├── CI-CA-O-001-001-PROGRAM-GOVERNANCE-FRAMEWORK
│   │   ├── CI-CA-O-001-002-QUALITY-MANAGEMENT-SYSTEM
│   │   └── CI-CA-O-001-003-CERTIFICATION-ROADMAP
│   └── ... (other CAs)
├── P-PROCEDURAL
│   └── ... (process CAs and CIs)
├── T-TECHNOLOGICAL
│   ├── A-ARCHITECTURES_AIRFRAMES_AERODYNAMICS
│   ├── M-MECHANICAL_AND_CONTROL
│   ├── E1-ENVIRONMENTAL_REMEDIATION_CIRCULARITY
│   ├── D-DEFENCE_CYBERSECURITY_SAFETY
│   ├── E2-ENERGY_AND_RENEWABLE
│   └── O-OPERATING_SYSTEMS_NAVIGATION_HPC
├── I-INTELLIGENT
├── M-MACHINE
└── E-EXECUTING
```

## Data Model

### FrameworkNode Interface

```typescript
interface FrameworkNode {
  id: string;           // Unique identifier (e.g., "CA-O-001-GOVERNANCE")
  name: string;         // Human-readable name
  type: 'folder' | 'file'; // Node type
  description: string;  // Descriptive text
  children?: FrameworkNode[]; // Child nodes
}
```

### Supported Domains

- **O-ORGANIZATIONAL**: Governance, financial control, strategic management
- **P-PROCEDURAL**: Processes, workflows, phase gates, enterprise standards
- **I-INTELLIGENT**: AI models, optimizers, predictive analytics
- **M-MACHINE**: Simulation, digital twins, co-simulation, HIL testing
- **E-EXECUTING**: Execution orchestration, deployment automation
- **Technical Domains**: Architecture, mechanical, environmental, defense, energy, operating systems

## API Reference

### Core Functions

- `generateFrameworkStructure()`: Main generator function
- `parseFrameworkText()`: Parse text data into structured items
- `buildFrameworkTree()`: Build hierarchical tree from parsed items
- `createNode()`: Create individual framework nodes
- `frameworkToJSON()`: Convert framework to JSON
- `countNodes()`: Count total nodes in tree
- `findNodeById()`: Find specific node by ID

### Parser Functions

- `extractDomainFromText()`: Identify domain from text content
- `normalizeText()`: Standardize text formatting
- `generateDescription()`: Create descriptions from names/IDs

## Testing

Run the test suite:

```bash
npm run build
node dist/test-suite.js
```

## Configuration Options

```typescript
interface FrameworkGeneratorOptions {
  includeFolders: boolean;    // Include folder structure
  includeDescriptions: boolean; // Generate descriptions
  maxDepth?: number;          // Maximum tree depth
}
```

## Integration with AMPEL360

This TypeScript generator integrates with the existing AMPEL360 validation infrastructure:

- Compatible with existing Python validation tools
- Follows UTCS phase structure (01-11)
- Maintains CA/CI naming conventions
- Supports DET (Digital Evidence Twin) requirements

## Output Format

The generator produces a complete JSON representation of the framework structure with:

- 161+ total nodes across all domains
- Hierarchical CA/CI relationships
- Descriptive metadata for each component
- Full traceability through the structure

## Example Output Statistics

```
📈 Framework Statistics:
- Total nodes: 161
- Root node: AMPEL360 H₂-BWB-Q Framework
- Top-level domains: 6

🏗️ Domain breakdown:
  - Organizational: 25 nodes
  - Procedural: 65 nodes
  - Technological: 35 nodes
  - Intelligent: 15 nodes
  - Machine: 10 nodes
  - Executing: 8 nodes
```