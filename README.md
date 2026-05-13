# Wynncraft-WTP-Room-3-Optimization
Potential algorithm to solve r3 of wtp
THIS ONLY INVOLVES THE USE OF ALREADY PUBLIC INFORMATION AND THIS IS STILL WIP

Note that one of the tangents between 2 seals must be the optimal charging path (the proof is left to the reader), and note that a pair of circles have at most 4 common tangents.

Hence instead of grid searching the entire coordination plane, for any given instance of n seals, I will only need to check for 2 * (n-1) * n vectors to check for optimality (currently defined as the charge that gets most of the seals + rocks, prioritising rocks). With this in mind, a greedy algorithm can solve the whole r3 in on average 0.06s on my pc with this algorithm.
