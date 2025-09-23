from typing import Any
from queue import Queue


class CSP:
    def __init__(
        self,
        edges: list[tuple[str, str]],
        variables: list[str],
        domains: dict[str, set],
        
    ):
        """Constructs a CSP instance with the given variables, domains and edges.
        
        Parameters
        ----------
        variables : list[str]
            The variables for the CSP
        domains : dict[str, set]
            The domains of the variables
        edges : list[tuple[str, str]]
            Pairs of variables that must not be assigned the same value
        """
        # sys.setrecursionlimit(100000)
        # print(variables)
        self.variables = variables
        self.domains = domains
        self.edges = edges

        # Binary constraints as a dictionary mapping variable pairs to a set of value pairs.
        #
        # To check if variable1=value1, variable2=value2 is in violation of a binary constraint:
        # if (
        #     (variable1, variable2) in self.binary_constraints and
        #     (value1, value2) not in self.binary_constraints[(variable1, variable2)]
        # ) or (
        #     (variable2, variable1) in self.binary_constraints and
        #     (value1, value2) not in self.binary_constraints[(variable2, variable1)]
        # ):
        #     Violates a binary constraint
        self.binary_constraints: dict[tuple[str, str], set] = {}
        for variable1, variable2 in edges:
            self.binary_constraints[(variable1, variable2)] = set()
            for value1 in self.domains[variable1]:
                for value2 in self.domains[variable2]:
                    if value1 != value2:
                        self.binary_constraints[(variable1, variable2)].add((value1, value2))
                        self.binary_constraints[(variable1, variable2)].add((value2, value1))

    def ac_3(self) -> bool:
        """Performs AC-3 on the CSP.
        Meant to be run prior to calling backtracking_search() to reduce the search for some problems.
        
        Returns
        -------
        bool
            False if a domain becomes empty, otherwise True
        """
        # YOUR CODE HERE (and remove the assertion below)
        def arc_reduce(x, y):
            change = False
            toDiscard = []
            for i in self.domains[x]:
                for j in self.domains[y]:
                    if i != j:
                        break
                else:
                    toDiscard.append(i)
                    change = True
            for i in toDiscard:

                self.domains[x].discard(i)
                
            return change
        
        worklist = Queue(0)
        for i in self.edges:
            worklist.put(i)
        # print(worklist)
        i = 0
        # yeah, while is kinda bad, but i did not expect vscode to cocistently crash
        while not worklist.empty():
            # i = i+1
            # if i == 2:
            #     break
 
            arc = worklist.get()
            # print(worklist.empty())
            if arc_reduce(arc[0], arc[1]):
                if(len(self.domains[arc[0]]) == 0  or len(self.domains[arc[1]]) == 0):
                    return False
                else:
                    for i in self.edges:
                        if arc[0]==i[0]:
                            if i[1]!= arc[1]:
                                worklist.put((i[1], i[0]))
                        elif arc[0] == i[1]:
                            if i[0] != arc[1]:
                                worklist.put((i[0], i[1]))
        # print(self.domains)
        return True
        
                    

    def backtracking_search(self) -> None | dict[str, Any]:
        """Performs backtracking search on the CSP.
        
        Returns
        -------
        None | dict[str, Any]
            A solution if any exists, otherwise None
        """
        # print(self.domains)
        def backtrack(assignment: dict[str, Any], c):
            for i in self.edges:
                if i[0] not in assignment.keys() or i[1] not in assignment.keys():
                    continue

                if assignment[i[0]]==assignment[i[1]]:

                    # print(self.variables[self.variables.index(c)-1])

                    assignment.pop(self.variables[self.variables.index(c)-1], None)

                    return


            for i in assignment.keys():
                for j in assignment.keys():
                    if i==j:
                        continue
                    else:
                        # handout code for validating constraint
                        if ((i, j) in self.edges and assignment[i]==assignment[j]) or ((j,i) in self.edges and assignment[i]==assignment[j]):
                            assignment.pop(self.variables[self.variables.index(c)-1], None)
                            return

            # check if all variables hav a value, if true return value

            for i in self.variables:

                if i not in assignment.keys():

                    break

            else:
                
                return assignment

            # if not try each valid value from its domain

            for i in self.domains[c]:
                
                assignment[c] = i
                print(assignment)
                # keep trying end options

                if(self.variables.index(c)+1 == len(self.variables)):
                    a = backtrack(assignment, self.variables[self.variables.index(c)])
                else:     
                    a = backtrack(assignment, self.variables[self.variables.index(c)+1])
                print(a)
                if a:
                    return a
        return backtrack({}, self.variables[0])


def alldiff(variables: list[str]) -> list[tuple[str, str]]:
    """Returns a list of edges interconnecting all of the input variables
    
    Parameters
    ----------
    variables : list[str]
        The variables that all must be different

    Returns
    -------
    list[tuple[str, str]]
        List of edges in the form (a, b)
    """
    return [(variables[i], variables[j]) for i in range(len(variables) - 1) for j in range(i + 1, len(variables))]
