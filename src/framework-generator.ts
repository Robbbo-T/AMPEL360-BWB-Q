/**
 * Core framework generator implementation
 */

import { FrameworkNode, ParsedFrameworkItem, FrameworkGeneratorOptions, FrameworkDomain } from './types';
import { parseFrameworkText, generateDescription, extractDomainFromText } from './parser';

/**
 * Create a framework node from parsed data
 */
export function createNode(
  id: string, 
  name: string, 
  description: string, 
  type: 'folder' | 'file' = 'folder', 
  children?: FrameworkNode[]
): FrameworkNode {
  return { id, name, type, description, children };
}

/**
 * Build hierarchical tree from parsed framework items
 */
export function buildFrameworkTree(
  items: ParsedFrameworkItem[], 
  domain: FrameworkDomain,
  options: FrameworkGeneratorOptions = { includeFolders: true, includeDescriptions: true }
): FrameworkNode[] {
  const nodes: FrameworkNode[] = [];
  const caNodes = new Map<string, FrameworkNode>();
  
  // First pass: create CA nodes
  const caItems = items.filter(item => item.level === 'CA');
  for (const caItem of caItems) {
    const description = options.includeDescriptions 
      ? generateDescription(caItem.name, caItem.id)
      : caItem.name;
    
    const caNode = createNode(
      caItem.id,
      caItem.name,
      description,
      'folder',
      []
    );
    
    caNodes.set(caItem.id, caNode);
    nodes.push(caNode);
  }
  
  // Second pass: create CI nodes and attach to CAs
  const ciItems = items.filter(item => item.level === 'CI');
  for (const ciItem of ciItems) {
    const description = options.includeDescriptions
      ? generateDescription(ciItem.name, ciItem.id)
      : ciItem.name;
    
    const ciNode = createNode(
      ciItem.id,
      ciItem.name,
      description,
      'folder'
    );
    
    // Find parent CA by matching the pattern
    if (ciItem.parentId) {
      let parentCA: FrameworkNode | undefined;
      
      // If parentId is a pattern (ends with -), find matching CA
      if (ciItem.parentId.endsWith('-')) {
        for (const [caId, caNode] of caNodes.entries()) {
          if (caId.startsWith(ciItem.parentId)) {
            parentCA = caNode;
            break;
          }
        }
      } else {
        // Direct match
        parentCA = caNodes.get(ciItem.parentId);
      }
      
      if (parentCA && parentCA.children) {
        parentCA.children.push(ciNode);
      }
    }
  }
  
  return nodes;
}

/**
 * Generate complete framework structure from text data
 */
export function generateFrameworkStructure(
  organizationalText: string,
  proceduralText: string,
  intelligentText: string,
  machineText: string,
  executingText: string,
  technicalDomainsTexts: string[],
  options: FrameworkGeneratorOptions = { includeFolders: true, includeDescriptions: true }
): FrameworkNode {
  
  // Parse organizational structure
  const orgItems = parseFrameworkText(organizationalText, 'O-ORGANIZATIONAL');
  const orgTree = buildFrameworkTree(orgItems, 'O-ORGANIZATIONAL', options);
  const orgNode = createNode(
    'O-ORGANIZATIONAL',
    'Organizational',
    'Governance, financial control, strategic management, org structures',
    'folder',
    orgTree
  );
  
  // Parse procedural structure
  const procItems = parseFrameworkText(proceduralText, 'P-PROCEDURAL');
  const procTree = buildFrameworkTree(procItems, 'P-PROCEDURAL', options);
  const procNode = createNode(
    'P-PROCEDURAL',
    'Procedural',
    'Processes, workflows, phase gates, enterprise standards',
    'folder',
    procTree
  );
  
  // Parse intelligent structure
  const intItems = parseFrameworkText(intelligentText, 'I-INTELLIGENT');
  const intTree = buildFrameworkTree(intItems, 'I-INTELLIGENT', options);
  const intNode = createNode(
    'I-INTELLIGENT',
    'Intelligent',
    'AI models, optimizers, predictive analytics, decision support',
    'folder',
    intTree
  );
  
  // Parse machine structure
  const machItems = parseFrameworkText(machineText, 'M-MACHINE');
  const machTree = buildFrameworkTree(machItems, 'M-MACHINE', options);
  const machNode = createNode(
    'M-MACHINE',
    'Machine',
    'Simulation, digital twins, co-simulation, HIL testing',
    'folder',
    machTree
  );
  
  // Parse executing structure
  const execItems = parseFrameworkText(executingText, 'E-EXECUTING');
  const execTree = buildFrameworkTree(execItems, 'E-EXECUTING', options);
  const execNode = createNode(
    'E-EXECUTING',
    'Executing',
    'Execution orchestration, deployment automation, runtime monitoring',
    'folder',
    execTree
  );
  
  // Parse technical domains
  const technicalNodes: FrameworkNode[] = [];
  const domainNames = [
    'Architectures Airframes Aerodynamics',
    'Mechanical and Control',
    'Environmental Remediation Circularity',
    'Defence Cybersecurity Safety',
    'Energy and Renewable',
    'Operating Systems Navigation HPC'
  ];
  
  for (let i = 0; i < technicalDomainsTexts.length && i < domainNames.length; i++) {
    const domain = extractDomainFromText(technicalDomainsTexts[i]);
    if (domain) {
      const items = parseFrameworkText(technicalDomainsTexts[i], domain);
      const tree = buildFrameworkTree(items, domain, options);
      const node = createNode(
        domain,
        domainNames[i],
        `Technical domain: ${domainNames[i]}`,
        'folder',
        tree
      );
      technicalNodes.push(node);
    }
  }
  
  const technicalNode = createNode(
    'T-TECHNOLOGICAL',
    'Technological',
    'Technical architecture, CAs/CIs, UTCS artifacts',
    'folder',
    technicalNodes
  );
  
  // Create root framework node
  const rootNode = createNode(
    'AMPEL360-H2-BWB-Q',
    'AMPEL360 H₂-BWB-Q Framework',
    'Enterprise-grade framework for AMPEL360 H₂-BWB-Q aircraft configuration optimization',
    'folder',
    [orgNode, procNode, technicalNode, intNode, machNode, execNode]
  );
  
  return rootNode;
}

/**
 * Convert framework tree to JSON string
 */
export function frameworkToJSON(framework: FrameworkNode, indent: number = 2): string {
  return JSON.stringify(framework, null, indent);
}

/**
 * Count total nodes in framework tree
 */
export function countNodes(node: FrameworkNode): number {
  let count = 1;
  if (node.children) {
    for (const child of node.children) {
      count += countNodes(child);
    }
  }
  return count;
}

/**
 * Find node by ID in framework tree
 */
export function findNodeById(node: FrameworkNode, id: string): FrameworkNode | null {
  if (node.id === id) {
    return node;
  }
  
  if (node.children) {
    for (const child of node.children) {
      const found = findNodeById(child, id);
      if (found) {
        return found;
      }
    }
  }
  
  return null;
}

/**
 * Get all node IDs at a specific depth
 */
export function getNodesAtDepth(node: FrameworkNode, targetDepth: number, currentDepth: number = 0): string[] {
  if (currentDepth === targetDepth) {
    return [node.id];
  }
  
  const ids: string[] = [];
  if (node.children && currentDepth < targetDepth) {
    for (const child of node.children) {
      ids.push(...getNodesAtDepth(child, targetDepth, currentDepth + 1));
    }
  }
  
  return ids;
}