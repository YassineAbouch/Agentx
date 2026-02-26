#!/usr/bin/env node

/**
 * CLI wrapper for mybrowser
 * Usage: ./cli.js <command> [args]
 */

import fetch from 'node-fetch';

const BASE_URL = process.env.BROWSER_URL || 'http://localhost:3000';

const commands = {
  open: async (url) => {
    const res = await fetch(`${BASE_URL}/open`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });
    return await res.json();
  },
  
  click: async (selector) => {
    const res = await fetch(`${BASE_URL}/click`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ selector })
    });
    return await res.json();
  },
  
  type: async (selector, text) => {
    const res = await fetch(`${BASE_URL}/type`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ selector, text })
    });
    return await res.json();
  },
  
  scroll: async (y = 800) => {
    const res = await fetch(`${BASE_URL}/scroll`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ y: parseInt(y) })
    });
    return await res.json();
  },
  
  text: async () => {
    const res = await fetch(`${BASE_URL}/content/text`);
    return await res.json();
  },
  
  links: async () => {
    const res = await fetch(`${BASE_URL}/links`);
    return await res.json();
  },
  
  screenshot: async () => {
    const res = await fetch(`${BASE_URL}/screenshot`);
    return await res.json();
  },
  
  status: async () => {
    const res = await fetch(`${BASE_URL}/status`);
    return await res.json();
  },
  
  back: async () => {
    const res = await fetch(`${BASE_URL}/nav/back`, { method: 'POST' });
    return await res.json();
  },
  
  forward: async () => {
    const res = await fetch(`${BASE_URL}/nav/forward`, { method: 'POST' });
    return await res.json();
  },
  
  reload: async () => {
    const res = await fetch(`${BASE_URL}/reload`, { method: 'POST' });
    return await res.json();
  }
};

async function main() {
  const [,, command, ...args] = process.argv;
  
  if (!command || command === 'help') {
    console.log(`
MyBrowser CLI

Usage: mybrowser <command> [args]

Commands:
  open <url>            Open a URL
  click <selector>      Click an element
  type <selector> <text> Type text into an element
  scroll [pixels]       Scroll the page (default: 800px)
  text                  Get page text content
  links                 List all links on page
  screenshot            Take a screenshot
  status                Check browser status
  back                  Go back
  forward               Go forward
  reload                Reload page
  help                  Show this help

Examples:
  mybrowser open https://example.com
  mybrowser click "button.submit"
  mybrowser type "input[name=search]" "hello world"
  mybrowser scroll 1000
  mybrowser links
    `);
    process.exit(0);
  }
  
  if (!commands[command]) {
    console.error(`❌ Unknown command: ${command}`);
    console.error('Run "mybrowser help" for available commands');
    process.exit(1);
  }
  
  try {
    const result = await commands[command](...args);
    console.log(JSON.stringify(result, null, 2));
    
    if (!result.ok) {
      process.exit(1);
    }
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

main();
