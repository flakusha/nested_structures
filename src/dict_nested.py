import unittest

class DictNested(dict):
    """
    Naive dictionary extension to work with deeply nested keys.
    Class provides methods to get info from deeply nested dictionary and
    set/reset/delete values in nested dict
    """

    def check_input(self, path):
        if isinstance(self, dict) or isinstance(self, DictNested):
            pass
        else:
            raise NotImplementedError

        if isinstance(path, str):
            if "." in path:
                path = path.split(".")
            else:
                path = list(path)
        elif isinstance(path, list) or isinstance(path, tuple):
            pass
        else:
            raise NotImplementedError
        return self, path

    def get_nested(self, path):
        self, path = DictNested.check_input(self, path)

        val = self
        tmp = None
        for key in path:
            if key in val:
                tmp = val[key]
            else:
                if tmp == None:
                    self = None
                    return self
                else:
                    self = val
                    return self

        self = tmp
        return self

    def set_nested(self, path, content = None, reset = False):
        self, path = DictNested.check_input(self, path)

        if self == False:
            val = {}
        else:
            val = self

        if content != None:
            reset = True

        level = 0
        for index, key in enumerate(path):
            if key in val:
                if isinstance(val[key], dict) or\
                isinstance(val[key], DictNested):
                    val = val[key]
                else:
                    if index == len(path) - 1\
                    and reset == False:
                        # and (not isinstance(val[key],
                        # dict) or isinstance(val[key], DictNested)) and\
                        return
                    else:
                        level = index
                        break
            else:
                level = index
                break

        if content == None:
            tmp = None
        else:
            tmp = content

        for index, key in enumerate(path[:level:-1]):
            if index == 0:
                tmp = {}
                tmp[key] = content
            else:
                tmp = {key: tmp}

        val[path[level]] = tmp
        self = val
    
    def del_nested(self, path):
        """
        Method removes entries:
        - if entry is data, which differs from dict, it is set to None
        - if entry is dict, it is set to {}
        - if len of path is 1, mathod has similar behavior to default
        del(dictionary[key])
        """
        # res = DictNested.get_nested(self, path)
        self, path = DictNested.check_input(self, path)

        if self == False:
            return

        # val = self
        for index, key in enumerate(path):
            if key in self:
                if len(path) == 1:
                    del(self[key])
                elif isinstance(self[key], dict) or\
                isinstance(self[key], DictNested):
                    if index < len(path) - 1:
                        self = self[key]
                    else:
                        self[key] = {}
                else:
                    self[key] = None
            else:
                raise KeyError

class TestNestedDictionary(unittest.TestCase):
    def test_get_default_dict(self):
        dictionary = {"a": {"b": None}}
        res = DictNested.get_nested(dictionary, "test")
        assert res == None
        res = DictNested.get_nested(dictionary, "a")
        assert res == {"b": None}
    
    def test_get_empty_dict(self):
        dictionary = {}
        res = DictNested.get_nested(dictionary, "test")
        assert res == None 
    
    def test_set_default(self):
        dictionary = {"some_key": "some_value"}
        DictNested.set_nested(dictionary, "abc")
        assert dictionary == {
            "some_key": "some_value",
            "a": {"b": {"c": None}}
        }

    def test_set_has_1_lvl(self):
        """
        In case dictionary already has keys and values, new ones should be
        added
        """
        dictionary = {"a": None}
        DictNested.set_nested(dictionary, ["a", "b", "c"])
        assert dictionary == {"a": {"b": {"c": None}}}
        dictionary = {"a": "some_value"}
        DictNested.set_nested(dictionary, ["a", "b", "c"])
        assert dictionary == {"a": {"b": {"c": None}}}

    def test_set_has_2_lvl(self):
        dictionary = {"a": {"b": None}}
        DictNested.set_nested(dictionary, ["a", "b", "c"])
        assert dictionary == {"a": {"b": {"c": None}}}

    def test_set_has_last_lvl(self):
        """
        In case dictionary already has the last level, nothing should change.
        If reset is True, value resets to None.
        """
        dictionary = {"a": {"b": {"c": {"d": None}}}}
        DictNested.set_nested(dictionary, ["a", "b", "c", "d"])
        assert dictionary == {"a": {"b": {"c": {"d": None}}}}
        dictionary = {"a": {"b": {"c": {"d": "some_value"}}}}
        DictNested.set_nested(dictionary, ["a", "b", "c", "d"])
        assert dictionary == {"a": {"b": {"c": {"d": "some_value"}}}}
        dictionary = {"a": {"b": {"c": {"d": "some_value"}}}}
        DictNested.set_nested(dictionary, ["a", "b", "c", "d"], reset = True)
        dictionary = {"a": {"b": {"c": {"d": None}}}}

    def test_set_with_content(self):
        dictionary = {"a": {"b": {"c": {"d": None}}}}
        DictNested.set_nested(dictionary, ["a", "b", "c", "d"],\
        content = ("e", "f"))
        assert dictionary == {"a": {"b": {"c": {"d": ("e", "f")}}}}

    def test_set_empty_init_dict(self):
        dictionary = {}
        DictNested.set_nested(dictionary, ["a", "b", "c", "d"])
        assert dictionary == {"a": {"b": {"c": {"d": None}}}}

    def test_del_entry(self):
        dictionary = {"a": "some_value", "b": {"c": {"d": "some_value"}},
        "c": "some_value"}
        DictNested.del_nested(dictionary, "bcd")
        assert dictionary == {"a": "some_value", "b": {"c": {"d": None}},
        "c": "some_value"}
        dictionary = {"a": "some_value", "b": {"c": {"d": "some_value"}},
        "c": "some_value"}
        DictNested.del_nested(dictionary, "bc")
        assert dictionary == {"a": "some_value", "b": {"c": {}},
        "c": "some_value"}
        dictionary = {"a": "some_value", "b": {"c": {"d": "some_value"}},
        "c": "some_value"}
        DictNested.del_nested(dictionary, "b")
        assert dictionary == {"a": "some_value", "c": "some_value"}

if __name__ == "__main__":
    unittest.main()
