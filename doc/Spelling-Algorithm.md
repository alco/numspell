The Spelling Algorithm
======================

On the highest level of abstraction, the spelling algorithm is a box with one
input and one output.

You feed an number to it and it returns a string with that number's spelling.


## The Basic Outline ##

When we descend one level of abstraction lower, we'll see the following steps
being performed:

1. If the number is **0**, return its spelling. Finish.

2. Decompose the number into a list of components by calling the `_parse_num`
   method.

3. Renumber the orders in the list from right to left starting with **1**. The
   orders are distinguished from other components easily because they are
   integers rather than strings.

4. If the selected language definition contains list passes, apply them one by
   one to our list of number components.

5. Spell out the remaining list elements by consulting with the NUMBERS table
   and ORDERS list.

6. Join all the list elements into a string, trim it at both ends, remove any
   duplicate spaces and return the string. Finish.


## Number Decomposition ##

The process of decomposing a number, as mentioned above, is implemented by the
`_parse_num` method. This method takes an integer and returns a list of
components. Let's take a closer look at its workings.

1. If the number is **0**, return an empty list. Finish.

2. Look the number up in the NUMBERS table. If it's there, return a list with
   the number as its single element. Note that we only check if there is a
   spelling for the number, we're not actually using it yet. Finish.

3. Match the rules in order, one at a time, against the given number.
   Specifically, match the pattern of each consecutive rule until it is
   matched. If such a rule is found, it is called the matching rule.
   Otherwise, raise an exception.

4. Extract the values of the variables defined by the matching rule's pattern
   from the given number. This step will produce a mapping from variables to
   digits which is used in the next step.

5. Expand the body of the matching rule by substituting variable values in
   place of the variable names. This step produces an expanded body with no
   variables left in it.

6. For every pair of braces in the matching rule's body, if its contents is not
   a star (`*`), run this algorithm recursively, passing as an argument the
   number enclosed between the braces and extend the list of components with
   the returned list. If the braces enclose a star, simply append an integer
   **0** to the list of components. The fact that **0** is an integer, whereas
   other list components are strings, makes it possible to later renumber the
   orders to obtain the correct spelling.

7. Return the obtained list of components.


## List Passes ##

List passes are user-defined transformations of list elements. They are used to
adjust the spelling of number components according to the rules of a given
language.

For English it is sufficient to use only decomposition rules, but for other
languages like Spanish or Russian it is necessary to further process number
components before obtaining the final spelling.

List passes are defined by means of template strings which use a simple syntax.
The syntax is described in detail on the [[Template Syntax]] page. For
real-world examples of passes, see the `spelling_es.py` and `spelling_ru.py`
files.
