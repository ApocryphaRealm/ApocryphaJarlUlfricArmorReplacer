Jarl Ulfric Armor Replacer
==========================

Ulfric Stormcloak's armour from NordwarUA's Guards Armor Replacer, on its own.

If you like what NordwarUA did with Ulfric but do not want every guard in Skyrim replaced, this is
that one piece of it: his cuirass, gauntlets, boots and helmet, and the two outfits that put them on
him. Nothing else from that mod is here.


WHAT IT CHANGES
---------------
  Two outfit records - UlfricOutfit and UlfricPrisonerOutfit - so they hand out NordwarUA's armour
  instead of the vanilla set. A new game reads them, so Ulfric wears the armour from the start.

  A save that already dressed Ulfric keeps his old clothes (the game never reads the outfit again), so
  the plugin also carries one small quest, JUAR_RedressUlfric. On the first load of such a save it waits
  until Ulfric is loaded; if he still wears his vanilla clothes it swaps his outfit away and back, which
  makes the game read the new outfit. It does nothing once he wears the armour, and nothing at all if
  another mod has dressed him in something else.

  It does NOT touch Ulfric's NPC records. Guards Armor Replacer overrides them, but each one already
  carries the same default outfit as vanilla, so they are not what dresses him. Leaving them alone
  means this mod does not conflict with face replacers, AI overhauls or anything else that edits
  NPCs - the usual reason an armour replacer causes trouble.


WHAT IS IN THE PACKAGE
----------------------
  Jarl Ulfric Armor Replacer.esp    14 records, one master (Skyrim.esm)
  Scripts\JUARRedressUlfric.pex     the quest script (source in Source\Scripts)
  Meshes\...\ElitArmor\Armor\  Ulfric's Stormlord armour, both weight variants
  Textures\...\Guards\         the fifteen textures those meshes name


REQUIREMENTS
------------
  None beyond Skyrim itself. No script extender (the quest script is plain Papyrus), no framework, no other mod - and in particular NOT
  Guards Armor Replacer. Every mesh and texture the armour needs is in this download; the only things
  it borrows from outside are two environment cubemaps that ship with the base game, and the vanilla
  races, keywords and outfit records its plugin points at. The plugin declares one master, Skyrim.esm.

  Supported runtimes: any - this is a plugin and loose assets, with no DLL.


INSTALLATION
------------
  Install with a mod manager and enable the plugin.

  If you also run Guards Armor Replacer, you do not need this mod - it already includes this armour.
  Installed together they do not fight: the meshes and textures are the same files, and whichever
  plugin wins the outfit records gives the same result.


CREDIT
------
  All meshes, textures and armour records are NordwarUA's, from Guards Armor Replacer SSE:
  https://www.nexusmods.com/skyrimspecialedition/mods/22671
  Nothing in them was made or altered here. See NOTICE.md for the full attribution chain.
