The Spelling Algorithm
======================

1. First, look the number up in the lookup table. If it's there, get the
   spelling from the table and go to **Step 6**. If it's not, proceed to the
   next step.

2. Match the rules in order, one at a time, against the given number.
   Specifically, match the pattern of each consecutive rule until it is
   matched. If no rule has matched, raise an exception. Otherwise, take the
   matching rule and proceed to the next step.

3. Extract the values of the variables defined in the matching rule's pattern
   from the given number. This step will produce a mapping from variables to
   digits which will be used in the next step.

4. Expand the body of the matching rule by substituting variable values in
   place of the variable names. This step produces an expanded body with no
   variables left in it.

5. For every pair of braces in the matching rule's body, run this algorithm
   recursively, passing as an argument the number enclosed between the braces.

6. Squash all series of the consecutive orders (if there are any) by leaving
   only the leftmost order and dropping the rest in each one of such serieses.
