"""Assignment 2: Treemap Visualiser

=== CSC148 Fall 2016 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the code to run the treemap visualisation program.
It is responsible for initializing an instance of AbstractTree (using a
concrete subclass, of course), rendering it to the user using pygame,
and detecting user events like mouse clicks and key presses and responding
to them.
"""
import pygame
from tree_data import FileSystemTree
from population import PopulationTree


# Screen dimensions and coordinates
ORIGIN = (0, 0)
WIDTH = 1024
HEIGHT = 768
FONT_HEIGHT = 30                       # The height of the text display.
TREEMAP_HEIGHT = HEIGHT - FONT_HEIGHT  # The height of the treemap display.

# Font to use for the treemap program.
FONT_FAMILY = 'Consolas'


def run_visualisation(tree):
    """Display an interactive graphical display of the given tree's treemap.

    @type tree: AbstractTree
    @rtype: None
    """
    # Setup pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Render the initial display of the static treemap.
    render_display(screen, tree, '')

    # Start an event loop to respond to events.
    event_loop(screen, tree)



def render_display(screen, tree, text):
    """Render a treemap and text display to the given screen.

    Use the constants TREEMAP_HEIGHT and FONT_HEIGHT to divide the
    screen vertically into the treemap and text comments.

    @type screen: pygame.Surface
    @type tree: AbstractTree
    @type text: str
        The text to render.
    @rtype: None
    """
    # First, clear the screen
    pygame.draw.rect(screen, pygame.color.THECOLORS['black'],
                     (0, 0, WIDTH, HEIGHT))
    # TODO: Implement this function!
    # This must be called *after* all other pygame functions have run.
    for x in tree.generate_treemap((0, 0, WIDTH, TREEMAP_HEIGHT)):
        pygame.draw.rect(screen, x[1], x[0])
    _render_text(screen, text)
    pygame.display.flip()




def _render_text(screen, text):
    """Render text at the bottom of the display.

    @type screen: pygame.Surface
    @type text: str
    @rtype: None

    """
    # The font we want to use
    font = pygame.font.SysFont(FONT_FAMILY, FONT_HEIGHT - 8)
    text_surface = font.render(text, 1, pygame.color.THECOLORS['white'])

    # Where to render the text_surface
    text_pos = (0, HEIGHT - FONT_HEIGHT + 4)
    screen.blit(text_surface, text_pos)


def event_loop(screen, tree):
    """Respond to events (mouse clicks, key presses) and update the display.

    Note that the event loop is an *infinite loop*: it continually waits for
    the next event, determines the event's type, and then updates the state
    of the visualisation or the tree itself, updating the display if necessary.
    This loop ends when the user closes the window.

    @type screen: pygame.Surface
    @type tree: AbstractTree
    @rtype: None
    """
    # We strongly recommend using a variable to keep track of the currently-
    # selected leaf (type AbstractTree | None).
    # But feel free to remove it, and/or add new variables, to help keep
    # track of the state of the program.
    selected_leaf = None
    text = ''
    prev_leaf = None
    from math import ceil
    while True:
        # Wait for an event
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            return
        if event.type == pygame.MOUSEBUTTONUP:
            x = event.pos[0]
            y = event.pos[1]
            lst = tree.generate_treemap((0, 0, WIDTH, TREEMAP_HEIGHT))
            for i in range(len(lst)):
                rect = lst[i]
                if (rect[0][0] <= x <= rect[0][0] + rect[0][2])\
                        and (rect[0][1] <= y <= rect[0][1] + rect[0][3]):
                    selected_leaf = tree.list_leaves()[i]
                    if event.button == 1:
                        if prev_leaf == selected_leaf:
                            render_display(screen, tree, '')
                            prev_leaf = None
                        else:
                            text = str(selected_leaf.get_separator()) + \
                                '     (' + str(selected_leaf.data_size) + ')'
                            render_display(screen, tree, text)
                            prev_leaf = selected_leaf
                    elif event.button == 3:
                        selected_leaf.data_size = 0
                        selected_leaf.update_data_size()
                        render_display(screen, tree, text)
        if (prev_leaf is not None) and (prev_leaf.data_size > 0):
            if event.type == pygame.KEYUP:
                dsize = ceil(prev_leaf.data_size * 0.02)
                if event.key == pygame.K_UP:
                    prev_leaf.data_size += dsize
                    prev_leaf.update_data_size()
                    text = str(selected_leaf.get_separator()) + \
                        '     (' + str(selected_leaf.data_size) + ')'
                    render_display(screen, tree, text)
                elif event.key == pygame.K_DOWN:
                    prev_leaf.data_size -= dsize
                    prev_leaf.update_data_size()
                    text = str(selected_leaf.get_separator()) + \
                        '     (' + str(selected_leaf.data_size) + ')'
                    render_display(screen, tree, text)
        # TODO: detect and respond to other types of events.
        # Remember to call render_display if any data_sizes change,
        # as the treemap will change in this case.


def run_treemap_file_system(path):
    """Run a treemap visualisation for the given path's file structure.

    Precondition: <path> is a valid path to a file or folder.

    @type path: str
    @rtype: None
    """
    file_tree = FileSystemTree(path)
    run_visualisation(file_tree)


def run_treemap_population():
    """Run a treemap visualisation for World Bank population data.

    @rtype: None
    """
    pop_tree = PopulationTree(True)
    run_visualisation(pop_tree)


if __name__ == '__main__':
    # import python_ta
    # Remember to change this to check_all when cleaning up your code.
    # python_ta.check_errors(config='pylintrc.txt')

    # To check your work for Tasks 1-4, try uncommenting the following function
    # call, with the '' replaced by a path like
    # 'C:\\Users\\David\\Documents\\csc148\\assignments' (Windows) or
    # '/Users/dianeh/Documents/courses/csc148/assignments' (OSX)
    # _render_text((0, 0, 1024, 768), 'hi')
    # run_treemap_file_system('/Users/Overseer/Dropbox')
    # run_treemap_file_system('/Users/Overseer/Desktop/csc148/assignments')
    # run_treemap_file_system('/Users/Overseer/Desktop/csc148/assignments/a1/data')
    # run_treemap_file_system('/Users/Overseer/Desktop/m4p')
    # run_treemap_file_system('/Users/Overseer/Desktop/League of Legends.app')
    # To check your work for Task 5, uncomment the following function call.
    # run_treemap_file_system('/Users/Overseer/Desktop')
    run_treemap_population()
