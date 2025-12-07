# -*- coding: utf-8 -*-

import numpy as np
from const import (ANGLE_MAX, ANGLE_MIN, ANGLE_VALUES, COLOR_MAX, COLOR_MIN,
                   COLOR_VALUES, NUM_MAX, NUM_MIN, NUM_VALUES, SIZE_MAX,
                   SIZE_MIN, SIZE_VALUES, TYPE_MAX, TYPE_MIN, TYPE_VALUES,
                   UNI_MAX, UNI_MIN, UNI_VALUES)


class Attribute(object):
    """Super-class for all attributes. Should not be instantiated directly."""
    def __init__(self, name):
        self.name = name
        self.level = "Attribute"
        self.previous_values = []

    def sample(self):
        pass

    def get_value(self):
        pass

    def set_value(self):
        pass

    def __repr__(self):
        return self.level + "." + self.name

    def __str__(self):
        return self.level + "." + self.name


class Number(Attribute):
    def __init__(self, min_level=NUM_MIN, max_level=NUM_MAX):
        super(Number, self).__init__("Number")
        self.value_level = 0
        self.values = NUM_VALUES
        self.min_level = min_level
        self.max_level = max_level

    def sample(self, min_level=None, max_level=None):
        if min_level is None:
            min_level = self.min_level
        if max_level is None:
            max_level = self.max_level
        min_level = max(self.min_level, min_level)
        max_level = min(self.max_level, max_level)
        if min_level > max_level:
            max_level = min_level
        self.value_level = np.random.randint(min_level, max_level + 1)

    def sample_new(self, min_level=None, max_level=None, previous_values=None):
        if min_level is None:
            min_level = self.min_level
        if max_level is None:
            max_level = self.max_level
        values = range(min_level, max_level + 1)
        if not previous_values:
            available = set(values) - set(self.previous_values) - set([self.value_level])
        else:
            available = set(values) - set(previous_values) - set([self.value_level])
        new_idx = np.random.choice(list(available))
        return new_idx

    def get_value_level(self):
        return self.value_level

    def set_value_level(self, value_level):
        self.value_level = value_level

    def get_value(self, value_level=None):
        if value_level is None:
            value_level = self.value_level
        return self.values[value_level]


class Type(Attribute):
    def __init__(self, min_level=TYPE_MIN, max_level=TYPE_MAX):
        super(Type, self).__init__("Type")
        self.value_level = 0
        self.values = TYPE_VALUES
        self.min_level = min_level
        self.max_level = max_level

    def sample(self, min_level=None, max_level=None):
        if min_level is None:
            min_level = self.min_level
        if max_level is None:
            max_level = self.max_level
        min_level = max(self.min_level, min_level)
        max_level = min(self.max_level, max_level)
        if min_level > max_level:
            max_level = min_level
        self.value_level = np.random.randint(min_level, max_level + 1)

    def sample_new(self, min_level=None, max_level=None, previous_values=None):
        if min_level is None:
            min_level = self.min_level
        if max_level is None:
            max_level = self.max_level
        values = range(min_level, max_level + 1)
        if not previous_values:
            available = set(values) - set(self.previous_values) - set([self.value_level])
        else:
            available = set(values) - set(previous_values) - set([self.value_level])
        new_idx = np.random.choice(list(available))
        return new_idx

    def get_value_level(self):
        return self.value_level

    def set_value_level(self, value_level):
        self.value_level = value_level

    def get_value(self, value_level=None):
        if value_level is None:
            value_level = self.value_level
        return self.values[value_level]


class Size(Attribute):
    def __init__(self, min_level=SIZE_MIN, max_level=SIZE_MAX):
        super(Size, self).__init__("Size")
        self.value_level = 3
        self.values = SIZE_VALUES
        self.min_level = min_level
        self.max_level = max_level

    def sample(self, min_level=None, max_level=None):
        if min_level is None:
            min_level = self.min_level
        if max_level is None:
            max_level = self.max_level
        min_level = max(self.min_level, min_level)
        max_level = min(self.max_level, max_level)
        if min_level > max_level:
            max_level = min_level
        self.value_level = np.random.randint(min_level, max_level + 1)

    def sample_new(self, min_level=None, max_level=None, previous_values=None):
        if min_level is None:
            min_level = self.min_level
        if max_level is None:
            max_level = self.max_level
        values = range(min_level, max_level + 1)
        if not previous_values:
            available = set(values) - set(self.previous_values) - set([self.value_level])
        else:
            available = set(values) - set(previous_values) - set([self.value_level])
        new_idx = np.random.choice(list(available))
        return new_idx

    def get_value_level(self):
        return self.value_level

    def set_value_level(self, value_level):
        self.value_level = value_level

    def get_value(self, value_level=None):
        if value_level is None:
            value_level = self.value_level
        return self.values[value_level]


