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
        if ((target_SearchState not in self.searched) and (target_SearchState not in self.search_stack)):
            self.search_stack.append(target_SearchState)
        # Job done.

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
        if ((target_SearchState not in self.searched) and (target_SearchState not in self.search_stack)):
            self.search_stack.insert(0, target_SearchState)
        # Job done.

        # If the target is the goal, update the class plan to match the path to the target.
        if (target_SearchState.wizard_loc == target_SearchState.portal_loc):
            self.plan = self.paths[target_SearchState]
        # Job done.


class WizardAstar(WizardSearchAgent):
    @dataclass(eq=True, frozen=True, order=True)
    class SearchState:
        wizard_loc: Location
        portal_loc: Location

    paths: dict[SearchState, tuple[float, list[WizardMoves]]] = {}
    search_pq: list[tuple[float, SearchState]] = []
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
        self.paths[initial_search_state] = 0, []
        self.search_pq = [(0, initial_search_state)]

    def is_goal(self, state: SearchState) -> bool:
        return state.wizard_loc == state.portal_loc

    def cost(self, source: GameState, target: GameState, action: WizardMoves) -> float:
        return 1

    def heuristic(self, target: GameState) -> float:
        # Manhattan Distance
        wizardLoc = target.get_all_entity_locations(Wizard)[0]
        portalLoc = target.get_all_tile_locations(Portal)[0]
        return abs(wizardLoc.row - portalLoc.row) + abs(wizardLoc.col - portalLoc.col)
        # Job done

    def next_search_expansion(self) -> GameState | None:
        # Chooses the next search node to expand
        return_node = heapq.heappop(self.search_pq)[1]
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
            target_path = [action] + source_path[1]
            cost = len(target_path)
            self.paths[target_SearchState] = (cost, target_path)
        else:
            cost = 1
            self.paths[target_SearchState] = (cost, [action])
            # Job done
        # Job done.

        insert_candidate = (cost + self.heuristic(target), target_SearchState)
        # Update the list of nodes to expand if we haven't explored it yet.
        if ((target_SearchState not in self.searched) and (insert_candidate not in self.search_pq)):
            heapq.heappush(self.search_pq, insert_candidate)
        # Job done.

        # If the target is the goal, update the class plan to match the path to the target.
        if (target_SearchState.wizard_loc == target_SearchState.portal_loc):
            self.plan = self.paths[target_SearchState][1]
        # Job done.


class CrystalSearchWizard(WizardSearchAgent):
    @dataclass(eq=True, frozen=True, order=True)
    class SearchState:
        wizard_loc: Location
        portal_loc: Location
        crystal_count: int

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
        crystal_count = len(game_state.get_all_tile_locations(Crystal))
        return self.SearchState(wizard_loc, portal_loc, crystal_count)

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

    def __init__(self, initial_state: GameState):
        self.start_search(initial_state)

    def manhattan_dist(self, loc1: Location, loc2: Location) -> float:
        # Manhattan Distance
        return abs(loc1.row - loc2.row) + abs(loc1.col - loc2.col)
        # Job done

    def heuristic(self, h_target: GameState) -> float:
        # If no crystals left, just calculate dist to the portal
        h_target_SearchState = self.game_to_search(h_target)
        if not h_target.get_all_tile_locations(Crystal):
            return self.manhattan_dist(h_target_SearchState.wizard_loc, h_target_SearchState.portal_loc)
        # Job done.

        # Distance to nearest crystal.
        crystal_dist = min(self.manhattan_dist(h_target_SearchState.wizard_loc, loc) for loc in crystal_dist)
        # Job done.

        # Longest distance between a crystal and another crystal or the portal
        targets = h_target.get_all_entity_locations(Crystal) + [h_target_SearchState.portal_loc]
        max_dist = 0

        for i in range(len(targets)):
            for j in range(i + 1, len(targets)):
                dist = self.manhattan_dist(targets[i], targets[j])
                if dist > max_dist:
                    max_dist = dist
        # Job done.

        # Sum the distances and return
        return crystal_dist + max_dist
        # Job done.


    def next_search_expansion(self) -> GameState | None:
        # Chooses the next search node to expand
        return_node = heapq.heappop(self.search_pq)[1]
        # Add the node we're expanding to the list of searched nodes
        return self.search_to_game(return_node)

    def process_search_expansion(
        self, source: GameState, target: GameState, action: WizardMoves
    ) -> None:
        # Update paths.
        target_SearchState = self.game_to_search(target)
        target_heuristic = self.heuristic(target)
        source_SearchState = self.game_to_search(source)
            # If we know the path to the start, preface the path to the target with the source's path. Otherwise (like at the start), start a new path.
        if (source_SearchState in self.paths):
            source_path = self.paths[source_SearchState]
            target_path = [action] + source_path[1]
            cost = len(target_path)
            self.paths[target_SearchState] = (cost, target_path)
        else:
            cost = 1
            self.paths[target_SearchState] = (cost + target_heuristic, [action])
            # Job done
        # Job done.

        insert_candidate = (cost + target_heuristic, target_SearchState)
        # Update the list of nodes to expand if it's better than the existing path cost.
        heapq.heappush(self.search_pq, insert_candidate)
        # Job done.

        # If the target is the goal, update the class plan to match the path to the target.
        if (self.is_goal(target_SearchState)):
            self.plan = self.paths[target_SearchState][1]
        # Job done.



class SuboptimalCrystalSearchWizard(CrystalSearchWizard):
    @dataclass(eq=True, frozen=True, order=True)
    class SearchState:
        wizard_loc: Location
        portal_loc: Location

    def heuristic(self, target: SearchState) -> float:
        # TODO YOUR CODE HERE
        raise NotImplementedError
