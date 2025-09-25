from typing import Any
from queue import Queue


class CSP:
    def __init__(
        self,
        variables: list[str],
        domains: dict[str, set],
        edges: list[tuple[str, str]],
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

        def pair_allowed(v1: str, a1: int, v2: str, a2: int) -> bool: #Checks the binary_constraints in both directions. Kinda same as handout
            if (v1, v2) in self.binary_constraints and (a1, a2) not in self.binary_constraints[(v1, v2)]:                 
                #If they have an edge and values are not violating
                return False
            if (v2, v1) in self.binary_constraints and (a2, a1) not in self.binary_constraints[(v2, v1)]:
                #Just inverse
                return False
            return True

        def select_empty_cell(assignment: dict[str, set]): 
            #Selects an empty cell by checking if it has a domain greater than one
            #None if all domains have an assigned value
            for var in self.variables:
                if len(assignment[var]) > 1:
                    return var
            return None

        def check_constraints(assignment: dict[str, set], var: str, val: int) -> bool:
            for other in self.variables: #Others, i.e not itself
                if other == var: #Dont check against itself
                    continue
                dom2 = assignment[other]
                if len(dom2) == 1: #Only check for singletons 
                    val2 = next(iter(dom2)) #Get that singleton value
                    if not pair_allowed(var, val, other, val2): #Checks of pair violates binary constraints (for every pair)
                        return False
            return True
        

        def copy_domains(assignment: dict[str, Any]) -> dict[str, set]:
            return {k: set(v) for k, v in assignment.items()} #Copies domains so we can undo

        def solved (assignment: dict[str, Any]) -> bool:
            return all(len(s) == 1 for s in assignment.values())

        def backtrack(assignment: dict[str, Any]):
            if solved(assignment): #If domains are all singletons we have a complete solution
                return {k: next(iter(v)) for k, v in assignment.items()}

            empty_cell = select_empty_cell(assignment) #Finds empty_cell
            if empty_cell is None:
                return {k: next(iter(v)) for k, v in assignment.items()} #If we have no empty cells, we also have a solution


            for tentative in sorted(self.domains[empty_cell]): #Tries values from the domain of the  empty cell

                if not check_constraints(assignment, empty_cell, tentative):
                    continue

                assignment2 = copy_domains(assignment) #Copy domains
                assignment2[empty_cell] = {tentative} #Set tentative assignment the empty cell

                rec = backtrack(assignment2) #recurse
                if rec is not None:
                    return rec


        start = copy_domains(self.domains)
        return backtrack(start)

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
