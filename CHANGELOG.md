# Jarl Ulfric Armor Replacer - changelog

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
