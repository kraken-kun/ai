# exp 3

from typing import Generic, TypeVar, Dict, List, Optional
from abc import ABC, abstractmethod

V = TypeVar('V')  # variable type
D = TypeVar('D')  # domain type

# Base class for all constraints
class Constraint(Generic[V, D], ABC):
    # The variables that the constraint is between
    def __init__(self, variables: List[V]) -> None:
        self.variables = variables

    # Must be overridden by subclasses
    @abstractmethod
    def satisfied(self, assignment: Dict[V, D]) -> bool:
        ...

# A constraint satisfaction problem consists of variables of type V
# that have ranges of values known as domains of type D and constraints
# that determine whether a particular variable's domain selection is valid
class CSP(Generic[V, D]):
    def __init__(self, variables: List[V], domains: Dict[V, List[D]]) -> None:
        self.variables: List[V] = variables  # variables to be constrained
        self.domains: Dict[V, List[D]] = domains  # domain of each variable
        self.constraints: Dict[V, List[Constraint[V, D]]] = {}
        for variable in self.variables:
            self.constraints[variable] = []

    # Add a constraint to the CSP
    def add_constraint(self, constraint: Constraint[V, D]) -> None:
        for variable in constraint.variables:
            if variable not in self.variables:
                raise ValueError("Variable in constraint not in CSP")
            self.constraints[variable].append(constraint)

    # Check if the value assignment is consistent by checking all constraints
    # for the given variable against it
    def consistent(self, variable: V, assignment: Dict[V, D]) -> bool:
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    # Backtracking search algorithm to find a solution
    def backtracking_search(self, assignment: Dict[V, D] = {}) -> Optional[Dict[V, D]]:
        # If the assignment is complete, return it
        if len(assignment) == len(self.variables):
            return assignment

        # Select an unassigned variable
        unassigned = [v for v in self.variables if v not in assignment]

        # Select the variable with the smallest domain
        variable = min(unassigned, key=lambda v: len(self.domains[v]))

        # Try assigning each value in the domain to the variable
        for value in self.domains[variable]:
            local_assignment = assignment.copy()
            local_assignment[variable] = value
            if self.consistent(variable, local_assignment):
                result = self.backtracking_search(local_assignment)
                if result is not None:
                    return result
        return None

class MapColoringConstraint(Constraint[str, str]):
    def __init__(self, place1: str, place2: str) -> None:
        super().__init__([place1, place2])
        self.place1 = place1
        self.place2 = place2

    def satisfied(self, assignment: Dict[str, str]) -> bool:
        # If either place is not in the assignment, then it is not yet possible for their colors to conflict
        if self.place1 not in assignment or self.place2 not in assignment:
            return True
        # Check if the colors are different
        return assignment[self.place1] != assignment[self.place2]


# Create a CSP for map coloring problem
variables = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
domains = {v: ['Red', 'Green', 'Blue'] for v in variables}
csp = CSP(variables, domains)

# Add constraints
csp.add_constraint(MapColoringConstraint('WA', 'NT'))
csp.add_constraint(MapColoringConstraint('WA', 'SA'))
csp.add_constraint(MapColoringConstraint('NT', 'SA'))
csp.add_constraint(MapColoringConstraint('NT', 'Q'))
csp.add_constraint(MapColoringConstraint('SA', 'Q'))
csp.add_constraint(MapColoringConstraint('SA', 'NSW'))
csp.add_constraint(MapColoringConstraint('SA', 'V'))
csp.add_constraint(MapColoringConstraint('Q', 'NSW'))
csp.add_constraint(MapColoringConstraint('NSW', 'V'))

# Solve the CSP
solution = csp.backtracking_search()

# Print the solution
if solution is None:
    print("No solution found.")
else:
    print("Map coloring solution:")
    for place, color in solution.items():
        print(f"{place}: {color}")
