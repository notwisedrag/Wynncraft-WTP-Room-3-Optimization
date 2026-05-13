import numpy as np
import matplotlib.pyplot as plt

class Spells:
    def __init__(self, spell1, spell2, spell3, spell4, cycle, transc=True, ascended=False, generalist=False):
        self.spellCosts = [spell1, spell2, spell3, spell4]
        self.counter = 0
        self.penalty = 0
        self.cycle = cycle # list of spell casts in order, for example [2,3,3] for usual dash stab stab
        self.transc = transc
        self.ascended = ascended # ascended nirv major id refunds 25% of mana if transc procs
        self.generalist = generalist # generalist switch
        self.first_call = True # checks if this is the first spell casted in cycle

    def cast(self):
        step = self.counter % len(self.cycle)
        random_value = np.random.rand()
        if random_value <= 0.25 and self.transc == True:
            spell_cost = 0.25*self.spellCosts[self.cycle[step]] if self.ascended else 0
        else:
            spell_cost = -self.spellCosts[self.cycle[step]-1] -self.penalty
        if self.cycle[step] != self.cycle[step-1] or self.first_call==True:
            self.penalty = 0
        else:
            self.penalty += 5
        self.first_call = False
        self.counter += 1
        return spell_cost

def calculate_sustain_duration(parameters):
    spells = Spells(parameters["spell1"], parameters["spell2"], parameters["spell3"], parameters["spell4"], parameters["spellCycle"], parameters["transc"], parameters["ascended"], parameters["generalist"])
    mana = parameters["maxMana"] # initial mana
    delay = parameters["delay"]
    max_mana = parameters["maxMana"]
    manaRegen = parameters["manaRegen"]
    manaSteal = parameters["manaSteal"]
    game_tick = 0
    while mana > 0:
        if game_tick % 4 == 0: # mana tick happens every 4 ticks
            mana += manaRegen/5/5
        if game_tick % delay == 0:
            mana += spells.cast()
        if manaSteal % 40 == 0: # mana steal happens every 2s
            mana += manaSteal * 2 / 3
        if mana > max_mana:
            mana = max_mana
        game_tick += 1
        if game_tick > 100000:
            break
    return game_tick/20

durations = []
parameters = {
    "manaRegen": 109, # include base
    "manaSteal": 0,
    "maxMana": 183, # include base
    "spell1": 2,
    "spell2": 1,
    "spell3": 12.5,
    "spell4": 2,
    "spellCycle": [2,3,3],
    "delay": 6,
    "transc": True,
    "ascended": True,
    "generalist": False
}

for _ in range(10000):
    duration = calculate_sustain_duration(parameters)
    if duration >= 5000:
        print("Inf sustain")
        break
    durations.append(duration)
mean_val = np.mean(durations)
sd_val = np.std(durations)
print("mean:", mean_val)
print("standard deviation:", sd_val)
plt.hist(durations, bins=50, alpha=0.7)
plt.title('Sustain Duration (in seconds)')
plt.xlabel('Duration (seconds)')
plt.ylabel('Frequency (100 simulations)')
plt.text(
    0.98,
    0.95,
    f"Mean: {mean_val:.2f}\nSD: {sd_val:.2f}",
    transform=plt.gca().transAxes,
    ha='right',
    va='top',
    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8)
)
plt.show()