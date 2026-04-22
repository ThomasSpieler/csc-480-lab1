from model import (
    Location,
    Portal,
    EmptyEntity,
    Wizard,
    Goblin,
    Crystal,
    WizardMoves,
    GoblinMoves,
    GameAction,
    GameState,
)
from agents import WizardSearchAgent
import heapq
from dataclasses import dataclass


class WizardDFS(WizardSearchAgent):
    @dataclass(eq=True, frozen=True, order=True)
    # Search State: the wizard location and portal location (used to keep track)
    class SearchState:
        wizard_loc: Location
        portal_loc: Location

    paths: dict[SearchState, list[WizardMoves]] = {}
    search_stack: list[SearchState] = []
    searched: list[SearchState] = []
    initial_game_state: GameState

    def search_to_game(self, search_state: SearchState) -> GameState:
        initial_wizard_loc = self.initial_game_state.active_entity_location
        initial_wizard = self.initial_game_state.get_active_entity()

        new_game_state = (
            self.initial_game_state.replace_entity(
                initial_wizard_loc.row, initial_wizard_loc.col, EmptyEntity()
            )
            .replace_entity(
                search_state.wizard_loc.row, search_state.wizard_loc.col, initial_wizard
            )
            .replace_active_entity_location(search_state.wizard_loc)
        )

        return new_game_state

    def game_to_search(self, game_state: GameState) -> SearchState:
        wizard_loc = game_state.active_entity_location
        portal_loc = game_state.get_all_tile_locations(Portal)[0]
        return self.SearchState(wizard_loc, portal_loc)

    def __init__(self, initial_state: GameState):
        self.start_search(initial_state)

    def start_search(self, game_state: GameState):
        self.initial_game_state = game_state

        initial_search_state = self.game_to_search(game_state)
        self.paths = {}
        self.paths[initial_search_state] = []
        self.search_stack = [initial_search_state]

    def is_goal(self, state: SearchState) -> bool:
        return state.wizard_loc == state.portal_loc

    def next_search_expansion(self) -> GameState | None:
        # Chooses the next search node to expand
        return_node = self.search_stack.pop()
        # Add the node we're expanding to the list of searched nodes
        self.searched.append(return_node)
        return self.search_to_game(return_node)

    def process_search_expansion(
        self, source: GameState, target: GameState, action: WizardMoves
    ) -> None:
        
        # Update paths.
        target_SearchState = self.SearchState(wizard_loc=target.get_all_entity_locations(Wizard)[0], portal_loc=target.get_all_tile_locations(Portal)[0])
        source_SearchState = self.SearchState(wizard_loc=source.get_all_entity_locations(Wizard)[0], portal_loc=source.get_all_tile_locations(Portal)[0])
            # If we know the path to the start, preface the path to the target with the source's path. Otherwise (like at the start), start a new path.
        if (source_SearchState in self.paths):
            source_path = self.paths[source_SearchState]
            target_path = [action] + source_path
            self.paths[target_SearchState] = target_path
        else:
            self.paths[target_SearchState] = [action]
            # Job done
        # Job done.

        # Update the list of nodes to expand if we haven't explored it yet.
        if (target_SearchState not in self.searched):
            self.search_stack.append(target_SearchState)
        # Jobe done.

        # If the target is the goal, update the class plan to match the path to the target.
        if (target_SearchState.wizard_loc == target_SearchState.portal_loc):
            self.plan = self.paths[target_SearchState]
        # Job done.


