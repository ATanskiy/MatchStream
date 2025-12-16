from matchstream_app.matchstream_backend.services import SwipeService


class FakeSwipeRepo:
    def __init__(self, mutual=False):
        self.mutual = mutual
        self.inserted = False
        self.matched = False

    def insert_swipe(self, *args):
        self.inserted = True

    def is_mutual_like(self, *args):
        return self.mutual

    def insert_match(self, *args):
        self.matched = True


def test_like_creates_match_if_mutual():
    repo = FakeSwipeRepo(mutual=True)
    service = SwipeService(repo)

    service.swipe("u1", "u2", "like")

    assert repo.inserted
    assert repo.matched


def test_dislike_does_not_match():
    repo = FakeSwipeRepo(mutual=True)
    service = SwipeService(repo)

    service.swipe("u1", "u2", "dislike")

    assert repo.inserted
    assert not repo.matched
