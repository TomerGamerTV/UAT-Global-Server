class UraConfig:
    skill_event_weight: list[int]
    reset_skill_event_weight_list: list[str]

    def __init__(self, config: dict):
        if "skillEventWeight" not in config or "resetSkillEventWeightList" not in config:
            raise ValueError("Wrong configuration: must configure 'skillEventWeight' and 'resetSkillEventWeightList'")
        self.skill_event_weight = config["skillEventWeight"]
        self.reset_skill_event_weight_list = config["resetSkillEventWeightList"]
    
    def removeSkillFromList(self, skill: str):
        if skill in self.reset_skill_event_weight_list:
            self.reset_skill_event_weight_list.remove(skill)
            # If skill list is empty, reset weights
            # If the list is empty from the beginning, this branch won't trigger, and weights won't be reset
            if len(self.reset_skill_event_weight_list) == 0:
                self.skill_event_weight = [0, 0, 0]
    
    def getSkillEventWeight(self, date: int) -> int:
        if date <= 24:
            return self.skill_event_weight[0]
        elif date <= 48:
            return self.skill_event_weight[1]
        else:
            return self.skill_event_weight[2]

class AoharuConfig:

    preliminary_round_selections: list[int]
    aoharu_team_name_selection: int

    def __init__(self, config: dict):
        if "preliminaryRoundSelections" not in config or "aoharuTeamNameSelection" not in config:
            raise ValueError("Wrong configuration: must configure 'preliminaryRoundSelections' and 'aoharuTeamNameSelection'")
        self.preliminary_round_selections = config["preliminaryRoundSelections"]
        self.aoharu_team_name_selection = config["aoharuTeamNameSelection"]

    """ Get opponent index for specified round, index starts from 0, preliminary round 1 is 0 """
    def get_opponent(self, round_index: int) -> int:
        if round_index < 0 or round_index >= len(self.preliminary_round_selections):
            raise IndexError("Round index out of range")
        return self.preliminary_round_selections[round_index]
    
class ScenarioConfig:
    """ Configuration for all scenarios """
    ura_config: UraConfig = None
    aoharu_config: AoharuConfig = None
    
    def __init__(self, ura_config: UraConfig = None, aoharu_config: AoharuConfig = None):
        self.ura_config = ura_config
        self.aoharu_config = aoharu_config
