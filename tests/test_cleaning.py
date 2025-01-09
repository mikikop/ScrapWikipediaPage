from utils.cleaning import cleaning_list


# test the cleaning function
def test_cleaning_list(self):
    list_test = ["toto", "[", "tata", "titi", "]", "tutu"]
    assert cleaning_list(list_test) == ["toto", "tutu"]

    list_test2 = ["toto", "tata", "titi", "tutu"]
    assert cleaning_list(list_test2) == ["toto", "tata", "titi", "tutu"]

    list_test_3 = ["toto", "[", "tata", "]", "tete", "[", "titi", "]", "tutu"]
    assert cleaning_list(list_test_3) == ["toto", "tete", "tutu"]

    list_test_4 = []
    assert cleaning_list(list_test_4) == []
