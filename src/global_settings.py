# Hinweis: Einstellungen können nur hier zur Design-Zeit gesetzt werden! Laufzeitänderungen werden ignoriert.

### Gibt die Anzahl an Pixeln^2 pro Quadrant eines Bildes an.
### Minimum: 1 -> entspricht 4 mittlersten Pixel, Maximum: 32 entspricht allen Pixel
pixel_count = 32

### Contains the threshold for the distances between each species for them to be in a group.
### Remarks: after changing this value, you have to run SimilarSpeciesExtractor and GroupExtractor again.
threshold = 20

### Contains the minimal occurence for a species that a species is left in the trainset.
### Remarks: after changing this value, you have to run MostCommonValueExtractor, SpeciesDiffExtractor, SimilarSpeciesExtractor and GroupExtractor again.
min_occurence = 10

### Sets the count of digits for rounding the test and trainset in the analysis. Range: [0, 12]
round_data_ndigits = 0

### Gibt den Seed für den Split und das Training an.
### Contains the seed which is used to split the trainset and for training
seed = 4 # hier ist bei 0.1 jede Spezies aus dem Validierungsset im Trainingsset vorhanden

### Gibt das Split-Verhältnis von Trainings- und Validierungsset an.
### Contains the split ratio for trainset
train_val_split = 0.1

# not used?
#read_data_count = -1 # seed: 39609