/**
 * Test script to debug the CI parsing
 */

import { parseFrameworkText } from './parser';

const testText = `
CA-O-001-GOVERNANCE
CI-CA-O-001-001-PROGRAM-GOVERNANCE-FRAMEWORK
CI-CA-O-001-002-QUALITY-MANAGEMENT-SYSTEM
CI-CA-O-001-003-CERTIFICATION-ROADMAP
`.trim();

console.log('Testing CI parsing:');
const items = parseFrameworkText(testText, 'O-ORGANIZATIONAL');

for (const item of items) {
  console.log(`${item.level}: ${item.id} -> ${item.name} (parent: ${item.parentId || 'none'})`);
}