import frame
from typing import List, Tuple

WORST_FITNESS = -100000000

# Wrapper function for basic bridge simulation. Takes as input a list of bridge
# points and named problem-instance parameters. Returns weight at which bridge
# failed or WORST_FITNESS if the bridge simulation failed. If gravity relaxation
# is enabled and a bridge cannot support its own weight, the value return is a
# portion of this large negative value relative to how much gravity relaxation
# was required. Base fitness function for Assignments 1a and 1b.
def basic_simulation(input_points, material:str, solid:bool, width:float, thickness=None, **kwargs):
    element_factory = frame.ElementFactory()

    assert material.casefold() in {'carbon fiber', 'wood', 'steel'}
    if material.casefold() == 'carbon fiber':
        element_factory.set_material_carbon_fiber()
    elif material.casefold() == 'wood':
        element_factory.set_material_wood()
    elif material.casefold() == 'steel':
        element_factory.set_material_steel()

    if solid:
        element_factory.set_cross_section_solid_square(width)
    else:
        assert thickness is not None
        element_factory.set_cross_section_hollow_square(width, thickness)

    results = frame.evaluate_frame(input_points=input_points, element_factory=element_factory, **kwargs)
    if results['invalid']:
        fitness = WORST_FITNESS
    else:
        fitness = results['weight'] + results['gravity_reduction']*WORST_FITNESS

    return fitness, results['frame']


# Fitness function that considers whether or not bridge elements enter an exclusion
# zone. Accepts the same inputs as basic_simulation with the addition of an
# exclusion zone definition. Returns raw fitness (WORST_FITNESS if constraint 
# is violated), unmodified fitness as generated by basic_simulation, the count 
# of bridge elements that collide with the exclusion zone, and a bridge object.
def constraint_satisfaction_simulation( input_points, material:str, solid:bool, width:float,
                                        exclusion_zones:List[Tuple[float, float]],
                                        thickness=None, **kwargs):
    fitness, frame = basic_simulation(input_points, material, solid, width, thickness, **kwargs)

    edges = [[(edge.start.x, edge.start.y), (edge.end.x, edge.end.y)] for edge in frame.elements]
    [edge.sort(key=lambda edge: edge[0]) for edge in edges]

    violations = 0
    for zone in exclusion_zones:
        x_bounds = zone[0]
        y_bounds = zone[1]
        for edge in edges:
            start_x, start_y = edge[0][0], edge[0][1]
            end_x, end_y = edge[1][0], edge[1][1]
            if ((start_x < x_bounds[0] and end_x < x_bounds[0]) or
               (start_x > x_bounds[1] and end_x > x_bounds[1]) or
               (start_y < y_bounds[0] and end_y < y_bounds[0]) or
               (start_y > y_bounds[1] and end_y > y_bounds[1])):
                continue

            corners = [
                (x_bounds[0], y_bounds[0]),
                (x_bounds[0], y_bounds[1]),
                (x_bounds[1], y_bounds[0]),
                (x_bounds[1], y_bounds[1])
            ]
            test_value = sum(line_relation(start_x, start_y, end_x, end_y, *corner)
                             for corner in corners)
            if 4 > test_value > -4:
                # Not all corners of the box were on the same side of the line, therefore collision
                violations += 1
    raw_fitness = WORST_FITNESS if violations > 0 else fitness
    return raw_fitness, fitness, violations, frame

# Fitness function that considers multiple objectives. Accepts the same inputs 
# as basic_simulation with the addition of a boolean that enables height as an
# objective. Considered objectives are unmodified fitness as generated by 
# basic_simulation, sum length of all connected bridge elements, and (optionally)
# the highest y-value of a point connected to the bridge. Returns a list of
# objective scores and a bridge object.
def multi_objective_simulation(input_points, material:str, solid:bool, width:float, thickness=None, **kwargs):
    fitness, frame = basic_simulation(input_points, material, solid, width, thickness, **kwargs)
    height = max(*[edge.start.y for edge in frame.elements], *[edge.end.y for edge in frame.elements])
    objectives = [fitness, height]

    return objectives, frame

# Utility function for plotting bridges using matplotlib. Takes a truss object
# as input.
def plot_bridge(*args, **kwargs):
    frame.plot_frame(*args, **kwargs)

# Used for calculating collisions with constraints.
# Sign determines which side of the line segment (x1, y1), (x2, y2) the given point (cx, cy) falls on.
def line_relation(x1, y1, x2, y2, cx, cy):
    relation = (y2-y1)*cx + (x1-x2)*cy + (x2*y1-x1*y2)
    if relation == 0:
        return 0
    else:
        return int(relation / abs(relation))