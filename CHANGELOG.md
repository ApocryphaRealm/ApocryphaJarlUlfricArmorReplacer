# Jarl Ulfric Armor Replacer - changelog

## 1.0.2 - 2026-10-18 - untested

### Fixed
- Ulfric stayed in his vanilla clothes on a save that had already dressed him (reported on 1.0.1 by FootConnoisseur, who had not started a new game). The game reads an outfit record only when an actor is first set up, so a save that already holds Ulfric's old clothes in his inventory never read the two outfit overrides. The plugin now carries one start-game-enabled quest, JUAR_RedressUlfric, with a Papyrus script: on the first load of such a save it waits until Ulfric is loaded and, if he still wears the vanilla clothes, swaps his outfit away and back so the game reads the overridden record. It does nothing once he wears the armour, nothing if another mod has dressed him, and stops after six tries. A new game is unchanged.

### Changed
- The plugin gains one quest record and a script (Scripts/JUARRedressUlfric.pex, source in Source/Scripts); it is still an ESPFE with the one master Skyrim.esm. No mesh, texture or outfit record changed. Compiled with the Creation Kit's Papyrus compiler against the vanilla sources; no script extender needed.

## 1.0.1 - 2026-09-16 - untested

### Changed

- **The plugin is an ESPFE** - `Jarl Ulfric Armor Replacer.esp` carrying the light flag - instead of
  a `.esl` file (the owner's standing rule, 2026-09-16). A `.esl` file is forced to the top of the
  load order where nothing can sort below it, which defeats a replacer that is meant to be superseded
  in the plugins tab; the `.esp` keeps the FE-space FormIDs and the freedom from the 254-slot limit
  and sorts among ordinary plugins. Same records, same FormIDs - only the four header flag bytes
  differ, and the conversion tool proved that by comparing the two files. Remove the old `.esl` when
  updating; a mod manager does this for you.

- **Saves:** Updating from the old .esl: let your mod manager remove the old file. A save made with the .esl loaded will not carry this mod's records over to the renamed plugin - the game ties them to the file name - so treat this like installing the mod fresh: existing saves lose what came from the old plugin, and a new game or a save that never had it is clean.

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
