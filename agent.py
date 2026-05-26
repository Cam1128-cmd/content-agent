import argparse
from pathlib import Path
from typing import Optional

from content_agent import create_gameplan


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a 7-day content gameplan.")
    parser.add_argument("niche", help="Niche to generate content for.")
    parser.add_argument("goal", nargs="?", default=None, help="Primary goal for the content plan.")
    parser.add_argument("-o", "--output", help="Write the generated gameplan to a Markdown file.")
    args = parser.parse_args()

    print(f"Generating a 7-day content gameplan for: {args.niche}")
    print()

    try:
        plan = create_gameplan(args.niche, args.goal)
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(plan, encoding="utf-8")
            print(f"Saved gameplan to {output_path}")
        else:
            print(plan)
    except Exception as exc:
        print("Error:", exc)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
