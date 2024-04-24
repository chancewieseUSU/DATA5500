class Pet:
    # I formatted species like this because I could make a function to add more species if I wanted
    species_lifespan = {
        "human" : 73,
        "dog" : 12,
        "cat" : 15,
        "fish" : 10
        }
        
    def __init__(self, name, age, species):
        self.name = name
        self.age = age
        self.species = species
        
    def calculate_human_age(self): #this method uses uman years/animal years to find the actual amount, rather than an estimation (like 7 years for dogs)
        return self.age * Pet.species_lifespan["human"]/Pet.species_lifespan[self.species.lower()]
        
    def average_lifespan(self):
        return self.species_lifespan.get(self.species.lower())
    

pet1 = Pet("Maya", 3, "dog")
pet2 = Pet("Opal", 6, "fish")
pet3 = Pet("Dobby", 12, "cat")
# made a list of pets to run through. could also create a function to append the pets list with new pets using the Pet class
pets = [pet1,pet2,pet3]

for pet in pets:
    print(pet.name, "is a", pet.age, "year old", pet.species)
    print("It's", pet.calculate_human_age(), "human years old and its average lifespan is", pet.average_lifespan(), "years\n")
    
    