/**
 * Utility functions for parsing AMPEL360 framework structure text data
 */

import { FrameworkData, ParsedFrameworkItem, FrameworkDomain } from './types';

/**
 * Parse a CA/CI text block and extract hierarchical structure
 */
export function parseFrameworkText(text: string, domain: FrameworkDomain): ParsedFrameworkItem[] {
  const lines = text.trim().split('\n').filter(line => line.trim().length > 0);
  const items: ParsedFrameworkItem[] = [];
  
  for (const line of lines) {
    const trimmedLine = line.trim();
    
    // Skip empty lines and comments
    if (!trimmedLine || trimmedLine.startsWith('#')) {
      continue;
    }
    
    // Parse CA (Component Architecture) lines
    if (trimmedLine.startsWith('CA-')) {
      const parts = trimmedLine.split('-');
      if (parts.length >= 3) {
        const id = trimmedLine;
        const name = parts.slice(3).join('-').replace(/_/g, ' ');
        
        items.push({
          level: 'CA',
          id,
          name,
        });
      }
    }
    
    // Parse CI (Configuration Item) lines
    else if (trimmedLine.startsWith('CI-')) {
      const parts = trimmedLine.split('-');
      if (parts.length >= 5) {
        const id = trimmedLine;
        const name = parts.slice(5).join('-').replace(/_/g, ' ');
        
        // Extract parent CA ID (CI-CA-X-YYY-ZZZ-... -> CA-X-YYY-...)
        // Find the corresponding CA by matching the pattern CI-CA-<domain>-<id>-<name>
        const ciParts = id.split('-');
        if (ciParts.length >= 5) {
          // For CI-CA-O-001-001-PROGRAM-..., parent should be CA-O-001-GOVERNANCE
          // We need to reconstruct the full CA name from the CI parts
          const domain = ciParts[2]; // O
          const caNum = ciParts[3];   // 001
          
          // Create potential parent ID pattern to match against existing CAs
          const parentIdPattern = `CA-${domain}-${caNum}-`;
          
          items.push({
            level: 'CI',
            id,
            name,
            parentId: parentIdPattern, // We'll resolve this later
          });
        }
      }
    }
  }
  
  return items;
}

/**
 * Extract domain identifier from text context
 */
export function extractDomainFromText(text: string): FrameworkDomain | null {
  const upperText = text.toUpperCase();
  
  if (upperText.includes('CA-O-') || upperText.includes('GOVERNANCE') || upperText.includes('ORGANIZATIONAL')) {
    return 'O-ORGANIZATIONAL';
  }
  if (upperText.includes('CA-P-') || upperText.includes('PROCESS') || upperText.includes('PROCEDURAL')) {
    return 'P-PROCEDURAL';
  }
  if (upperText.includes('CA-I-') || upperText.includes('INTELLIGENT') || upperText.includes('AUTONOMY')) {
    return 'I-INTELLIGENT';
  }
  if (upperText.includes('CA-M-') || upperText.includes('MACHINE') || upperText.includes('AUTOMATION')) {
    return 'M-MACHINE';
  }
  if (upperText.includes('CA-E-') || upperText.includes('EXECUTING') || upperText.includes('RUNTIME')) {
    return 'E-EXECUTING';
  }
  if (upperText.includes('CA-A-') || upperText.includes('ARCHITECTURE') || upperText.includes('AIRFRAME')) {
    return 'A-ARCHITECTURES_AIRFRAMES_AERODYNAMICS';
  }
  if (upperText.includes('MECHANICAL') || upperText.includes('CONTROL') || upperText.includes('HYDRAULIC')) {
    return 'M-MECHANICAL_AND_CONTROL';
  }
  if (upperText.includes('ENVIRONMENTAL') || upperText.includes('REMEDIATION') || upperText.includes('CIRCULARITY')) {
    return 'E1-ENVIRONMENTAL_REMEDIATION_CIRCULARITY';
  }
  if (upperText.includes('DEFENCE') || upperText.includes('CYBERSECURITY') || upperText.includes('SAFETY')) {
    return 'D-DEFENCE_CYBERSECURITY_SAFETY';
  }
  if (upperText.includes('ENERGY') || upperText.includes('RENEWABLE') || upperText.includes('POWER')) {
    return 'E2-ENERGY_AND_RENEWABLE';
  }
  if (upperText.includes('OPERATING') || upperText.includes('NAVIGATION') || upperText.includes('HPC')) {
    return 'O-OPERATING_SYSTEMS_NAVIGATION_HPC';
  }
  
  return null;
}

/**
 * Normalize text by removing extra whitespace and standardizing format
 */
export function normalizeText(text: string): string {
  return text
    .trim()
    .replace(/_/g, ' ')
    .replace(/-/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

/**
 * Generate a description from a name/ID
 */
export function generateDescription(name: string, id: string): string {
  const normalizedName = normalizeText(name);
  
  if (id.startsWith('CA-')) {
    return `Component Architecture: ${normalizedName}`;
  } else if (id.startsWith('CI-')) {
    return `Configuration Item: ${normalizedName}`;
  }
  
  return normalizedName;
}

/**
 * Extract hierarchical level from ID
 */
export function getHierarchyLevel(id: string): number {
  const parts = id.split('-');
  return parts.length;
}