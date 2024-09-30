def test_lol():
    assert 1 == 1

class TestGrouping():
    def test_group1(self):
        assert True

    def not_run(self):
        assert False

def will_not_be_run():
    assert 1 == 2
