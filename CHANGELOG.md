# Jarl Ulfric Armor Replacer - changelog

## 1.0.1 - 2026-09-16 - untested

### Changed

- **The plugin is an ESPFE** - `Jarl Ulfric Armor Replacer.esp` carrying the light flag - instead of
  a `.esl` file (the owner's standing rule, 2026-09-16). A `.esl` file is forced to the top of the
  load order where nothing can sort below it, which defeats a replacer that is meant to be superseded
  in the plugins tab; the `.esp` keeps the FE-space FormIDs and the freedom from the 254-slot limit
  and sorts among ordinary plugins. Same records, same FormIDs - only the four header flag bytes
  differ, and the conversion tool proved that by comparing the two files. Remove the old `.esl` when
  updating; a mod manager does this for you.

No mesh, texture or record changes.

## 1.0.0 - 2026-09-16 - untested

First version.

### Added

- **Ulfric's armour from NordwarUA's Guards Armor Replacer, on its own** - his cuirass, gauntlets,
  boots and helmet, with the meshes and textures those records name and nothing else from that mod.
- **Outfit-only.** The two outfit records that dress him are overridden; his three NPC records are
  deliberately left alone, because each already carries the vanilla default outfit and is therefore
  not what puts the armour on him. That keeps this mod clear of face, AI and appearance mods.
- **A generator rather than a copied plugin.** `tools/build-esp.py` lifts the records out of
  NordwarUA's own archive at build time and renumbers them for a single-master plugin, so this
  repository carries none of his plugin and the extraction is reviewable.
