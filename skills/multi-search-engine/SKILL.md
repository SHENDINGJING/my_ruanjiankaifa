---
name: multi-search-engine
description: Multi search engine integration with 17 engines (8 CN + 9 Global). Supports advanced search operators, time filters, site search, privacy engines, and WolframAlpha knowledge queries. No API keys required.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": [] },
        "install": [],
      },
  }
---

# Multi Search Engine

Multi search engine integration with 17 engines (8 Chinese + 9 Global). Supports advanced search operators, time filters, site search, privacy engines, and WolframAlpha knowledge queries. No API keys required.

## Supported Search Engines

### Chinese Engines (8)
1. **Baidu** (百度) - Chinese web search
2. **Bing CN** (必应中国) - Microsoft search in China
3. **Sogou** (搜狗) - Chinese search engine
4. **360 Search** (360搜索) - Chinese search
5. **Zhihu** (知乎) - Chinese Q&A platform search
6. **Weibo** (微博) - Chinese microblogging search
7. **Douban** (豆瓣) - Chinese book/movie/music reviews
8. **Tieba** (贴吧) - Chinese forum search

### Global Engines (9)
1. **Google** - Global web search
2. **Bing** - Microsoft global search
3. **DuckDuckGo** - Privacy-focused search
4. **Startpage** - Privacy search with Google results
5. **Yandex** - Russian search engine
6. **Ecosia** - Eco-friendly search (plants trees)
7. **Qwant** - Privacy-focused European search
8. **Brave Search** - Privacy-focused with its own index
9. **WolframAlpha** - Computational knowledge engine

## Features

### Advanced Search Operators
- **site:** - Search within specific website
- **filetype:** - Search for specific file types
- **intitle:** - Search in page titles
- **inurl:** - Search in URLs
- **"exact phrase"** - Exact phrase search
- **-exclude** - Exclude terms
- **OR** - Boolean OR operator
- **..** - Number range (e.g., 2020..2023)

### Time Filters
- Past hour
- Past 24 hours
- Past week
- Past month
- Past year
- Custom date range

### Search Types
1. **Web Search** - General web pages
2. **Image Search** - Image results
3. **Video Search** - Video results
4. **News Search** - News articles
5. **Academic Search** - Scholarly papers
6. **Shopping Search** - Product listings
7. **Map Search** - Location-based results
8. **Book Search** - Book information

### Privacy Features
- No tracking
- No personalized results
- No search history storage
- Encrypted connections
- Anonymous searching options

### WolframAlpha Integration
- Mathematical computations
- Scientific data
- Historical facts
- Geographical information
- Linguistic analysis
- Nutritional information
- Financial data
- Weather information

## Usage

### Basic Search
```bash
# Search with default engine
search "query"

# Search with specific engine
search --engine google "query"
search --engine baidu "中文查询"
```

### Advanced Search
```bash
# Site-specific search
search "site:github.com openclaw"

# File type search
search "filetype:pdf machine learning"

# Time-filtered search
search "latest news" --time past-week

# Multiple engines
search "query" --engines google,bing,duckduckgo
```

### WolframAlpha Queries
```bash
# Mathematical computation
wolfram "integrate x^2 from 0 to 1"

# Scientific data
wolfram "speed of light"

# Real-world data
wolfram "population of China 2024"
```

## Engine Selection Guide

### For Chinese Content
- **General search**: Baidu, Bing CN
- **Q&A**: Zhihu
- **Social media**: Weibo
- **Reviews**: Douban
- **Forums**: Tieba

### For Global Content
- **General search**: Google, Bing
- **Privacy**: DuckDuckGo, Startpage
- **European focus**: Qwant
- **Eco-friendly**: Ecosia
- **Computational**: WolframAlpha

### For Specific Needs
- **Academic**: Google Scholar (via Google)
- **Images**: Google Images, Bing Images
- **Videos**: YouTube (via Google)
- **News**: Google News, Bing News
- **Shopping**: Google Shopping

## Configuration

### Default Settings
- Primary engine: Google
- Secondary engine: Baidu (for Chinese queries)
- Results per page: 10
- Safe search: Moderate
- Language: Auto-detect
- Region: Auto-detect

### Customization
```bash
# Set default engine
config --default-engine duckduckgo

# Set language preference
config --language zh-CN

# Set region
config --region CN

# Enable/disable safe search
config --safe-search strict
config --safe-search off
```

## Integration with OpenClaw

### Web Search Tool
This skill enhances the existing `web_search` tool with:
- Multiple engine support
- Advanced operators
- Time filtering
- Privacy options

### Browser Integration
- Direct search from browser
- Quick engine switching
- Search history (optional)
- Bookmark integration

### API Access
- REST API for programmatic access
- JSON responses
- Rate limiting
- Caching options

## No API Keys Required

All search engines are accessed through:
1. Public search interfaces
2. Open APIs where available
3. Web scraping (respecting robots.txt)
4. RSS feeds
5. Sitemap indexes

## Legal and Ethical Use

### Respectful Usage
- Follow robots.txt rules
- Respect rate limits
- Use caching appropriately
- Attribute sources properly
- Don't overload servers

### Privacy Protection
- Minimize data collection
- Use privacy engines when needed
- Clear search history regularly
- Use encrypted connections
- Avoid tracking cookies

### Content Guidelines
- Respect copyright
- Follow terms of service
- Use for legitimate purposes
- Avoid automated abuse
- Report inappropriate content

## Performance Tips

### For Speed
- Use closest regional servers
- Enable caching
- Limit concurrent requests
- Use lightweight engines first
- Prefer text-only results when possible

### For Accuracy
- Use multiple engines
- Compare results
- Check date filters
- Verify with authoritative sources
- Use advanced operators

### For Privacy
- Use DuckDuckGo or Startpage
- Clear cookies regularly
- Use private browsing mode
- Disable personalized results
- Use VPN when needed

## Troubleshooting

### Common Issues
1. **Engine not responding**: Try alternative engine
2. **Rate limited**: Wait or switch engine
3. **Blocked by firewall**: Use different engine or proxy
4. **Incorrect results**: Check search operators
5. **Slow performance**: Reduce concurrent searches

### Error Messages
- "Engine timeout": Server is slow or down
- "Access denied": IP blocked or restricted
- "Invalid query": Check search syntax
- "No results": Try different keywords or engines
- "API limit exceeded**: Wait before trying again

## Updates and Maintenance

### Regular Updates
- Engine compatibility updates
- New feature additions
- Bug fixes
- Performance improvements
- Security patches

### Community Contributions
- Report bugs
- Suggest new engines
- Improve documentation
- Share use cases
- Translate interfaces

Based on gpyAngyoujun/multi-search-engine v2.0.1 from ClawHub.