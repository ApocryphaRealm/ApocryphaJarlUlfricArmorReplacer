# Jarl Ulfric Armor Replacer - state and standing exceptions

## What it is

Ulfric Stormcloak's armour from NordwarUA's Guards Armor Replacer (Nexus 22671), extracted into a
standalone mod. Two outfit overrides, eleven new armour records, 25 meshes and 15 textures. No code.

1.0.0 is recorded working: seen in game on 2026-09-16 in Njordlinger (SE 1.5.97) with Guards Armor
Replacer absent, confirmed by the owner from his own screenshot - "its correct".

## Rule 31 (DevBench observability) - acknowledged and justified, not silently skipped

`pre-finalize-check.ps1` reports:

> No RegisterTool(...)/GetDevBenchInterface call found anywhere in source.

That is correct and it stays that way. **This mod contains no code.** It is an ESP and loose files;
there is no DLL, no process to attach to, nothing that runs, and therefore nothing a DevBench tool
could observe or drive. Rule 31 exists so a mod's behaviour can be watched live instead of
reconstructed from logs afterwards - a mod with no behaviour at runtime has nothing to watch.

What replaces it here, and what was actually done instead:

* The plugin is **generated** by `tools/build-esp.py` and was parsed back record by record after
  building - 13 records, one master, every internal reference checked.
* The assets are **generated** by `tools/extract-assets.py`, which fails loudly rather than silently
  extracting nothing, and whose output was verified byte-for-byte against the shipped package.
* Every texture the meshes name was read out of the NIFs and traced to its source; the two that are
  not shipped were confirmed present in the vanilla archives with BSArch.

That is the observability this mod can have, and it is stronger than a log line would be.

## What is deliberately not here

* **Ulfric's NPC records.** Guards Armor Replacer overrides all three; this mod overrides none,
  because each already carries the vanilla default outfit and is not what dresses him. See NOTICE.md.
* **NordwarUA's files.** They are not committed - `.gitignore` keeps them out. The repo holds the
  generators; his archive supplies the data.

## Open

* **The Nexus permissions block has not been read.** Mod 22671's page returns 403 to anything but a
  browser. The owner instructed the mod be made and stated the assets are free to use; that is the
  only authority this rests on. Read the block before publishing and record it in NOTICE.md.
