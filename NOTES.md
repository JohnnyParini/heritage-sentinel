# Lab P1

When swapping the problem file, our BFS implementation found a correct solution without requiring any modification. This demonstrates that our implementation of the search algorithm is modular and problem-agnostic. It can find a solution to a given set of inputs so long as the problem can be modeled after a graph, regardless of the nature of each individual element. Our algorithm only needs an input that is analogous to nodes on a graph with connecting edges. 

# Lab P2

The test case test_no_solution_returns_none passed, indicating that our original BFS implementation correctly handles cases where there are no solutions

# Lab P3

1. The hidden trap experiment showed a random order output everytime the program was run. This was because the values in a set aren't hashed the same way every time, so their order differs each time the program is run

2. The oracle breaking teaches us that our tests must evolve with our program. As the requirements for a valid output change, the tests that verify an output's validity must also change.

# Lab P4

Predictions:
-r1: Looks good
-r2: A loose base and crack shouldn't be a minor severity
-r3: Looks good
-r4: Stone can't rot
-r5: Looks good
-r6: Textile can't corrode
-r7: Looks good
-r8: Has damage with no severity
-r9: rot on stone and has severity minor for loose base and crack
-r10: Has no severity at all (not even none)
-r11: Looks good

Comparisons: I missed r11 being an unknown material 'marble', the system was right here and I predicted wrong saying it would pass fine.

1. Why does the while loop always terminate? What quantity grows each pass, and what bounds it?
At the start of each iteration of the while loop, changed is set to false, which is then set to true if anything changes. This makes it so eventually when nothing changes, changed will be false and the loop will end. The quantity that grows each pass is the size of known and it's bounded by however many conclusions/clauses there are (or in other words, len(known) <= len(conclusions/clauses)). 

2. Why does explain call sorted(premises)? (Think back to Lab 3.)
Explain calls sorted(premises) so we can be deterministic. Premises is a set and can have random ordering, so by sorting it, we ensure we always get the same outcome no matter what ordering was already in premises. This also makes testing easier/possible, since tests would only pass some of the time due to ordering if not deterministic with sorting.

Try to write a rule that rejects a report with severity major but no damage listed. Why can't you express it as a Horn clause? What would you have to add to the system, and what does it cost?
This can't be a Horn clause because we would have no way of making a no damage listed. No damage is the absence of damage, and we can't exactly check for that absence (the horns work like a + b -> c, but we wouldn't know not a or not b). 
One potential fix I see to this is in logic.py, we can add an if statement after the for loop that says if not changed (nothing changed) and not "has_damage" in known (the artifact is not damaged), then we can add not damaged and make changed = true to keep looping with not damaged. 
We could also alternatively check the facts at the beginning to see if there is anything in damages then adding in no damage if there is no damage in the facts
The overall cost of this isn't that high, at most it's like one if statement at the beginning if we go with the second implementation I proposed (I realize now the first implementation is prob a lot more inefficient).

# Lab P5
Predictions
1. I predict this will be accepted
2. I predict this will be acceped
3. I predict this will be quarantined
4. I predict this will be rejected
5. I predict this will be rejected

