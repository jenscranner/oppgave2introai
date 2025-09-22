from typing import Any
from queue import Queue
import sys

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
        assert False, "Not implemented"

    def backtracking_search(self) -> None | dict[str, Any]:
        """Performs backtracking search on the CSP.
        
        Returns
        -------
        None | dict[str, Any]
            A solution if any exists, otherwise None
        """
        def backtrack(assignment: dict[str, Any], c):
            # print(assignment)
            # print(sys.getrecursionlimit())
            # YOUR CODE HERE (and remove the assertion below)
            # assert False, "Not implemented"
            # if reject(P, c) then return
            # if accept(P, c) then output(P, c)
            # s ← first(P, c)
            # while s ≠ NULL do
            #     backtrack(P, s)
            #     s ← next(P, s)
            
            # check if current assignment is valid
            for i in self.binary_constraints:
                if i[0] not in assignment.keys() or i[1] not in assignment.keys():
                    continue
                if assignment[i[0]]==assignment[i[1]]:
                    # print(self.variables[self.variables.index(c)-1])
                    assignment.pop(self.variables[self.variables.index(c)-1])
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
                # keep trying end options
                if(self.variables.index(c)+1 == len(self.variables)):
                    a = backtrack(assignment, self.variables[self.variables.index(c)])
                else:     
                    a = backtrack(assignment, self.variables[self.variables.index(c)+1])
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
