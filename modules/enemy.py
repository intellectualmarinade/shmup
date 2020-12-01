class Enemy(object):

    def __init__(self, name, HP, skills, attack, defense, loot, expget, flvrtxt):
        self.name = name
        self.HP = HP
        self.skills = skills
        self.attack = attack
        self.defense = defense
        self.loot = loot
        self.expget = expget
        self.flvrtxt = flvrtext


enemy1 = Enemy("Bush", 10, "none", 0, 5, "A Stick", 50, "Just a bush, it cannot attack")
enemy2 = Enemy("Imp", 50, "none", 10, 10, "gold", 150, "Cliche RPG enemy")
enemy3 = Enemy("Imp", 50, "none", 10, 10, "gold", 150, "Cliche RPG enemy")
