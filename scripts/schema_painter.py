"""
Version 1.0

Listing authors :
Vadym Chobu
Tristan Rey
Jessen Page
Florian Desmons

Functions :
draw_schema(elements)
- Main function that takes list of the elements and starts to draw a scheme based on received list and screen_parameters
that is already provided in code

get_coordinates(row)
- Function that creates 2 rows of elements and gives them coordinates based on their quantity and taking into account
that they always should be centered

draw_simple_arrow(posA, posB, delta_x=0.0, delta_y=0.0)
- Draw a simple arrow based on coordinates of start, coordinates of end,
offset on x axes(if required) and offset on y axes(if required)

draw_curved_arrow(posA, posB, rad=0.0)
- Draw a curved arrow based on coordinates of start, coordinates of end and curvature modifier

draw_image(path, posXY)
- Draw an image based on its path + name + image extension(.png) and coordinates where this image will be created
"""


# Define the main function which creates the schema
def draw_schema(elements):
    # Libraries that are required to draw an image
    from matplotlib.patches import FancyArrowPatch

    import matplotlib.pyplot as plt
    import values_storage

    # Define screen parameters
    screen_parameters = {
        'width': 1920,
        'height': 1080,
        'px': 1 / plt.rcParams['figure.dpi'],
        'zoom': 0.3,
        'xMinValue': 0,
        'xMaxValue': 20,
        'yMinValue': 0,
        'yMaxValue': 10,
        'arrowStyle': 'simple',
        'arrowColor': 'black',
        'arrowMutation': 25,
    }

    # Function to get coordinates for elements
    def get_coordinates(row):
        modifier = 0
        # Calculate coordinates for row 1
        if row == 1:
            # Change modifier if number of elements is odd
            if len(elements) % 2 == 1:
                modifier = 1
            coord.append([((screen_parameters['xMaxValue'] / (
                    len(elements) // 2 + modifier)) * (half_one + 1) -
                    (screen_parameters['xMaxValue'] // (len(elements) // 2 + modifier)) / 2),
                    screen_parameters['yMaxValue'] / 2 + screen_parameters
                    ['yMaxValue'] / 6])

        # Calculate coordinates for row 2
        elif row == 2:
            coord.append([((screen_parameters['xMaxValue'] / (
                    len(elements) // 2)) * (half_one + 1) -
                    (screen_parameters['xMaxValue'] // (len(elements) // 2)) / 2),
                    screen_parameters['yMaxValue'] / 2 - screen_parameters
                    ['yMaxValue'] / 6])

    # Function to draw a simple arrow between two points
    def draw_simple_arrow(posA, posB, delta_x=0.0, delta_y=0.0):
        # Draw a simple arrow between two points
        arrow = FancyArrowPatch(posA, (posB[0] + delta_x, posB[1] + delta_y),
                    color=screen_parameters['arrowColor'],
                    arrowstyle=screen_parameters['arrowStyle'],
                    mutation_scale=screen_parameters['arrowMutation'])
        ax.add_patch(arrow)

    # Function to draw a curved arrow between two points
    def draw_curved_arrow(posA, posB, rad=0.0):
        # Draw a curved arrow between two points
        arrow = FancyArrowPatch(posA, posB,
                    color=screen_parameters['arrowColor'],
                    arrowstyle=screen_parameters['arrowStyle'],
                    mutation_scale=screen_parameters['arrowMutation'],
                    connectionstyle=f'arc3, rad = {rad}')
        ax.add_patch(arrow)

    # Function to draw an image at a specified position
    def draw_image(path, posXY):
        from matplotlib.offsetbox import OffsetImage, AnnotationBbox
        # Draw an image at a specified position
        ab = AnnotationBbox(OffsetImage(plt.imread(path), zoom=screen_parameters['zoom']), posXY)
        ax.add_artist(ab)

    # Create a figure and axes
    fig, ax = plt.subplots(figsize=(
        screen_parameters['width'] * screen_parameters['px'], screen_parameters['height'] * screen_parameters['px']))
    # Set axis properties
    plt.axis('off')
    ax.set_xlim([screen_parameters['xMinValue'], screen_parameters['xMaxValue']])
    ax.set_ylim([screen_parameters['yMinValue'], screen_parameters['yMaxValue']])
    # Check if there are elements to draw
    if len(elements) != 0:
        # Logic to draw elements based on the number of elements
        coord = []
        if len(elements) == 1:
            # Draw elements and arrows for a single element
            draw_image(f'../icons/{elements[0]}.png',
                       (screen_parameters['xMaxValue'] / 2, screen_parameters['yMaxValue'] / 2))
            draw_curved_arrow((screen_parameters['xMaxValue'] / 2 + 0.5, screen_parameters['yMaxValue'] / 2 + 0.45), (
                screen_parameters['xMaxValue'] / 2 - 0.5, screen_parameters['yMaxValue'] / 2 + 0.45), 0.5)
            draw_curved_arrow((screen_parameters['xMaxValue'] / 2 - 0.5, screen_parameters['yMaxValue'] / 2 - 0.45), (
                screen_parameters['xMaxValue'] / 2 + 0.5, screen_parameters['yMaxValue'] / 2 - 0.45), 0.5)

        elif len(elements) == 2:
            # Draw elements and arrows for two elements
            draw_image(f'../icons/{elements[0]}.png', (
                screen_parameters['xMaxValue'] / 2 - screen_parameters['xMaxValue'] / 8,
                screen_parameters['yMaxValue'] / 2))
            draw_image(f'../icons/{elements[1]}.png', (
                screen_parameters['xMaxValue'] / 2 + screen_parameters['xMaxValue'] / 8,
                screen_parameters['yMaxValue'] / 2))

            draw_curved_arrow((screen_parameters['xMaxValue'] / 2 - screen_parameters['xMaxValue'] / 8,
                               screen_parameters['yMaxValue'] / 2),
                              (screen_parameters['xMaxValue'] / 2 + screen_parameters['xMaxValue'] / 8,
                               screen_parameters['yMaxValue'] / 2 - 0.45),
                              0.5)
            draw_curved_arrow((screen_parameters['xMaxValue'] / 2 + screen_parameters['xMaxValue'] / 8,
                               screen_parameters['yMaxValue'] / 2),
                              (screen_parameters['xMaxValue'] / 2 - screen_parameters['xMaxValue'] / 8,
                               screen_parameters['yMaxValue'] / 2 + 0.45),
                              0.5)

        elif len(elements) == 3:
            # Draw elements and arrows for three elements
            draw_image(f'../icons/{elements[0]}.png', (
                screen_parameters['xMaxValue'] / 2 - screen_parameters['xMaxValue'] / 8,
                screen_parameters['yMaxValue'] / 2 + screen_parameters['yMaxValue'] / 8))
            draw_image(f'../icons/{elements[1]}.png', (
                screen_parameters['xMaxValue'] / 2 + screen_parameters['xMaxValue'] / 8,
                screen_parameters['yMaxValue'] / 2 + screen_parameters['yMaxValue'] / 8))
            draw_image(f'../icons/{elements[2]}.png', (screen_parameters['xMaxValue'] / 2,
                                                       screen_parameters['yMaxValue'] / 2 - screen_parameters[
                                                           'yMaxValue'] / 8))

            draw_simple_arrow((screen_parameters['xMaxValue'] / 2 - screen_parameters['xMaxValue'] / 8, 6.25), (
                screen_parameters['xMaxValue'] / 2 + screen_parameters['xMaxValue'] / 8,
                screen_parameters['yMaxValue'] / 2 + screen_parameters['yMaxValue'] / 8), -0.5)
            draw_curved_arrow((screen_parameters['xMaxValue'] / 2 + screen_parameters['xMaxValue'] / 8, 6.25), (
                screen_parameters['xMaxValue'] / 2 + 0.5,
                screen_parameters['yMaxValue'] / 2 - screen_parameters['yMaxValue'] / 8), -0.5)
            draw_curved_arrow((screen_parameters['xMaxValue'] / 2, 3.75), (
                screen_parameters['xMaxValue'] / 2 - screen_parameters['xMaxValue'] / 8,
                screen_parameters['yMaxValue'] / 2 + screen_parameters['yMaxValue'] / 8 - 0.45), -0.5)

        elif len(elements) % 2 == 0:
            # Draw elements and arrows for an even number of elements
            for half_one in range(len(elements) // 2):
                get_coordinates(1)
                draw_image(f'../icons/{elements[half_one]}.png', coord[half_one])

            first_half_reversed = range(len(elements) // 2 - 1, -1, -1)
            second_half = list(range(len(elements) // 2, len(elements)))

            for half_one, half_two in zip(first_half_reversed, second_half):
                get_coordinates(2)
                draw_image(f'../icons/{elements[half_two]}.png', coord[half_two])

            for pos in range(1, len(coord)):
                if pos == len(coord) - 1:
                    draw_simple_arrow(coord[pos - 1], coord[pos], 0.5)
                    draw_simple_arrow(coord[pos], coord[0], 0.0, -0.45)

                elif pos == len(coord) // 2:
                    draw_simple_arrow((coord[pos - 1]), (coord[pos]), 0.0, 0.45)

                elif pos < len(coord) // 2:
                    draw_simple_arrow((coord[pos - 1]), (coord[pos]), -0.5)

                elif pos > len(coord) // 2:
                    draw_simple_arrow((coord[pos - 1]), (coord[pos]), 0.5)

        elif len(elements) % 2 == 1:
            # Draw elements and arrows for an odd number of elements
            for half_one in range(len(elements) // 2 + 1):
                get_coordinates(1)
                draw_image(f'../icons/{elements[half_one]}.png', coord[half_one])

            first_half_reversed = range(len(elements) // 2 - 1, -1, -1)
            second_half = list(range(len(elements) // 2 + 1, len(elements)))

            for half_one, half_two in zip(first_half_reversed, second_half):
                get_coordinates(2)
                draw_image(f'../icons/{elements[half_two]}.png', coord[half_two])

            for pos in range(1, len(coord)):
                if pos == len(coord) - 1:
                    draw_simple_arrow((coord[pos - 1]), (coord[pos]), 0.5)
                    draw_simple_arrow((coord[pos]), (coord[0]), 0.0, -0.45)

                elif pos == len(coord) // 2 + 1:
                    draw_simple_arrow((coord[pos - 1]), (coord[pos]), 0.0, 0.45)

                elif pos < len(coord) // 2 + 1:
                    draw_simple_arrow((coord[pos - 1]), (coord[pos]), -0.5)

                elif pos > len(coord) // 2:
                    draw_simple_arrow((coord[pos - 1]), (coord[pos]), 0.5)

        # Draw unique elements at the bottom with annotations
        unique_elements = sorted(list(set(elements)))

        for element_index in range(len(unique_elements)):
            draw_image(f'../icons/{unique_elements[element_index]}.png', (element_index * 1.25, 0.5))
            ax.annotate(unique_elements[element_index], xy=(element_index * 1.25, 1), ha='center')

        # Adjust layout and save the schema as a PNG file
        fig.tight_layout()
        plt.savefig(values_storage.results_path+'\schema.png')

        ## Uncomment to plot the graph directly into matplotlib (not into file)
        # plt.get_current_fig_manager().full_screen_toggle()
        # plt.show()

    # Exit if there are no elements
    elif len(elements) == 0:
        print('Error: 0 elements have been detected')
        exit()
