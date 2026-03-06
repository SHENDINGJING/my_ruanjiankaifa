#!/usr/bin/env node

/**
 * Self-Reflection Tool for OpenClaw Agents
 * 
 * This script helps agents review their recent work and identify
 * areas for improvement.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Get today's date for memory file
const today = new Date().toISOString().split('T')[0];
const memoryDir = path.join(process.cwd(), 'memory');
const memoryFile = path.join(memoryDir, `${today}.md`);
const longTermMemory = path.join(process.cwd(), 'MEMORY.md');

// Ensure memory directory exists
if (!fs.existsSync(memoryDir)) {
  fs.mkdirSync(memoryDir, { recursive: true });
}

// Check recent git commits or file changes
function getRecentChanges() {
  try {
    // Try to get recent git commits
    const commits = execSync('git log --oneline -5', { encoding: 'utf8' });
    return `Recent commits:\n${commits}`;
  } catch (e) {
    // If not a git repo or other error, check recent file modifications
    const files = execSync('dir /od /tw', { encoding: 'utf8' });
    return `Recent file changes:\n${files}`;
  }
}

// Self-reflection prompts
const prompts = [
  "What did I accomplish recently?",
  "What mistakes did I make, and what did I learn from them?",
  "What could I have done better or more efficiently?",
  "What new knowledge or skills did I gain?",
  "What should I remember for future similar tasks?",
  "What processes or workflows could be improved?",
];

function conductSelfReflection() {
  console.log('🤔 Conducting self-reflection...\n');
  
  const changes = getRecentChanges();
  console.log(changes + '\n');
  
  console.log('Reflection Questions:');
  prompts.forEach((prompt, i) => {
    console.log(`${i + 1}. ${prompt}`);
  });
  
  console.log('\n---\n');
  console.log('Take a moment to reflect on these questions.');
  console.log('Consider updating:');
  console.log(`1. ${memoryFile} - Daily learnings`);
  console.log(`2. ${longTermMemory} - Important long-term knowledge`);
  console.log('3. Relevant skill files - Improved procedures');
  console.log('4. TOOLS.md - New tools or techniques');
}

// Run if called directly
if (require.main === module) {
  conductSelfReflection();
}

module.exports = { conductSelfReflection, prompts };