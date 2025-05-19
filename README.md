# Sasta SourceMap
analyze map files right away.


**The Risk**:

If Developers forget to disable or delete the .map files before production
Anyone (including attackers) can:
1. Reverse-engineer the full code structure
2. Discover APIs, keys, role logic
3. Build better client-side exploits

Usage: python3 src-recon.py <source_map_file> <./output-folder>

Usage: python src-recon_windows.py <source_map_file> ./output-folder
