# -*- coding: utf-8 -*-

import copy
import numpy as np
from const import COLOR_MAX, COLOR_MIN

def Rule_Wrapper(name, attr, param, component_idx):
    ret = None
    if name == "Constant":
        ret = Constant(name, attr, param, component_idx)
    elif name == "Progression":
        ret = Progression(name, attr, param, component_idx)
    elif name == "Arithmetic":
        ret = Arithmetic(name, attr, param, component_idx)
    elif name == "Distribute_Three":
        ret = Distribute_Three(name, attr, param, component_idx)
    else:
        raise ValueError("Unsupported Rule")
    return ret 


class Rule(object):
    """General API for a rule.
    Priority order: Rule on Number/Position always comes first
    """
    
    def __init__(self, name, attr, params, component_idx=0):
        self.name = name
        self.attr = attr
        self.params = params
        self.component_idx = component_idx
        self.value = 0
        self.sample()
    
    def sample(self):
        if self.params is not None:
            self.value = np.random.choice(self.params)
    
    def apply_rule(self, aot, in_aot=None):
        pass


class Constant(Rule):
    def __init__(self, name, attr, param, component_idx):
        super(Constant, self).__init__(name, attr, param, component_idx)
    
    def apply_rule(self, aot, in_aot=None):
        if in_aot is None:
            in_aot = aot
        return copy.deepcopy(in_aot)


class Progression(Rule):
    def __init__(self, name, attr, param, component_idx):
        super(Progression, self).__init__(name, attr, param, component_idx)
        self.first_col = True

    def apply_rule(self, aot, in_aot=None):
        current_layout = aot.children[0].children[self.component_idx].children[0]
        if in_aot is None:
            in_aot = aot
        second_aot = copy.deepcopy(in_aot)
        second_layout = second_aot.children[0].children[self.component_idx].children[0]
        if self.attr == "Position":
            change_value = self.value
            if current_layout.name == 'Mesh_Layout':
                if change_value > 0:
                    change_value = 3
                else:
                    change_value = -3
            second_pos_idx = (second_layout.position.get_value_idx() + change_value) % len(second_layout.position.values)
            # clip indices to be within number of entities
            second_pos_idx = np.clip(second_pos_idx, 0, second_layout.number.get_value() - 1)
            second_layout.position.set_value_idx(second_pos_idx)
            second_bbox = second_layout.position.get_value()
            for i in range(len(second_bbox)):
                second_layout.children[i].bbox = second_bbox[i]
        # ... keep all other attributes as-is
        return second_aot


class Arithmetic(Rule):
    def __init__(self, name, attr, param, component_idx):
        super(Arithmetic, self).__init__(name, attr, param, component_idx)
        self.memory = []
        self.color_count = 0
        self.color_white_alarm = False
    
    def apply_rule(self, aot, in_aot=None):
        current_layout = aot.children[0].children[self.component_idx].children[0]
        if in_aot is None:
            in_aot = aot
        second_aot = copy.deepcopy(in_aot)
        second_layout = second_aot.children[0].children[self.component_idx].children[0]
        if self.attr == "Position":
            if len(self.memory) > 0:
                first_layout_value_idx = self.memory.pop()
                if self.value > 0:
                    new_pos_idx = set(first_layout_value_idx) | set(current_layout.position.get_value_idx())
                else:
                    new_pos_idx = set(first_layout_value_idx) - set(current_layout.position.get_value_idx())
                # clip indices
                new_pos_idx = np.clip(list(new_pos_idx), 0, second_layout.number.get_value() - 1)
                second_layout.number.set_value_level(len(new_pos_idx) - 1)
                second_layout.position.set_value_idx(np.array(new_pos_idx))
            else:
                current_layout_value_idx = current_layout.position.get_value_idx()
                self.memory.append(current_layout_value_idx)
                while True:
                    second_layout.number.sample()
                    second_layout.position.sample(second_layout.number.get_value())
                    # clip indices
                    pos_idx = np.clip(second_layout.position.get_value_idx(), 0, second_layout.number.get_value() - 1)
                    second_layout.position.set_value_idx(pos_idx)
                    if self.value > 0:
                        if not (set(current_layout_value_idx) >= set(second_layout.position.get_value_idx())):
                            break
                    else:
                        if not (set(current_layout_value_idx) <= set(second_layout.position.get_value_idx())):
                            break
        return second_aot


