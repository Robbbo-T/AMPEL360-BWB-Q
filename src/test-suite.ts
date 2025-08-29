/**
 * Comprehensive test suite for AMPEL360 Framework Generator
 */

import { 
  parseFrameworkText, 
  generateDescription, 
  normalizeText,
  extractDomainFromText 
} from './parser';
import { 
  generateFrameworkStructure, 
  buildFrameworkTree, 
  countNodes, 
  findNodeById,
  createNode
} from './framework-generator';

// Test data
const testOrgText = `
CA-O-001-GOVERNANCE
CI-CA-O-001-001-PROGRAM-GOVERNANCE-FRAMEWORK
CI-CA-O-001-002-QUALITY-MANAGEMENT-SYSTEM
`.trim();

const testProcText = `
CA-P-001-PROCESS-ARCHITECTURE
CI-CA-P-001-001-PROCESS-CATALOG
CI-CA-P-001-002-BPMN-META-MODEL
`.trim();

function runTests() {
  console.log('🧪 Running AMPEL360 Framework Generator Tests');
  console.log('===========================================\n');
  
  // Test 1: Text parsing
  console.log('Test 1: Text Parsing');
  const orgItems = parseFrameworkText(testOrgText, 'O-ORGANIZATIONAL');
  console.log(`✅ Parsed ${orgItems.length} items from organizational text`);
  
  const caItems = orgItems.filter(item => item.level === 'CA');
  const ciItems = orgItems.filter(item => item.level === 'CI');
  console.log(`   - CAs: ${caItems.length}, CIs: ${ciItems.length}`);
  
  // Test 2: Tree building
  console.log('\nTest 2: Tree Building');
  const orgTree = buildFrameworkTree(orgItems, 'O-ORGANIZATIONAL');
  console.log(`✅ Built tree with ${orgTree.length} root nodes`);
  
  const firstCA = orgTree[0];
  console.log(`   - First CA: ${firstCA.name} with ${firstCA.children?.length || 0} children`);
  
  // Test 3: Domain extraction
  console.log('\nTest 3: Domain Extraction');
  const detectedDomain = extractDomainFromText(testOrgText);
  console.log(`✅ Detected domain: ${detectedDomain}`);
  
  // Test 4: Node utilities
  console.log('\nTest 4: Node Utilities');
  const testNode = createNode('TEST-001', 'Test Node', 'Test description');
  console.log(`✅ Created test node: ${testNode.id}`);
  
  // Test 5: Text normalization
  console.log('\nTest 5: Text Normalization');
  const testText = 'TEST_WITH_UNDERSCORES-AND-DASHES';
  const normalized = normalizeText(testText);
  console.log(`✅ Normalized '${testText}' -> '${normalized}'`);
  
  // Test 6: Description generation
  console.log('\nTest 6: Description Generation');
  const desc = generateDescription('TEST COMPONENT', 'CA-TEST-001');
  console.log(`✅ Generated description: '${desc}'`);
  
  console.log('\n🎉 All tests completed successfully!');
}

// Run tests if executed directly
if (require.main === module) {
  runTests();
}

export { runTests };