ScriptName JUARRedressUlfric Extends Quest
{Jarl Ulfric Armor Replacer - dresses Ulfric in the replacer armour on a save that already dressed him.

 The plugin overrides Ulfric's two outfit records. A new game reads them when Ulfric is first set up, so he
 wears the new armour. A save that already ran his set-up (or the Helgen quest's SetOutfit) holds his old
 clothes in his inventory and keeps them: the outfit record was never read again. This quest starts once on
 such a save, waits until Ulfric is loaded (he is not, until the player is near him), and if he still wears
 his vanilla clothes it swaps his outfit away and back, which makes the game read the overridden record and
 replace the outfit items. Nothing runs after it has dressed him, or once it finds him already dressed.
 It never touches Ulfric when something else has dressed him (he wears neither vanilla clothes nor ours).}

Actor Property UlfricRef Auto
{Ulfric's persistent reference in the Palace of the Kings (0001B131).}

Armor Property ReplacerCuirass Auto
{This mod's cuirass. Worn means he is already dressed.}

Armor Property VanillaClothes Auto
{ClothesUlfric (00062303). Worn means the save still holds the vanilla outfit.}

Armor Property VanillaCuffs Auto
{PrisonerCuffs (00103941). Worn means his current outfit is the prisoner one.}

Outfit Property UlfricOutfit Auto
{UlfricOutfit (00045C33).}

Outfit Property UlfricPrisonerOutfit Auto
{UlfricPrisonerOutfit (00101AF2).}

Float Property PollSeconds = 10.0 Auto
{How often to look again while Ulfric is not loaded yet.}

Int Property MaxAttempts = 6 Auto
{How many times to redress him before giving up (a failed attempt is logged).}

Int attempts = 0

Event OnInit()
	RegisterForSingleUpdate(2.0)
EndEvent

Event OnUpdate()
	If Settle()
		Debug.Trace("[JUAR] done: nothing more to do")
	Else
		RegisterForSingleUpdate(PollSeconds)
	EndIf
EndEvent

; True when the job is over (dressed, not needed, or given up); False to ask again later.
Bool Function Settle()
	If UlfricRef == None || ReplacerCuirass == None || VanillaClothes == None || UlfricOutfit == None || UlfricPrisonerOutfit == None
		Debug.Trace("[JUAR] a property is not filled - leaving Ulfric alone")
		Return True
	EndIf
	If UlfricRef.IsDead()
		Return True
	EndIf
	If !UlfricRef.Is3DLoaded()
		Return False
	EndIf
	If UlfricRef.IsEquipped(ReplacerCuirass)
		Debug.Trace("[JUAR] Ulfric already wears the replacer armour")
		Return True
	EndIf
	If !UlfricRef.IsEquipped(VanillaClothes)
		Debug.Trace("[JUAR] Ulfric wears neither the vanilla clothes nor ours - leaving him alone")
		Return True
	EndIf
	attempts += 1
	Outfit target = UlfricOutfit
	Outfit other = UlfricPrisonerOutfit
	If VanillaCuffs != None && UlfricRef.IsEquipped(VanillaCuffs)
		target = UlfricPrisonerOutfit
		other = UlfricOutfit
	EndIf
	Debug.Trace("[JUAR] attempt " + attempts + ": Ulfric wears the vanilla clothes - swapping his outfit away and back")
	UlfricRef.SetOutfit(other)
	Utility.Wait(1.0)
	UlfricRef.SetOutfit(target)
	Utility.Wait(2.0)
	If UlfricRef.IsEquipped(ReplacerCuirass)
		Debug.Trace("[JUAR] Ulfric now wears the replacer armour")
		Return True
	EndIf
	Debug.Trace("[JUAR] attempt " + attempts + " did not take")
	If attempts >= MaxAttempts
		Debug.Trace("[JUAR] giving up after " + attempts + " attempts")
		Return True
	EndIf
	Return False
EndFunction
