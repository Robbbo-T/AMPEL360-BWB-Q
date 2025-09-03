/**
 * TypeScript types and interfaces for AMPEL360 H₂-BWB-Q Framework Structure
 */

export interface FrameworkNode {
  id: string;
  name: string;
  type: 'folder' | 'file';
  description: string;
  children?: FrameworkNode[];
}

export interface ComponentArchitecture {
  id: string;
  name: string;
  description: string;
  configurationItems: ConfigurationItem[];
}

export interface ConfigurationItem {
  id: string;
  name: string;
  description: string;
  parentCA: string;
  utcsPhases?: UTCSPhase[];
}

export interface UTCSPhase {
  phase: string;
  name: string;
  artifacts: string[];
}

export type FrameworkDomain = 
  | 'O-ORGANIZATIONAL'
  | 'P-PROCEDURAL' 
  | 'I-INTELLIGENT'
  | 'M-MACHINE'
  | 'E-EXECUTING'
  | 'A-ARCHITECTURES_AIRFRAMES_AERODYNAMICS'
  | 'M-MECHANICAL_AND_CONTROL'
  | 'E1-ENVIRONMENTAL_REMEDIATION_CIRCULARITY'
  | 'D-DEFENCE_CYBERSECURITY_SAFETY'
  | 'E2-ENERGY_AND_RENEWABLE'
  | 'O-OPERATING_SYSTEMS_NAVIGATION_HPC';

export interface FrameworkData {
  domain: FrameworkDomain;
  items: string[];
}

export interface ParsedFrameworkItem {
  level: 'CA' | 'CI';
  id: string;
  name: string;
  parentId?: string;
}

export interface FrameworkGeneratorOptions {
  includeFolders: boolean;
  includeDescriptions: boolean;
  maxDepth?: number;
}