class Color(Attribute):
    def __init__(self, min_level=COLOR_MIN, max_level=COLOR_MAX):
        super(Color, self).__init__("Color")
        self.value_level = 0
        self.values = COLOR_VALUES
        self.min_level = min_level
        self.max_level = max_level

    def sample(self, min_level=None, max_level=None):
        if min_level is None:
            min_level = self.min_level
        if max_level is None:
            max_level = self.max_level
        min_level = max(self.min_level, min_level)
        max_level = min(self.max_level, max_level)
        if min_level > max_level:
            max_level = min_level
        self.value_level = np.random.randint(min_level, max_level + 1)

    def sample_new(self, min_level=None, max_level=None, previous_values=None):
        if min_level is None:
            min_level = self.min_level
        if max_level is None:
            max_level = self.max_level
        values = range(min_level, max_level + 1)
        if not previous_values:
            available = set(values) - set(self.previous_values) - set([self.value_level])
        else:
            available = set(values) - set(previous_values) - set([self.value_level])
        new_idx = np.random.choice(list(available))
        return new_idx

    def get_value_level(self):
        return self.value_level

    def set_value_level(self, value_level):
        self.value_level = value_level

    def get_value(self, value_level=None):
        if value_level is None:
            value_level = self.value_level
        return self.values[value_level]


class Angle(Attribute):
    def __init__(self, min_level=ANGLE_MIN, max_level=ANGLE_MAX):
        super(Angle, self).__init__("Angle")
        self.value_level = 3
        self.values = ANGLE_VALUES
        self.min_level = min_level
        self.max_level = max_level

    def sample(self, min_level=None, max_level=None):
        if min_level is None:
            min_level = self.min_level
        if max_level is None:
            max_level = self.max_level
        min_level = max(self.min_level, min_level)
        max_level = min(self.max_level, max_level)
        if min_level > max_level:
            max_level = min_level
        self.value_level = np.random.randint(min_level, max_level + 1)

    def sample_new(self, min_level=None, max_level=None, previous_values=None):
        if min_level is None:
            min_level = self.min_level
        if max_level is None:
            max_level = self.max_level
        values = range(min_level, max_level + 1)
        if not previous_values:
            available = set(values) - set(self.previous_values) - set([self.value_level])
        else:
            available = set(values) - set(previous_values) - set([self.value_level])
        new_idx = np.random.choice(list(available))
        return new_idx

    def get_value_level(self):
        return self.value_level

    def set_value_level(self, value_level):
        self.value_level = value_level

    def get_value(self, value_level=None):
        if value_level is None:
            value_level = self.value_level
        return self.values[value_level]


class Uniformity(Attribute):
    def __init__(self, min_level=UNI_MIN, max_level=UNI_MAX):
        super(Uniformity, self).__init__("Uniformity")
        self.value_level = 0
        self.values = UNI_VALUES
        self.min_level = min_level
        self.max_level = max_level

    def sample(self):
        self.value_level = np.random.randint(self.min_level, self.max_level + 1)

    def sample_new(self):
        # Should not resample uniformity
        pass

    def set_value_level(self, value_level):
        self.value_level = value_level

    def get_value_level(self):
        return self.value_level

    def get_value(self, value_level=None):
        if value_level is None:
            value_level = self.value_level
        return self.values[value_level]


class Position(Attribute):
    """Position attribute (planar or angular or lines)."""
    def __init__(self, pos_type, pos_list):
        super(Position, self).__init__("Position")
        assert pos_type in ("planar", "angular", "lines")
        self.pos_type = pos_type
        self.values = pos_list
        self.value_idx = None
        self.isChanged = False

    def sample(self, num):
        length = len(self.values)
        assert num <= length
        self.value_idx = np.random.choice(range(length), num, False)

    def sample_new(self, num, previous_values=None):
        length = len(self.values)
        constraints = previous_values if previous_values else self.previous_values
        while True:
            finished = True
            new_value_idx = np.random.choice(length, num, False)
            if set(new_value_idx) == set(self.value_idx):
                continue
            for previous_value in constraints:
                if set(new_value_idx) == set(previous_value):
                    finished = False
                    break
            if finished:
                break
        return new_value_idx

    def sample_add(self, num):
        ret = []
        available = set(range(len(self.values))) - set(self.value_idx)
        idxes_2_add = np.random.choice(list(available), num, False)
        for index in idxes_2_add:
            self.value_idx = np.insert(self.value_idx, 0, index)
            ret.append(self.values[index])
        return ret

    def get_value_idx(self):
        return self.value_idx

    def set_value_idx(self, value_idx):
        self.value_idx = value_idx

    def get_value(self, value_idx=None):
        if value_idx is None:
            value_idx = self.value_idx
        return [self.values[idx] for idx in value_idx]

    def remove(self, bbox):
        idx = self.values.index(bbox)
        np_idx = np.where(self.value_idx == idx)[0][0]
        self.value_idx = np.delete(self.value_idx, np_idx)