class WizardBFS(WizardSearchAgent):
    @dataclass(eq=True, frozen=True, order=True)
    class SearchState:
        wizard_loc: Location
        portal_loc: Location

    paths: dict[SearchState, list[WizardMoves]] = {}
    search_stack: list[SearchState] = []
    initial_game_state: GameState

    def search_to_game(self, search_state: SearchState) -> GameState:
        initial_wizard_loc = self.initial_game_state.active_entity_location
        initial_wizard = self.initial_game_state.get_active_entity()

        new_game_state = (
            self.initial_game_state.replace_entity(
                initial_wizard_loc.row, initial_wizard_loc.col, EmptyEntity()
            )
            .replace_entity(
                search_state.wizard_loc.row, search_state.wizard_loc.col, initial_wizard
            )
            .replace_active_entity_location(search_state.wizard_loc)
        )

        return new_game_state

    def game_to_search(self, game_state: GameState) -> SearchState:
        wizard_loc = game_state.active_entity_location
        portal_loc = game_state.get_all_tile_locations(Portal)[0]
        return self.SearchState(wizard_loc, portal_loc)

    def __init__(self, initial_state: GameState):
        self.start_search(initial_state)

    def start_search(self, game_state: GameState):
        self.initial_game_state = game_state

        initial_search_state = self.game_to_search(game_state)
        self.paths = {}
        self.paths[initial_search_state] = []
        self.search_stack = [initial_search_state]

    def is_goal(self, state: SearchState) -> bool:
        return state.wizard_loc == state.portal_loc

    def next_search_expansion(self) -> GameState | None:
        # TODO: YOUR CODE HERE
        raise NotImplementedError

    def process_search_expansion(
        self, source: GameState, target: GameState, action: WizardMoves
    ) -> None:
        # TODO: YOUR CODE HERE
        raise NotImplementedError


class WizardAstar(WizardSearchAgent):
    @dataclass(eq=True, frozen=True, order=True)
    class SearchState:
        wizard_loc: Location
        portal_loc: Location

    paths: dict[SearchState, tuple[float, list[WizardMoves]]] = {}
    search_pq: list[tuple[float, SearchState]] = []
    initial_game_state: GameState

    def search_to_game(self, search_state: SearchState) -> GameState:
        initial_wizard_loc = self.initial_game_state.active_entity_location
        initial_wizard = self.initial_game_state.get_active_entity()

        new_game_state = (
            self.initial_game_state.replace_entity(
                initial_wizard_loc.row, initial_wizard_loc.col, EmptyEntity()
            )
            .replace_entity(
                search_state.wizard_loc.row, search_state.wizard_loc.col, initial_wizard
            )
            .replace_active_entity_location(search_state.wizard_loc)
        )

        return new_game_state

    def game_to_search(self, game_state: GameState) -> SearchState:
        wizard_loc = game_state.active_entity_location
        portal_loc = game_state.get_all_tile_locations(Portal)[0]
        return self.SearchState(wizard_loc, portal_loc)

    def __init__(self, initial_state: GameState):
        self.start_search(initial_state)

    def start_search(self, game_state: GameState):
        self.initial_game_state = game_state

        initial_search_state = self.game_to_search(game_state)
        self.paths = {}
        self.paths[initial_search_state] = 0, []
        self.search_pq = [(0, initial_search_state)]

    def is_goal(self, state: SearchState) -> bool:
        return state.wizard_loc == state.portal_loc

    def cost(self, source: GameState, target: GameState, action: WizardMoves) -> float:
        return 1

    def heuristic(self, target: GameState) -> float:
        # TODO: YOUR CODE HERE
        raise NotImplementedError

    def next_search_expansion(self) -> GameState | None:
        # TODO: YOUR CODE HERE
        raise NotImplementedError

    def process_search_expansion(
        self, source: GameState, target: GameState, action: WizardMoves
    ) -> None:
        # TODO: YOUR CODE HERE
        raise NotImplementedError


class CrystalSearchWizard(WizardSearchAgent):
    # TODO: YOUR CODE HERE

    def __init__(self, initial_state: GameState):
        self.start_search(initial_state)

    def next_search_expansion(self) -> GameState | None:
        # TODO YOUR CODE HEREs
        raise NotImplementedError

    def process_search_expansion(
        self, source: GameState, target: GameState, action: WizardMoves
    ) -> None:
        # TODO YOUR CODE HERE
        raise NotImplementedError



class SuboptimalCrystalSearchWizard(CrystalSearchWizard):
    @dataclass(eq=True, frozen=True, order=True)
    class SearchState:
        wizard_loc: Location
        portal_loc: Location

    def heuristic(self, target: SearchState) -> float:
        # TODO YOUR CODE HERE
        raise NotImplementedError
