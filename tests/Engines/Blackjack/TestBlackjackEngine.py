from Modules.Players.Dealer import Dealer


class TestBlackjackEngine:
    def test_create_dealer(self):
        dealer = Dealer()
        assert dealer is not None
