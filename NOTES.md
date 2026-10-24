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

Questions
1. **Your predictions**. Where did you disagree with the pipeline on the five planted reports, and who was right?
My predictions where different from the pipeline on a-odd1 and a-odd2. I predicted both would be accepted, but the pipeline quarantined both as improbable. The pipline appears to be right because the combinations are unusual under the reference data, even though they pass the logic checks. 

2. **Independence**. The model treats each damage type as independent of the others, given the material. Name one real dependency it ignores. (Think about what crack and loose_base on the same object might mean.)
Crack and loose_base together suggest structural damage so a real object with both is more likely to be rated major and the generator hard-codes that. The model treats each damage type as independent given the material. Its only link to severity is the damage count, so it cannot tell a crack plus loose_base from a crack plus fading. Both count as 2+ and get the same severity probabilities.

3. **Parameters**. Count the model's free parameters and check against 35. Is 400 reference reports enough to estimate them? What would go wrong with 40?
For the likelihood model there are 35 free parameters: 4 for the five-way material distribution, 25 for five binary damage probabilities across five materials, and 6 for severity across the three damage-count buckets. Four hundred reports are enough for a rough estimate in this small example, but some material/damage combinations are still rare. With only 40 reports, the conditional groups would be very sparse, estimates would be noisy, and many combinations could have zero observations.

4. **Smoothing**. Your unsmoothed-model test raises an error. Describe a realistic production situation that would trigger the same failure.
Without smoothing, an unobserved material/damage combination gets probability zero. For example, a real report of corrosion on stone may never have appeared in the reference set. Scoring it calls log(0), which raises ValueError. This can happen in production when a rare combination appears, even if it is valid.

5.  **Calibration.** You calibrated the threshold on the same 400 reports the model was fitted on, yet the held-out quarantine rate came out close to 2%. Why was the gap small here? What would make it larger? (Week 6 will give this problem a name.)
he held-out quarantine rate came close to the 2% target (2.15%, 43 of 2,000 reports) because the held-out reports came from the same stable generator as the reference reports and this is a relatively small, smoothed model. The in-sample threshold is still optimistic because the same reports were used to fit the model and calibrate the cutoff. A smaller reference set, a more complex model with more parameters, or a changed real-world reporting distribution could all make the gap larger .

6. **Quarantine versus reject.** a-odd3 is a textile object with a crack *and* a loose base, rated major. Suppose it's a real, correctly reported, unusual find. What does this system do to people who report rare but true things? Where would you move the threshold if losing a rare discovery were worse than admitting one typo, and what would you pay for that?
a-odd3 passes the logic checks but is quarantined as improbable, meaning a rare but accurate report would be wrongly viewed as suspicious, leading to delays in analysis or entire disregardment of the result. The threshhold can be lowered to if losing a rare discovery were worse than admitting one typo. The consequence of this is that more problematic/false reports will pass as acceptable, increasing the risk of review and causing redundant work.


