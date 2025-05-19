import json
import os
import re
from collections import defaultdict

def sanitize_path_component(part: str) -> str:
    # Replace only illegal characters in filenames/folder names
    return re.sub(r'[<>:"\\\\|?*]', '_', part)

def sanitize_path(full_path: str) -> str:
    # Apply component sanitization without removing slashes
    parts = full_path.split('/')
    return os.path.join(*[sanitize_path_component(p) for p in parts if p.strip() != ''])

def extract_map(map_file_path, output_dir):
    with open(map_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    sources = data.get("sources", [])
    contents = data.get("sourcesContent", [])

    os.makedirs(output_dir, exist_ok=True)
    extracted_count = 0
    module_counts = defaultdict(int)

    for src, content in zip(sources, contents):
        if not content:
            print(f"[!] Skipped empty content: {src}")
            continue

        # Clean and reconstruct path safely
        sanitized_rel_path = sanitize_path(src)
        safe_path = os.path.normpath(os.path.join(output_dir, sanitized_rel_path))

        # Prevent path traversal outside output dir
        if not os.path.abspath(safe_path).startswith(os.path.abspath(output_dir)):
            print(f"[!] Skipped unsafe path: {safe_path}")
            continue

        dir_name = os.path.dirname(safe_path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)

        try:
            with open(safe_path, "w", encoding="utf-8") as f_out:
                f_out.write(content)
            print(f"[+] Wrote: {safe_path}")
            extracted_count += 1

            # Track top-level folder/module
            relative_path = os.path.relpath(safe_path, output_dir)
            top_folder = relative_path.split(os.sep)[0]
            module_counts[top_folder] += 1

        except Exception as e:
            print(f"[!] Failed to write {safe_path}: {e}")

    print(f"\\n✅ Extraction complete. {extracted_count} files written to: {output_dir}")

    print(f"\\n📦 Summary by module:")
    for module, count in sorted(module_counts.items()):
        print(f" - {module}/ → {count} file(s)")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python src-recon.py <main.js.map> <output_folder>")
    else:
        extract_map(sys.argv[1], sys.argv[2])

