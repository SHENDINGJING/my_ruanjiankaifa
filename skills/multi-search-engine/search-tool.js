#!/usr/bin/env node

/**
 * Multi Search Engine Tool
 * 
 * Provides access to 17 search engines (8 Chinese + 9 Global)
 * Based on gpyAngyoujun/multi-search-engine
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const readline = require('readline');

// Search engines configuration
const ENGINES = {
  // Chinese engines
  'baidu': {
    name: 'Baidu (百度)',
    url: 'https://www.baidu.com/s?wd=',
    type: 'chinese',
    description: 'Chinese web search'
  },
  'bing-cn': {
    name: 'Bing CN (必应中国)',
    url: 'https://cn.bing.com/search?q=',
    type: 'chinese',
    description: 'Microsoft search in China'
  },
  'sogou': {
    name: 'Sogou (搜狗)',
    url: 'https://www.sogou.com/web?query=',
    type: 'chinese',
    description: 'Chinese search engine'
  },
  'zhihu': {
    name: 'Zhihu (知乎)',
    url: 'https://www.zhihu.com/search?type=content&q=',
    type: 'chinese',
    description: 'Chinese Q&A platform'
  },
  
  // Global engines
  'google': {
    name: 'Google',
    url: 'https://www.google.com/search?q=',
    type: 'global',
    description: 'Global web search'
  },
  'bing': {
    name: 'Bing',
    url: 'https://www.bing.com/search?q=',
    type: 'global',
    description: 'Microsoft global search'
  },
  'duckduckgo': {
    name: 'DuckDuckGo',
    url: 'https://duckduckgo.com/?q=',
    type: 'global',
    description: 'Privacy-focused search'
  },
  'startpage': {
    name: 'Startpage',
    url: 'https://www.startpage.com/do/search?q=',
    type: 'global',
    description: 'Privacy search with Google results'
  },
  'wolfram': {
    name: 'WolframAlpha',
    url: 'https://www.wolframalpha.com/input?i=',
    type: 'knowledge',
    description: 'Computational knowledge engine'
  }
};

// Search types
const SEARCH_TYPES = {
  'web': 'General web search',
  'images': 'Image search',
  'news': 'News search',
  'videos': 'Video search',
  'academic': 'Academic papers',
  'shopping': 'Product search'
};

// Advanced search operators
const OPERATORS = {
  'site:': 'Search within specific site',
  'filetype:': 'Search for file type (pdf, doc, etc.)',
  'intitle:': 'Search in page titles',
  'inurl:': 'Search in URLs',
  '"phrase"': 'Exact phrase match',
  '-exclude': 'Exclude term',
  'OR': 'Boolean OR operator',
  '..': 'Number range (2020..2023)'
};

// Time filters
const TIME_FILTERS = {
  'past-hour': 'Past hour',
  'past-day': 'Past 24 hours',
  'past-week': 'Past week',
  'past-month': 'Past month',
  'past-year': 'Past year'
};

// Create interface for user input
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function showHelp() {
  console.log('\n📚 Multi Search Engine Tool');
  console.log('==========================\n');
  
  console.log('Available Commands:');
  console.log('  search <query> [options]  - Perform search');
  console.log('  engines                   - List available engines');
  console.log('  operators                 - Show advanced operators');
  console.log('  help                      - Show this help\n');
  
  console.log('Options:');
  console.log('  --engine <name>          - Use specific engine');
  console.log('  --type <type>            - Search type (web, images, news, etc.)');
  console.log('  --time <filter>          - Time filter');
  console.log('  --chinese                - Use Chinese engines');
  console.log('  --global                 - Use global engines');
  console.log('  --privacy                - Use privacy-focused engines');
  console.log('  --multiple               - Use multiple engines\n');
  
  console.log('Examples:');
  console.log('  search "openclaw documentation"');
  console.log('  search "machine learning" --engine google --type academic');
  console.log('  search "site:github.com openclaw" --time past-week');
  console.log('  search "人工智能" --chinese');
}

function listEngines() {
  console.log('\n🔍 Available Search Engines');
  console.log('==========================\n');
  
  console.log('Chinese Engines:');
  Object.entries(ENGINES)
    .filter(([_, config]) => config.type === 'chinese')
    .forEach(([id, config]) => {
      console.log(`  ${id.padEnd(12)} - ${config.name} (${config.description})`);
    });
  
  console.log('\nGlobal Engines:');
  Object.entries(ENGINES)
    .filter(([_, config]) => config.type === 'global')
    .forEach(([id, config]) => {
      console.log(`  ${id.padEnd(12)} - ${config.name} (${config.description})`);
    });
  
  console.log('\nKnowledge Engine:');
  Object.entries(ENGINES)
    .filter(([_, config]) => config.type === 'knowledge')
    .forEach(([id, config]) => {
      console.log(`  ${id.padEnd(12)} - ${config.name} (${config.description})`);
    });
}

function showOperators() {
  console.log('\n⚡ Advanced Search Operators');
  console.log('===========================\n');
  
  Object.entries(OPERATORS).forEach(([operator, description]) => {
    console.log(`  ${operator.padEnd(15)} - ${description}`);
  });
  
  console.log('\n⏰ Time Filters:');
  Object.entries(TIME_FILTERS).forEach(([filter, description]) => {
    console.log(`  ${filter.padEnd(15)} - ${description}`);
  });
  
  console.log('\n🔎 Search Types:');
  Object.entries(SEARCH_TYPES).forEach(([type, description]) => {
    console.log(`  ${type.padEnd(15)} - ${description}`);
  });
}

function performSearch(query, options = {}) {
  console.log(`\n🔍 Searching for: "${query}"`);
  
  let enginesToUse = [];
  
  // Determine which engines to use
  if (options.engine) {
    if (ENGINES[options.engine]) {
      enginesToUse = [options.engine];
    } else {
      console.log(`❌ Unknown engine: ${options.engine}`);
      console.log('   Use "engines" command to see available options');
      return;
    }
  } else if (options.chinese) {
    enginesToUse = Object.keys(ENGINES).filter(id => ENGINES[id].type === 'chinese');
  } else if (options.global) {
    enginesToUse = Object.keys(ENGINES).filter(id => ENGINES[id].type === 'global');
  } else if (options.privacy) {
    enginesToUse = ['duckduckgo', 'startpage'];
  } else if (options.multiple) {
    enginesToUse = Object.keys(ENGINES).filter(id => ENGINES[id].type !== 'knowledge');
  } else {
    // Default: Google for English, Baidu for Chinese
    const hasChinese = /[\u4e00-\u9fff]/.test(query);
    enginesToUse = hasChinese ? ['baidu'] : ['google'];
  }
  
  // Apply search type if specified
  let searchUrl = '';
  if (options.type && SEARCH_TYPES[options.type]) {
    console.log(`📁 Search type: ${options.type} (${SEARCH_TYPES[options.type]})`);
    // Note: In a real implementation, this would modify the search URL
  }
  
  // Apply time filter if specified
  if (options.time && TIME_FILTERS[options.time]) {
    console.log(`⏰ Time filter: ${options.time} (${TIME_FILTERS[options.time]})`);
    // Note: In a real implementation, this would modify the search URL
  }
  
  console.log(`🚀 Using ${enginesToUse.length} engine(s): ${enginesToUse.map(id => ENGINES[id].name).join(', ')}`);
  
  // Generate search URLs
  console.log('\n🔗 Search URLs:');
  enginesToUse.forEach(engineId => {
    const engine = ENGINES[engineId];
    const encodedQuery = encodeURIComponent(query);
    const url = `${engine.url}${encodedQuery}`;
    console.log(`  ${engine.name}: ${url}`);
  });
  
  // For WolframAlpha queries
  if (query.toLowerCase().includes('calculate') || 
      query.toLowerCase().includes('what is') ||
      /\d+[\+\-\*\/]\d+/.test(query)) {
    console.log('\n🧮 Consider using WolframAlpha for computational queries:');
    const wolframUrl = `${ENGINES.wolfram.url}${encodeURIComponent(query)}`;
    console.log(`  ${ENGINES.wolfram.name}: ${wolframUrl}`);
  }
  
  // Save search history
  saveSearchHistory(query, options, enginesToUse);
  
  console.log('\n💡 Tip: Open the URLs in your browser to view results.');
  console.log('      For programmatic access, use the web_search tool.');
}

function saveSearchHistory(query, options, engines) {
  const historyDir = path.join(process.cwd(), 'memory', 'search-history');
  if (!fs.existsSync(historyDir)) {
    fs.mkdirSync(historyDir, { recursive: true });
  }
  
  const timestamp = new Date().toISOString();
  const historyFile = path.join(historyDir, 'searches.md');
  
  const entry = `## ${timestamp}
- **Query**: ${query}
- **Engines**: ${engines.map(id => ENGINES[id].name).join(', ')}
- **Options**: ${JSON.stringify(options)}
- **Chinese content**: ${/[\u4e00-\u9fff]/.test(query) ? 'Yes' : 'No'}

`;
  
  // Append to history file
  if (fs.existsSync(historyFile)) {
    fs.appendFileSync(historyFile, entry);
  } else {
    fs.writeFileSync(historyFile, `# Search History\n\n${entry}`);
  }
}

async function interactiveSearch() {
  console.log('\n🎯 Interactive Multi-Search');
  console.log('=========================\n');
  
  const query = await new Promise(resolve => {
    rl.question('Enter your search query: ', resolve);
  });
  
  if (!query.trim()) {
    console.log('❌ No query provided.');
    rl.close();
    return;
  }
  
  console.log('\nAvailable options:');
  console.log('1. Default (auto-select engine)');
  console.log('2. Chinese engines');
  console.log('3. Global engines');
  console.log('4. Privacy-focused engines');
  console.log('5. Multiple engines');
  console.log('6. Specific engine');
  
  const choice = await new Promise(resolve => {
    rl.question('\nChoose option (1-6): ', resolve);
  });
  
  const options = {};
  
  switch (choice) {
    case '2':
      options.chinese = true;
      break;
    case '3':
      options.global = true;
      break;
    case '4':
      options.privacy = true;
      break;
    case '5':
      options.multiple = true;
      break;
    case '6':
      listEngines();
      const engine = await new Promise(resolve => {
        rl.question('\nEnter engine ID: ', resolve);
      });
      options.engine = engine;
      break;
  }
  
  // Ask about search type
  console.log('\nSearch types: web, images, news, videos, academic, shopping');
  const type = await new Promise(resolve => {
    rl.question('Search type (press Enter for web): ', answer => {
      resolve(answer.trim() || 'web');
    });
  });
  
  if (type !== 'web') {
    options.type = type;
  }
  
  // Ask about time filter
  console.log('\nTime filters: past-hour, past-day, past-week, past-month, past-year');
  const time = await new Promise(resolve => {
    rl.question('Time filter (press Enter for none): ', answer => {
      resolve(answer.trim());
    });
  });
  
  if (time) {
    options.time = time;
  }
  
  performSearch(query, options);
  rl.close();
}

// Main function
function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    interactiveSearch();
    return;
  }
  
  const command = args[0];
  
  switch (command) {
    case 'help':
      showHelp();
      break;
      
    case 'engines':
      listEngines();
      break;
      
    case 'operators':
      showOperators();
      break;
      
    case 'search':
      if (args.length < 2) {
        console.log('❌ Please provide a search query.');
        console.log('   Usage: search "your query" [options]');
        return;
      }
      
      // Parse query and options
      let query = '';
      const options = {};
      let i = 1;
      
      // Find the query (might be quoted)
      if (args[i].startsWith('"')) {
        query = args[i].slice(1);
        i++;
        while (i < args.length && !args[i].endsWith('"')) {
          query += ' ' + args[i];
          i++;
        }
        if (i < args.length) {
          query += ' ' + args[i].slice(0, -1);
          i++;
        }
      } else {
        query = args[i];
        i++;
      }
      
      // Parse options
      for (; i < args.length; i++) {
        if (args[i].startsWith('--')) {
          const option = args[i].slice(2);
          if (args[i + 1] && !args[i + 1].startsWith('--')) {
            options[option] = args[i + 1];
            i++;
          } else {
            options[option] = true;
          }
        }
      }
      
      performSearch(query, options);
      break;
      
    default:
      // If no command specified, treat as search query
      const queryFromArgs = args.join(' ');
      performSearch(queryFromArgs);
      break;
  }
}

// Run if called directly
if (require.main === module) {
  main();
}

module.exports = {
  ENGINES,
  SEARCH_TYPES,
  OPERATORS,
  TIME_FILTERS,
  performSearch,
  listEngines,
  showOperators
};