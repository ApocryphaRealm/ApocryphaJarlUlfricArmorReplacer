# Jarl Ulfric Armor Replacer - what is whose

This mod is mostly **not our work**, and the licence reflects that. It is worth reading before
touching anything here.

## NordwarUA's, redistributed

Every mesh, every texture, and the armour records themselves come from
**[Guards Armor Replacer SSE](https://www.nexusmods.com/skyrimspecialedition/mods/22671)** by
**NordwarUA** (Nexus mod 22671, version 5.5a, uploaded by DanielUA). Nothing in them was made here
and nothing in them was altered - the meshes and textures are byte-for-byte his files, and the
records are his records with only their FormIDs renumbered so they fit a plugin with one master
instead of six.

That covers:

* `Meshes\1_Soldier_Replacer\Guards\ElitArmor\Armor\Stormlord*.nif` and `1stUArmor*.nif`
* `Textures\1_Soldier_Replacer\Guards\*.dds` (the fifteen those meshes name)
* the ARMO and ARMA records for Ulfric's cuirass, gauntlets, boots and helmet
* the two outfit overrides that put them on him

His own page credits Vaultman30, Christian Paskota (gechbal), Narf's Rus Armor for Mount & Blade and
the Witcher 2 Armor Collection for work his armours are based on, and states that all assets there
are used with explicit author permission. That chain of credit travels with these files.

**PERMISSION, AND WHAT WAS ACTUALLY CHECKED.** The owner of this project instructed that this mod be
made and stated that NordwarUA's assets are free to use (2026-09-16: *"because this is Nordwar UA,
all assets are free use"*). The Nexus "Permissions and credits" block on mod 22671 could **not** be
read from here - the page returns HTTP 403 to anything but a browser - so that block has not been
verified independently. Before this is published anywhere, somebody should open that page and read
it. This file should then record what it says.

## Ours

Only `tools/build-esp.py` - the generator that lifts the records out of NordwarUA's plugin and
writes this one. It carries no assets and no record data of his; it reads his archive at build time.
That script is GPL-3.0-or-later, copyright (C) 2026 ApocryphaRealm.

## It stands alone - checked, not assumed

Every path the shipped meshes ask for was read out of the NIFs and traced to its source:

| What is needed | Where it comes from |
|---|---|
| 15 armour textures | shipped here |
| 25 meshes | shipped here |
| `textures\cubemaps\chitin_e_ebony.dds`, `textures\cubemaps\quickskydark_e.dds` | vanilla, `Skyrim - Textures3.bsa` |
| every FormID the records reference | vanilla `Skyrim.esm` (races, keywords, armour ratings, the two outfits) |

Nothing resolves to Guards Armor Replacer or to any other mod. The plugin declares one master. Install
this on a bare Skyrim and Ulfric wears the armour.

(The two cubemaps were confirmed present in the vanilla archive with BSArch. A first pass wrongly
reported them missing - BSArch takes `<archive> -list`, not `list <archive>`, and the usage banner it
prints for a malformed command reads exactly like an empty result.)

## What this mod deliberately does not contain

Guards Armor Replacer is 1,382 files covering every hold's guards, the Solitude elite set, weapons
and shields. None of that is here. Neither are Ulfric's three NPC records, which that mod overrides
- each one carries the same default outfit as vanilla, so they are not what dresses him, and leaving
them out keeps this mod away from face, AI and appearance mods.
