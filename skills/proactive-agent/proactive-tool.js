#!/usr/bin/env node

/**
 * Proactive Agent Tool
 * 
 * Helps develop and maintain proactive behaviors.
 * Based on halthelobster/proactive-agent concept.
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

// Create interface for user input
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Proactive prompts and exercises
const proactiveExercises = [
  {
    name: "Morning Anticipation",
    question: "Looking at today's date and context, what needs might arise today?",
    prompts: [
      "Are there any meetings or deadlines?",
      "What ongoing projects need attention?",
      "What information might be needed?",
      "What follow-ups are pending?"
    ]
  },
  {
    name: "Pattern Recognition",
    question: "What patterns have you noticed in recent requests or tasks?",
    prompts: [
      "What tasks recur frequently?",
      "What information is often requested?",
      "What problems keep happening?",
      "What solutions work consistently?"
    ]
  },
  {
    name: "Initiative Assessment",
    question: "Where could you take more initiative right now?",
    prompts: [
      "What tasks are waiting for explicit instruction?",
      "What information could be prepared in advance?",
      "What processes could be improved?",
      "What learning could happen proactively?"
    ]
  },
  {
    name: "Continuous Improvement",
    question: "How can you improve based on recent experience?",
    prompts: [
      "What worked well that should be repeated?",
      "What didn't work that should be changed?",
      "What new skills would be helpful?",
      "What knowledge gaps need filling?"
    ]
  }
];

// Main function
async function runProactiveSession() {
  console.log('🚀 Proactive Agent Development Session\n');
  console.log('Goal: Transform from reactive to proactive mindset\n');
  
  const date = new Date().toISOString().split('T')[0];
  const logFile = path.join(process.cwd(), 'memory', `proactive-${date}.md`);
  
  let sessionLog = `# Proactive Session - ${date}\n\n`;
  
  for (const exercise of proactiveExercises) {
    console.log(`\n## ${exercise.name}`);
    console.log(exercise.question);
    
    exercise.prompts.forEach((prompt, i) => {
      console.log(`  ${i + 1}. ${prompt}`);
    });
    
    sessionLog += `## ${exercise.name}\n`;
    sessionLog += `**Question**: ${exercise.question}\n\n`;
    
    // Get user input for each prompt
    for (let i = 0; i < exercise.prompts.length; i++) {
      const prompt = exercise.prompts[i];
      await new Promise((resolve) => {
        rl.question(`\n${i + 1}. ${prompt}\nYour response: `, (answer) => {
          sessionLog += `**${prompt}**\n${answer}\n\n`;
          resolve();
        });
      });
    }
  }
  
  // Save session log
  const memoryDir = path.join(process.cwd(), 'memory');
  if (!fs.existsSync(memoryDir)) {
    fs.mkdirSync(memoryDir, { recursive: true });
  }
  
  fs.writeFileSync(logFile, sessionLog);
  console.log(`\n✅ Session saved to: ${logFile}`);
  
  // Generate proactive action plan
  console.log('\n📋 Suggested Proactive Actions:');
  console.log('1. Review the session notes and identify 1-2 proactive behaviors to implement');
  console.log('2. Set specific, measurable goals for proactive actions');
  console.log('3. Schedule regular proactive review sessions');
  console.log('4. Track the impact of proactive behaviors');
  console.log('5. Share insights and improvements with others');
  
  rl.close();
}

// Run if called directly
if (require.main === module) {
  runProactiveSession().catch(console.error);
}

module.exports = {
  proactiveExercises,
  runProactiveSession
};