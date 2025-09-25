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
        # print(self.edges)
        # print(self.domains)
        """Performs backtracking search on the CSP.
        
        Returns
        -------
        None | dict[str, Any]
            A solution if any exists, otherwise None
        """
        # print(self.domains)
        def backtrack(assignment: dict[str, Any]):
            # procedure backtrack(P, c) is
            # if reject(P, c) then return
            # if accept(P, c) then output(P, c)
            # s ← first(P, c)
            # while s ≠ NULL do
            #     backtrack(P, s)
            #     s ← next(P, s)
            # print(assignment)
            # for i in assignment.keys():
            #     if assignment[i] not in self.domains[i]:
            #         print("WTF")
            for i in assignment.keys():
                for j in assignment.keys():
                    if assignment[i]==assignment[j]:
                        if (i,j) in self.edges or (j,i) in self.edges:
                            # print(assignment.popitem())
                            assignment.popitem()
                            return
            if(len(assignment.keys()) == len(self.variables)):
                return assignment
            current = 0
            if assignment!={}:
                current = list(assignment.keys())[-1]
                next = self.variables[self.variables.index(current)+1]
            else:
                next = self.variables[0]
            
            for i in self.domains[next]:
                # print(next)
                # print(current)
                # print(next)
                # print(self.domains[next])
                assignment[next] = i
                if backtrack(assignment) != None:
                    return assignment
        return backtrack({})


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
