'''
A list of convenience constants used to describe all types of alleles that are used in evaluating the game state
'''

DISTANCE_TO_NEAREST_GHOST_IMPORTANCE = "distanceToNearestGhostImportance"
FOOD_PROXIMITY_IMPORTANCE = "foodProximityImportance"
NO_ISOLATED_FOOD_IMPORTANCE = "notLeavingIsolatedFoodImportance"
CAPSULE_PROXIMITY_IMPORTANCE = "capsuleProximityImportance"
ALLIED_AGENT_PROXIMITY_IMPORTANCE = "alliedAgentProximityImportance"
TIME_OF_DEFENCE_IMPORTANCE = "timeOfDefenceImportance"
SEARCH_REGIONS_IMPORTANCE_IMPORTANCE = "importanceOfSearchRegions"

DEFENSE_AREA_SIZE_IMPORTANCE = "defenseAreaSizeImportance"
PATROLLING_SAME_AREA_IMPORTANCE = "patrollingSameAreaImportance"
GUARDING_FOOD_WHILE_WALKING_IMPORTANCE = "guardingFoodWhileWalkingImportance"
CHASING_IMPORTANCE = "chasingImportance"
PROTECTING_PATHS_TO_FOOD_IMPORTANCE = "protectingStrategicPathsToTheFoodImportance"
PROTECTING_CAPSULES_IMPORTANCE = "protectingCapsulesImportance"

'''
Convenience mapping from allele names to chromosome indices
'''
CONSTANT_TO_CHROMOSOME_INDEX_MAPPING = {DISTANCE_TO_NEAREST_GHOST_IMPORTANCE: 0,
                                        FOOD_PROXIMITY_IMPORTANCE: 1,
                                        NO_ISOLATED_FOOD_IMPORTANCE: 2,
                                        CAPSULE_PROXIMITY_IMPORTANCE: 3,
                                        ALLIED_AGENT_PROXIMITY_IMPORTANCE: 4,
                                        TIME_OF_DEFENCE_IMPORTANCE: 5,
                                        SEARCH_REGIONS_IMPORTANCE_IMPORTANCE: 6,
                                        DEFENSE_AREA_SIZE_IMPORTANCE: 7,
                                        PATROLLING_SAME_AREA_IMPORTANCE: 8,
                                        GUARDING_FOOD_WHILE_WALKING_IMPORTANCE: 9,
                                        CHASING_IMPORTANCE: 10,
                                        PROTECTING_PATHS_TO_FOOD_IMPORTANCE: 11,
                                        PROTECTING_CAPSULES_IMPORTANCE: 12}
'''
Convenience list of all names of currently used alleles
'''
CONSTANTS_LIST = [DISTANCE_TO_NEAREST_GHOST_IMPORTANCE,
                  FOOD_PROXIMITY_IMPORTANCE, 
                  NO_ISOLATED_FOOD_IMPORTANCE,
                  CAPSULE_PROXIMITY_IMPORTANCE,
                  ALLIED_AGENT_PROXIMITY_IMPORTANCE,
                  TIME_OF_DEFENCE_IMPORTANCE,
                  SEARCH_REGIONS_IMPORTANCE_IMPORTANCE,
                  DEFENSE_AREA_SIZE_IMPORTANCE,
                  PATROLLING_SAME_AREA_IMPORTANCE,
                  GUARDING_FOOD_WHILE_WALKING_IMPORTANCE,
                  CHASING_IMPORTANCE,
                  PROTECTING_PATHS_TO_FOOD_IMPORTANCE,
                  PROTECTING_CAPSULES_IMPORTANCE]

NUMBER_OF_CHROMOSOMES = len(CONSTANTS_LIST)