class Distribute_Three(Rule):
    """Ternary operator. Three values across the columns form a fixed set.
    """

    def __init__(self, name, attr, param, component_idx):
        super(Distribute_Three, self).__init__(name, attr, param, component_idx)
        self.value_levels = []
        self.count = 0

    def apply_rule(self, aot, in_aot=None):
        current_layout = aot.children[0].children[self.component_idx].children[0]
        if in_aot is None:
            in_aot = aot
        second_aot = copy.deepcopy(in_aot)
        second_layout = second_aot.children[0].children[self.component_idx].children[0]

        row, col = divmod(self.count, 2)

        # Helper: ensure row exists
        if row >= len(self.value_levels):
            row = 0

        if self.attr == "Number":
            if self.count == 0:
                all_value_levels = list(range(current_layout.layout_constraint["Number"][0], 
                                              current_layout.layout_constraint["Number"][1] + 1))
                current_value_level = current_layout.number.get_value_level()
                all_value_levels = [v for v in all_value_levels if v != current_value_level]
                three_value_levels = np.random.choice(all_value_levels, 2, replace=False)
                three_value_levels = np.insert(three_value_levels, 0, current_value_level)
                self.value_levels = [three_value_levels[[0, 1, 2]]]
                # optionally shuffle additional orders
                if np.random.uniform() >= 0.5:
                    self.value_levels.append(three_value_levels[[1, 2, 0]])
                    self.value_levels.append(three_value_levels[[2, 0, 1]])
                else:
                    self.value_levels.append(three_value_levels[[2, 0, 1]])
                    self.value_levels.append(three_value_levels[[1, 2, 0]])
                second_layout.number.set_value_level(self.value_levels[0][1])
            else:
                if col == 0:
                    current_layout.number.set_value_level(self.value_levels[row][0])
                    current_layout.resample()
                    second_aot = copy.deepcopy(aot)
                    second_layout = second_aot.children[0].children[self.component_idx].children[0]
                    second_layout.number.set_value_level(self.value_levels[row][1])
                else:
                    second_layout.number.set_value_level(self.value_levels[row][2])

            second_layout.position.sample(second_layout.number.get_value())
            pos = second_layout.position.get_value()
            del second_layout.children[:]
            for i in range(len(pos)):
                entity = copy.deepcopy(current_layout.children[0])
                entity.name = str(i)
                entity.bbox = pos[i]
                if not current_layout.uniformity.get_value():
                    entity.resample()
                second_layout.insert(entity)

        elif self.attr == "Position":
            num_entities = current_layout.number.get_value()
            if self.count == 0:
                pos_0 = current_layout.position.get_value_idx()
                pos_1 = current_layout.position.sample_new(num_entities)
                pos_2 = current_layout.position.sample_new(num_entities, [pos_1])
                three_value_levels = np.array([pos_0, pos_1, pos_2])
                three_value_levels = np.clip(three_value_levels, 0, num_entities - 1)
                self.value_levels = [three_value_levels[[0, 1, 2]]]
                if np.random.uniform() >= 0.5:
                    self.value_levels.append(three_value_levels[[1, 2, 0]])
                    self.value_levels.append(three_value_levels[[2, 0, 1]])
                else:
                    self.value_levels.append(three_value_levels[[2, 0, 1]])
                    self.value_levels.append(three_value_levels[[1, 2, 0]])
                second_layout.position.set_value_idx(self.value_levels[0][1])
            else:
                if col == 0:
                    current_layout.number.set_value_level(len(self.value_levels[row][0]) - 1)
                    current_layout.resample()
                    current_layout.position.set_value_idx(self.value_levels[row][0])
                    pos = current_layout.position.get_value()
                    for i in range(len(pos)):
                        entity = current_layout.children[i]
                        entity.bbox = pos[i]
                    second_aot = copy.deepcopy(aot)
                    second_layout = second_aot.children[0].children[self.component_idx].children[0]
                    second_layout.position.set_value_idx(self.value_levels[row][1])
                else:
                    second_layout.position.set_value_idx(self.value_levels[row][2])

            pos = second_layout.position.get_value()
            for i in range(len(pos)):
                second_layout.children[i].bbox = pos[i]

        elif self.attr in ["Type", "Size", "Color"]:
            # Initialize value_levels if first call
            if self.count == 0:
                if self.attr == "Type":
                    constraint = current_layout.entity_constraint["Type"]
                elif self.attr == "Size":
                    constraint = current_layout.entity_constraint["Size"]
                else:
                    constraint = current_layout.entity_constraint["Color"]

                all_value_levels = list(range(constraint[0], constraint[1] + 1))
                three_value_levels = np.random.choice(all_value_levels, 3, replace=False)
                np.random.shuffle(three_value_levels)
                self.value_levels = [three_value_levels[[0, 1, 2]]]
                if np.random.uniform() >= 0.5:
                    self.value_levels.append(three_value_levels[[1, 2, 0]])
                    self.value_levels.append(three_value_levels[[2, 0, 1]])
                else:
                    self.value_levels.append(three_value_levels[[2, 0, 1]])
                    self.value_levels.append(three_value_levels[[1, 2, 0]])

            # Apply value levels safely
            if col == 0:
                value_current = self.value_levels[row][0]
                value_next = self.value_levels[row][1]
                for entity in current_layout.children:
                    getattr(entity, self.attr.lower()).set_value_level(value_current)
                for entity in second_layout.children:
                    getattr(entity, self.attr.lower()).set_value_level(value_next)
            else:
                value_next = self.value_levels[row][2]
                for entity in second_layout.children:
                    getattr(entity, self.attr.lower()).set_value_level(value_next)

        else:
            raise ValueError("Unsupported attriubute")

        self.count = (self.count + 1) % 6
        return second_aot

