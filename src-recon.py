import json
import os

def extract_map(map_file_path, output_dir):
    with open(map_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    sources = data.get("sources", [])
    contents = data.get("sourcesContent", [])

    os.makedirs(output_dir, exist_ok=True)

    extracted_count = 0

    for src, content in zip(sources, contents):
        if not content:
            print(f"[!] Skipped empty content: {src}")
            continue

        # Normalize and anchor all paths inside output_dir
        safe_path = os.path.normpath(os.path.join(output_dir, src))

        # Absolute safety: block writing outside intended dir
        if not os.path.abspath(safe_path).startswith(os.path.abspath(output_dir)):
            print(f"[!] Skipped unsafe path: {safe_path}")
            continue

        # Create necessary folders
        os.makedirs(os.path.dirname(safe_path), exist_ok=True)

        # Write content
        with open(safe_path, "w", encoding="utf-8") as f_out:
            f_out.write(content)
            print(f"[+] Wrote: {safe_path}")
            extracted_count += 1

    print(f"\n✅ Extraction complete. {extracted_count} files written to: {output_dir}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python src-recon.py <main.js.map> <output_folder>")
    else:
        extract_map(sys.argv[1], sys.argv[2])

