# Text-ID

HOW TO USE:

Text-ID takes in two texts and creates models for them based off word usage, their average word lengths, common stems they use, average
sentence lengths, and puncutaion used. Using these models it can take an unknown text and indetify, between the two models given, who
was more likely to have written the unknown text.

To use compare a text against two models use the function

compareTextWithTwoModels(<unknown text>, <text for model 1>, <text for model 2>)

This wil print out the values calculated for the similarities between each model and the unknown text and which model is most similar
to the unknown text.
