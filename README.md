# Sasta SourceMap
analyze map files right away.


**The Risk**
If Developers forget to disable or delete the .map files before production
1. Anyone (including attackers) can:
2. Reverse-engineer the full code structure
3. Discover APIs, keys, role logic
4. Build better client-side exploits

Usage: python3 src-recon.py <source_map_file> <./output-folder>

Usage: python src-recon_windows.py <source_map_file> ./output-folder
