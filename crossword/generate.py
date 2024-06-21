import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        
        for var in self.domains:   
            self.domains[var] = set(filter(lambda w:len(w)==var.length,self.domains[var]))
            

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        

        if self.crossword.overlaps[x, y] == None:
            return False
        
        i, j = self.crossword.overlaps[x, y]
        
        to_remove = []

        for w1 in self.domains[x]:
            ac = False
            for w2 in self.domains[y]:
                if w1[i] == w2[j]:
                    ac = True
            if ac == False:
                to_remove.append(w1)

        if to_remove == []:
            return False
        else:
            for w in to_remove:
                self.domains[x].remove(w)
            return True
            



    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        

        
        if arcs == None:
            arcs = []
            for i in self.crossword.variables:
                for j in self.crossword.variables:
                    if i!=j:
                        arcs += [(i, j)]
             
        while arcs != []:
            (x, y) = arcs.pop(0)

            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False

                for z in self.crossword.neighbors(x):
                    if z!=y:
                        arcs += [(z, x)]

        return True





    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        
        for var in self.crossword.variables:
            if var not in assignment:
                return False

        for var in assignment:
            if assignment[var] not in self.crossword.words:
                return False

        return True
        



    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        
        s = []

        for x in assignment:
            if len(assignment[x]) != x.length:
                return False
            for y in self.crossword.neighbors(x):
                if y in assignment:
                    (i, j) = self.crossword.overlaps[x, y]
                    if assignment[x][i] != assignment[y][j]:
                        return False
            if assignment[x] in s:
                return False
            else:
                s += [assignment[x]]

        return True




    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        

        N = self.crossword.neighbors(var)

        occ = []

        for w1 in self.domains[var]:
            count = 0
            for n in N:
                (i, j) = self.crossword.overlaps[var, n]
                for w2 in self.domains[n]:
                    if w1[i] != w2[j]:
                        count += 1
            occ += [(w1,count)]

        occ = sorted(occ, key=lambda x:x[1])

        res = [q[0] for q in occ]

        return res



    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        
        candidates = []

        for var in self.crossword.variables:
            if var not in assignment:
                candidates += [(var,len(self.domains[var]),len(self.crossword.neighbors(var)))]
        
        candidates = sorted(candidates, key=lambda x: (x[1], x[2]))

        return candidates[0][0]




    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)

        for val in self.order_domain_values(var, assignment):
            assignment[var] = val
            if self.consistent(assignment):
                res = self.backtrack(assignment)
                if res != None:
                    return res
            del assignment[var]
        return None







def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)

    ######################
    """ for i in crossword.variables:
        for j in crossword.variables:
            if i==j:
                continue
            if crossword.overlaps[i,j]:
                x = i
                y = j

    creator.enforce_node_consistency()
    print(x, creator.domains[x])
    print(y, creator.domains[y])
    print(crossword.overlaps[x, y])

    creator.revise(x,y)

    print(x, creator.domains[x])
    print(y, creator.domains[y])


    exit() """
    #######################


    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
