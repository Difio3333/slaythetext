import re
from pathlib import Path
import entities



def words(text): return re.findall(r'\w+', text)

#WORDS = Counter(words(open(str(Path.cwd())+"/things.txt").read()))

WORDS = {"Strike":1,"Strike +":1,"Shiv":1,"Shiv +":1,"Defend":1,"Defend +":1,"Neutralize":1,"Neutralize +":1,"Survivor":1,"Survivor +":1,"Bane":1,"Bane +":1,"Dagger Spray":1,"Dagger Spray +":1,"Dagger Throw":1,"Dagger Throw +":1,"Flying Knee":1,"Flying Knee +":1,"Poisoned Stab":1,"Poisoned Stab +":1,"Quick Slash":1,"Quick Slash +":1,"Slice":1,"Slice +":1,"Sneaky Strike":1,"Sneaky Strike +":1,"Sucker Punch":1,"Sucker Punch +":1,"All-Out Attack":1,"All-Out Attack +":1,"Backstab":1,"Backstab +":1,"Choke":1,"Choke +":1,"Dash":1,"Dash +":1,"Endless Agony":1,"Endless Agony +":1,"Eviscerate":1,"Eviscerate +":1,"Finisher":1,"Finisher +":1,"Flechettes":1,"Flechettes +":1,"Heel Hook":1,"Heel Hook +":1,"Masterful Stab":1,"Masterful Stab +":1,"Predator":1,"Predator +":1,"Riddle with Holes":1,"Riddle with Holes +":1,"Skewer":1,"Skewer +":1,"Die Die Die":1,"Die Die Die +":1,"Glass Knife":1,"Glass Knife +":1,"Grand Finale":1,"Grand Finale +":1,"Unload":1,"Unload +":1,"Acrobatics":1,"Acrobatics +":1,"Backflip":1,"Backflip +":1,"Blade Dance":1,"Blade Dance +":1,"Cloak and Dagger":1,"Cloak and Dagger +":1,"Deadly Poison":1,"Deadly Poison +":1,"Deflect":1,"Deflect +":1,"Dodge and Roll":1,"Dodge and Roll +":1,"Outmaneuver":1,"Outmaneuver +":1,"Piercing Wail":1,"Piercing Wail +":1,"Prepared":1,"Prepared +":1,"Blur":1,"Blur +":1,"Bouncing Flask":1,"Bouncing Flask +":1,"Calculated Gamble":1,"Calculated Gamble +":1,"Catalyst":1,"Catalyst +":1,"Concentrate":1,"Concentrate +":1,"Crippling Cloud":1,"Crippling Cloud +":1,"Distraction":1,"Distraction +":1,"Escape Plan":1,"Escape Plan +":1,"Expertise":1,"Expertise +":1,"Leg Sweep":1,"Leg Sweep +":1,"Reflex":1,"Reflex +":1,"Tactician":1,"Tactician +":1,"Setup":1,"Setup +":1,"Terror":1,"Terror +":1,"Adrenaline":1,"Adrenaline +":1,"Alchemize":1,"Alchemize +":1,"Corpse Explosion":1,"Corpse Explosion +":1,"Doppelganger":1,"Doppelganger +":1,"Malaise":1,"Malaise +":1,"Phantasmal Killer":1,"Phantasmal Killer +":1,"Bullet Time":1,"Bullet Time +":1,"Storm of Steel":1,"Storm of Steel +":1,"Burst":1,"Burst +":1,"Accuracy":1,"Accuracy +":1,"After Image":1,"After Image +":1,"Caltrops":1,"Caltrops +":1,"Footwork":1,"Footwork +":1,"Infinite Blades":1,"Infinite Blades +":1,"NoxiousFumes":1,"NoxiousFumes +":1,"Well-Laid Plans":1,"Well-Laid Plans +":1,"A Thousand Cuts":1,"A Thousand Cuts +":1,"Envenom":1,"Envenom +":1,"Tools of the Trade":1,"Tools of the Trade +":1,"Wraith Form":1,"Wraith Form +":1,"Bandage Up":1,"Bandage Up +":1,"Blind":1,"Blind +":1,"Trip":1,"Trip +":1,"Dark Shackles":1,"Dark Shackles +":1,"Deep Breath":1,"Deep Breath +":1,"Discovery":1,"Discovery +":1,"Dramatic Entrance":1,"Dramatic Entrance +":1,"Enlightenment":1,"Enlightenment +":1,"Finesse":1,"Finesse +":1,"Flash of Steel":1,"Flash of Steel +":1,"Forethought":1,"Forethought +":1,"Good Instincts":1,"Good Instincts +":1,"Impatience":1,"Impatience +":1,"Jack of All Trades":1,"Jack of All Trades +":1,"Madness":1,"Madness +":1,"Mind Blast":1,"Mind Blast +":1,"Panacea":1,"Panacea +":1,"Panic Button":1,"Panic Button +":1,"Purify":1,"Purify +":1,"Swift Strike":1,"Swift Strike +":1,"Apotheosis":1,"Apotheosis +":1,"Chrysalis":1,"Chrysalis +":1,"Hand of Greed":1,"Hand of Greed +":1,"Magnetism":1,"Magnetism +":1,"Master of Strategy":1,"Master of Strategy +":1,"Mayhem":1,"Mayhem +":1,"Metamorphosis":1,"Metamorphosis +":1,"Panache":1,"Panache +":1,"Sadistic Nature":1,"Sadistic Nature +":1,"Secret Technique":1,"Secret Technique +":1,"Secret Weapon":1,"Secret Weapon +":1,"The Bomb":1,"The Bomb +":1,"Thinking Ahead":1,"Thinking Ahead +":1,"Transmutation":1,"Transmutation +":1,"Violence":1,"Violence +":1,"Apparition":1,"Apparition +":1,"Ritual Dagger":1,"Ritual Dagger +":1,"Slimed":1,"Void":1,"Dazed":1,"Burn":1,"Burn +":1,"Clumsy":1,"Injury":1,"Wound":1,"Decay":1,"Parasite":1,"Regret":1,"Shame":1,"Doubt":1,"Pain":1,"Writhe":1,"Normality":1,"Curse of the Bell":1,"Necronomicurse":1,"Ascender's Bane":1,"Ring of the Snake":1,"Akabeko":1,"Anchor":1,"Ancient Tea Set":1,"Art of War":1,"Bag of Marbles":1,"Bag of Preparation":1,"Blood Vial":1,"Bronze Scales":1,"Centennial Puzzle":1,"Ceramic Fish":1,"Dream Catcher":1,"Happy Flower":1,"Juzu Bracelet":1,"Lantern":1,"Maw Bank":1,"Meal Ticket":1,"Nunchaku":1,"Oddly Smooth Stone":1,"Omamori":1,"Orichalcum":1,"Pen Nib":1,"Potion Belt":1,"Preserved Insect":1,"Regal Pillow":1,"Smiling Mask":1,"Snecko Skull":1,"Strawberry":1,"The Boot":1,"Tiny Chest":1,"Toy Ornithopter":1,"Vajra":1,"War Paint":1,"Whetstone":1,"Blue Candle":1,"Bottled Flame":1,"Bottled Lightning":1,"Bottled Tornado":1,"Darkstone Periapt":1,"Eternal Feather":1,"Frozen Egg":1,"Gremlin Horn":1,"Horn Cleat":1,"Ink Bottle":1,"Kunai":1,"Letter Opener":1,"Matryoshka":1,"Meat on the Bone":1,"Mercury Hourglass":1,"Molten Egg":1,"Mummified Hand":1,"Ninja Scroll":1,"Ornamental Fan":1,"Pantograph":1,"Paper Krane":1,"Pear":1,"Question Card":1,"Shuriken":1,"Singing Bowl":1,"Strike Dummy":1,"Sundial":1,"The Courier":1,"Toxic Egg":1,"White Beast Statue":1,"Bird-Faced Urn":1,"Calipers":1,"Captain's Wheel":1,"Dead Branch":1,"Du-Vu Doll":1,"Fossilized Helix":1,"Ginger":1,"Girya":1,"Ice Cream":1,"Lizard Tail":1,"Mango":1,"Old Coin":1,"Peace Pipe":1,"Pocketwatch":1,"Prayer Wheel":1,"Shovel":1,"Stone Calendar":1,"The Specimen":1,"Thread and Needle":1,"Tingsha":1,"Torii":1,"Tough Bandages":1,"Tungsten Rod":1,"Turnip":1,"Unceasing Top":1,"Astrolabe":1,"Black Star":1,"Busted Crown":1,"Calling Bell":1,"Coffee Dripper":1,"Cursed Key":1,"Ectoplasm":1,"Empty Cage":1,"Fusion Hammer":1,"Hovering Kite":1,"Pandora's Box":1,"Philosopher's Stone":1,"Ring of the Serpent":1,"Runic Dome":1,"Runic Pyramid":1,"Sacred Bark":1,"Slaver's Collar":1,"Sozu":1,"Snecko Eye":1,"Velvet Choker":1,"Wrist Blade":1,"Cultist Headpiece":1,"Enchiridion":1,"Red Mask":1,"N'loth's Gift":1,"Face of Cleric":1,"Golden Idol":1,"Gremlin Visage":1,"Mark of the Bloom":1,"Mutagenic Strength":1,"Necronomicon":1,"Neow's Lament":1,"Nilry's Codex":1,"N'loth's Hungry Face":1,"Odd Mushroom":1,"Ssserpent Head":1,"Warped Tongs":1,"Cauldron":1,"Chemical X":1,"Clockwork Souvenir":1,"Dolly's Mirror":1,"Frozen Eye":1,"Hand Drill":1,"Lee's Waffle":1,"Medical Kit":1,"Membership Card":1,"Orrery":1,"Sling of Courage":1,"Strange Spoon":1,"The Abacus":1,"Toolbox":1,"Twisted Funnel":1,"Red Key":1,"Blue Key":1,"Green Key":1,"Ancient Potion":1,"Attack Potion":1,"Blessing of the Forge":1,"Block Potion":1,"Blood Potion":1,"Colorless Potion":1,"Cultist Potion":1,"Cunning Potion":1,"Dexterity Potion":1,"Strength Potion":1,"Distilled Chaos":1,"Duplication Potion":1,"Energy Potion":1,"Entropic Brew":1,"Essence of Steel":1,"Explosive Potion":1,"Fairy in a Bottle":1,"Fear Potion":1,"Fire Potion":1,"Fruit Juice":1,"Gamblers Brew":1,"Ghost in a Jar":1,"Liquid Bronze":1,"Liquid Memories":1,"Poison Potion":1,"Power Potion":1,"Regen Potion":1,"Skill Potion":1,"Smoke Bomb":1,"Snecko Oil":1,"Speed Potion":1,"Flex Potion":1,"Swift Potion":1,"Weak Potion":1}


def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)))

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ '
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

