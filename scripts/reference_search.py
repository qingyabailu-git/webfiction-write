import sys, argparse, pathlib, json

def main():
    p = argparse.ArgumentParser(description='Search writing references by skill, table, query, and genre')
    p.add_argument('--skill', required=True, help='Skill name (write, conceive, etc.)')
    p.add_argument('--table', required=True, help='Reference file name without .md')
    p.add_argument('--query', default='', help='Search query')
    p.add_argument('--genre', default='', help='Genre filter')
    args = p.parse_args()

    # Locate the reference file
    base = pathlib.Path(__file__).resolve().parent.parent
    ref_dir = base / 'skills' / f'fiction-{args.skill}' / 'references'
    ref_file = ref_dir / f'{args.table}.md'

    if not ref_file.exists():
        # Try broader search
        for skill_dir in base.glob('skills/fiction-*/references'):
            candidate = skill_dir / f'{args.table}.md'
            if candidate.exists():
                ref_file = candidate
                break

    if not ref_file.exists():
        print(f'# Reference not found: {args.table}')
        print(f'Searched in: {ref_dir}')
        sys.exit(1)

    content = ref_file.read_text('utf-8')

    # If query specified, filter relevant sections
    if args.query:
        lines = content.split('\n')
        result = []
        in_section = False
        query_lower = args.query.lower()
        for line in lines:
            if line.startswith('#'):
                in_section = False
            if query_lower in line.lower() or (args.genre and args.genre.lower() in line.lower()):
                in_section = True
            if in_section:
                result.append(line)
        if result:
            print('\n'.join(result))
        else:
            # Return header + first 100 lines as overview
            print('\n'.join(lines[:100]))
            print(f'\n(Showing overview. Full file: {ref_file})')
    else:
        print(content)

if __name__ == '__main__':
    main()