#!/usr/bin/env python3
"""
Convert Hexo posts to Zola format - Fixed for BOM handling
"""
import os
import re
import yaml
from pathlib import Path
from datetime import datetime

def strip_bom(content):
    """Remove UTF-8 BOM if present"""
    if content.startswith('\ufeff'):
        return content[1:]
    return content

def convert_post(source_path, dest_dir):
    """Convert a single Hexo post to Zola format"""
    filename = os.path.basename(source_path)
    
    try:
        with open(source_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"ERROR reading {filename}: {e}")
        return None
    
    # Strip BOM if present
    content = strip_bom(content)
    
    # Parse frontmatter
    if not content.startswith('---'):
        print(f"SKIP {filename}: No frontmatter marker (starts with: {repr(content[:20])})")
        return None
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        print(f"SKIP {filename}: Invalid frontmatter structure")
        return None
    
    try:
        frontmatter = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        print(f"YAML ERROR in {filename}: {e}")
        return None
    except Exception as e:
        print(f"ERROR parsing frontmatter in {filename}: {e}")
        return None
    
    if frontmatter is None:
        print(f"SKIP {filename}: Empty frontmatter")
        return None
    
    body = parts[2].strip()
    
    # Convert to TOML
    title = frontmatter.get('title', '').replace('"', '\\"')
    date = frontmatter.get('date')
    tags = frontmatter.get('tags', []) or []
    
    # Format date for Zola
    if isinstance(date, datetime):
        date_str = date.strftime('%Y-%m-%dT%H:%M:%SZ')
    else:
        date_str = str(date)
    
    # Build TOML frontmatter
    toml_lines = ['+++']
    toml_lines.append(f'title = "{title}"')
    toml_lines.append(f'date = {date_str}')
    
    if tags:
        toml_lines.append('')
        toml_lines.append('[taxonomies]')
        tags_str = ', '.join(f'"{t}"' for t in tags if t)
        toml_lines.append(f'tags = [{tags_str}]')
    
    toml_lines.append('+++')
    toml_lines.append('')
    
    # Convert body
    # Replace Hexo excerpt marker
    body = body.replace('<!-- more -->', '<!-- more -->')
    
    # Replace asset_path shortcodes (used in raw HTML img tags)
    # In Zola, assets are colocated so we just need the filename
    body = re.sub(
        r'{%\s*asset_path\s+(\S+)\s*%}',
        lambda m: m.group(1),
        body
    )
    
    # Fix broken Disqus comment anchors - remove them since comments aren't in static build
    body = re.sub(
        r'\[([^\]]+)\]\(#comment-\d+\)',
        r'\1',
        body
    )
    
    # Replace asset_img shortcodes
    body = re.sub(
        r'{%\s*asset_img\s+(\S+)\s*(.*?)?\s*%}',
        lambda m: f'{{{{ image(path="{m.group(1)}"{f", alt=\"{m.group(2).strip()}\"" if m.group(2) else ""}) }}}}',
        body
    )
    
    # Replace blockquote shortcodes - opening tag with body content needs {% %} syntax
    body = re.sub(
        r'{%\s*blockquote\s+(.*?)\s*%}(.*?){%\s*endblockquote\s*%}',
        lambda m: f'{{% blockquote(author="{m.group(1).strip()}") %}}\n{m.group(2).strip()}\n{{% end %}}',
        body,
        flags=re.DOTALL
    )
    
    # Replace youtube shortcodes
    body = re.sub(
        r'{%\s*youtube\s+(\S+)\s*%}',
        r'{{ youtube(id="\1") }}',
        body
    )
    
    toml_content = '\n'.join(toml_lines) + body
    
    # Determine output filename (remove date prefix)
    # Remove date prefix like 2020-01-20-
    new_filename = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', filename)
    
    dest_path = os.path.join(dest_dir, new_filename)
    
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(toml_content)
    
    return dest_path

def main():
    source_dir = 'source/_posts'
    dest_dir = 'content/posts'
    
    os.makedirs(dest_dir, exist_ok=True)
    
    converted = []
    skipped = []
    
    for filename in sorted(os.listdir(source_dir)):
        if filename.endswith('.md'):
            source_path = os.path.join(source_dir, filename)
            result = convert_post(source_path, dest_dir)
            if result:
                converted.append(result)
                print(f'✓ Converted: {filename}')
            else:
                skipped.append(filename)
    
    print(f'\n{"="*60}')
    print(f'Total converted: {len(converted)}')
    print(f'Total skipped: {len(skipped)}')
    if skipped:
        print(f'\nSkipped files:')
        for f in skipped:
            print(f'  - {f}')

if __name__ == '__main__':
    main()
