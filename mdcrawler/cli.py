"""Command line interface for mdcrawler"""
import asyncio
import argparse
from pathlib import Path
import logging
from crawler import crawl_documentation, crawl_multiple_libraries

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(
        description="Crawl documentation websites and convert them to markdown",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    mdcrawler --url https://docs.example.com --name example-docs
    mdcrawler --config libraries.yaml
    mdcrawler https://docs.example.com example-docs
"""
    )
    
    parser.add_argument("--config", help="Path to libraries configuration file (YAML)")
    parser.add_argument("--url", help="URL of a single documentation website")
    parser.add_argument("--name", help="Name of the output directory for single website")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("url_pos", nargs="?", help="URL of documentation website (positional)")
    parser.add_argument("name_pos", nargs="?", help="Output directory name (positional)")
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")

    try:
        if args.config:
            asyncio.run(crawl_multiple_libraries(args.config))
        elif args.url and args.name:
            asyncio.run(crawl_documentation(args.url, args.name))
        elif args.url_pos and args.name_pos:
            asyncio.run(crawl_documentation(args.url_pos, args.name_pos))
        else:
            parser.error("Either --config or URL and name must be provided (either as named or positional arguments)")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        raise

if __name__ == "__main__":
    main()