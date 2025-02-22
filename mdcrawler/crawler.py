"""Core crawler functionality"""
import os
import asyncio
import logging
import yaml
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.content_filter_strategy import PruningContentFilter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Move existing functions from main.py
def get_safe_filename(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path.strip('/')
    if not path:
        return 'index.md'
    
    safe_name = path.replace('/', '_').replace('\\', '_')
    return f"{safe_name}.md"

def get_url_from_link(link) -> str:
    if isinstance(link, str):
        return link
    elif isinstance(link, dict):
        return link.get('href', '')
    return ''

def should_process_url(url: str, base_domain: str) -> bool:
    parsed = urlparse(url)
    if parsed.netloc != base_domain:
        return False
    if '#' in url:
        return False
    if 'djangoproject.com' in base_domain:
        path_parts = parsed.path.strip('/').split('/')
        if len(path_parts) >= 2 and path_parts[0] == 'en':
            try:
                version = float(path_parts[1])
                if version < 4.0:
                    return False
            except ValueError:
                pass
    return True

async def crawl_documentation(url: str, name: str, timeout: int = 1800):
    """Crawl documentation from a given URL."""
    logger.info(f"Starting crawl process for URL: {url}")
    logger.info(f"Output will be saved in: docs/{name}")

    output_dir = Path(f"docs/{name}")
    output_dir.mkdir(parents=True, exist_ok=True)

    start_time = datetime.now()
    
    browser_cfg = BrowserConfig(headless=True)
    link_extraction_cfg = CrawlerRunConfig(
        word_count_threshold=0,
        excluded_tags=[],
        markdown_generator=DefaultMarkdownGenerator(
            content_filter=PruningContentFilter(threshold=0.1),
            options={"ignore_links": False}
        ),
        cache_mode="BYPASS"
    )

    content_extraction_cfg = CrawlerRunConfig(
        word_count_threshold=15,
        excluded_tags=[
            "script", "style", "nav", "header", "footer", "aside",
            ".sidebar", "#sidebar", ".menu", "#menu", ".navigation", "#navigation",
            "[role='navigation']", ".nav-menu", ".nav-list", ".table-of-contents",
            ".toc", "#toc", ".site-nav", ".site-menu", ".docs-nav", ".docs-menu",
            ".mintlify-nav", ".docs-sidebar", ".navigation-menu", ".nav-groups",
            ".nav-wrapper", ".nav-container", ".navigation-wrapper",
            ".md-nav", ".md-sidebar", ".md-header", ".md-footer", ".md-tabs",
            ".md-search", ".md-search-result", ".md-source", ".md-header-nav",
            ".md-main__inner > nav", ".md-nav__title", ".md-nav__list",
            ".terminal-mkdocs", ".terminal-mkdocs-nav", ".terminal-mkdocs-sidebar",
            ".search-box", ".search-wrapper", ".ctrl-key", ".keyboard-shortcut",
            ".version-selector", ".version-info", ".metadata-bar",
            "*[class*='sidebar']", "*[class*='navigation']", "*[class*='nav-']",
            "*[id*='sidebar']", "*[id*='navigation']", "*[id*='nav-']",
            "*[class*='menu']", "*[id*='menu']"
        ],
        markdown_generator=DefaultMarkdownGenerator(
            content_filter=PruningContentFilter(threshold=0.3),
            options={
                "ignore_links": True,
                "ignore_navigation": True,
                "main_content_only": True,
                "remove_navigation_elements": True,
                "clean_documentation_artifacts": True,
                "strip_empty_headings": True,
                "remove_duplicate_content": True
            }
        ),
        cache_mode="BYPASS"
    )
    
    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        base_domain = urlparse(url).netloc
        main_result = await crawler.arun(url, config=link_extraction_cfg)
        internal_links = main_result.links.get("internal", [])
        
        main_content = await crawler.arun(url, config=content_extraction_cfg)
        main_filename = get_safe_filename(url)
        main_path = output_dir / main_filename
        with open(main_path, "w", encoding="utf-8") as f:
            f.write(main_content.markdown)
        
        processed_urls = {url}
        
        for link in internal_links:
            if (datetime.now() - start_time).total_seconds() > timeout:
                logger.warning(f"Timeout reached after {timeout} seconds. Stopping crawl.")
                break

            try:
                link_url = get_url_from_link(link)
                if not link_url or link_url in processed_urls:
                    continue
                    
                if not should_process_url(link_url, base_domain):
                    logger.debug(f"Skipping filtered URL: {link_url}")
                    continue
                
                await asyncio.sleep(0.5)
                result = await crawler.arun(link_url, config=content_extraction_cfg)
                
                if result and result.success:
                    filename = get_safe_filename(link_url)
                    output_path = output_dir / filename
                    
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(result.markdown)
                    processed_urls.add(link_url)
                    
            except Exception as e:
                logger.error(f"Error processing link {link}: {str(e)}")

async def crawl_multiple_libraries(config_file: str):
    """Crawl multiple documentation websites based on a configuration file."""
    logger.info(f"Loading library configuration from: {config_file}")
    
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Error loading configuration file: {str(e)}")
        raise

    if not config or 'libraries' not in config:
        raise ValueError("Invalid configuration file: 'libraries' section not found")

    libraries = config['libraries']
    if not libraries:
        logger.warning("No libraries defined in configuration file")
        return

    total_libraries = len(libraries)
    for idx, library in enumerate(libraries, 1):
        if not isinstance(library, dict) or 'name' not in library or 'url' not in library:
            logger.warning(f"Skipping invalid library entry: {library}")
            continue

        name = library['name']
        url = library['url']
        
        try:
            await crawl_documentation(url, name)
        except Exception as e:
            logger.error(f"Error processing library {name}: {str(e)}")
            await asyncio.sleep(5)