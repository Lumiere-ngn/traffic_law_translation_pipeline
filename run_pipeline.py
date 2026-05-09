import argparse
import sys
import yaml
import os

# Ensure the pipeline modules can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def load_config():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "sites.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(description="Traffic Law Translation Pipeline")
    
    # Target
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--site", type=str, help="Site name from sites.yaml (e.g. quebec, ontario)")
    group.add_argument("--from-cache", type=str, help="Path to cached raw_laws.json to skip scraping")
    
    # LLM Settings
    parser.add_argument("--model", type=str, help="LiteLLM model string (e.g. gpt-4o, claude-3-5-sonnet-20240620, ollama/llama3)")
    
    # Modes
    parser.add_argument("--scrape-only", action="store_true", help="Scrape only, do not run LLM translation")
    parser.add_argument("--resume", action="store_true", help="Resume from checkpoint if output exists")

    args = parser.parse_args()

    if not args.scrapeonly and not args.model:
        parser.error("--model is required unless --scrape-only is used")

    print("=" * 60)
    print("  Traffic Law Pipeline")
    print("=" * 60)

    # 1. Scrape or Load
    laws = []
    if args.from_cache:
        print(f"Loading laws from cache: {args.from_cache}")
        # To be implemented: load JSON to Law dataclass
        print("Not fully implemented yet.")
    elif args.site:
        config = load_config()
        if args.site not in config["sites"]:
            print(f"Error: Site '{args.site}' not found in config/sites.yaml")
            sys.exit(1)
        site_cfg = config["sites"][args.site]
        print(f"Target site: {args.site} ({site_cfg['base_url']})")
        
        from adapters import get_adapter
        adapter = get_adapter(site_cfg["base_url"])
        print(f"Using adapter: {type(adapter).__name__}")
        
        # To be implemented: laws = adapter.fetch_laws(...)
        print("Scraping not fully implemented yet.")

    if args.scrape_only:
        print("\nScrape-only mode requested. Saving raw laws and exiting.")
        sys.exit(0)

    # 2. Translate
    print(f"\nInitializing Open Interpreter with model: {args.model}")
    # To be implemented: translator loop
    print("Translation not fully implemented yet.")

    # 3. Persist
    print("\nFinished pipeline run.")


if __name__ == "__main__":
    main()
